"""
Cache Framework

Concepts

  There are 3 types of cache methods

  It is important to understand the difference between a cache_key and a 'list version key'.
    cache_key represents a unique cached return
    list version represents the version number of the underlying list source

  A page can have a cache_key associated with it e.g.
    'contents_index:site_version:list=articles:creator=unittest:_logged_in_creator=True:limit=3:1798'
  This uniquely identifys the returned data and is used as the redis cache_key and etag cache_key
  
  The final number in the example ':1798' is the version number of the list
  Regardless of some of the kwarg params the list is BASED ON 'the list of artilces for unittest'
  The list key is
    'cache_ver:contents_index:articles:unittest'
  the value of this key is 1798
  
  When a new article is created by unittest (or any other action that could invalidate the list of articles), this version number is incremented
  
  Description of cache flow:
    Calls that rely on multiple lists - or - Call that is a master call:
      Fetch the version numbers all lists the current call is dependent on - concatinating them together to make an eTag key
      if the client eTag matchs then execition can be aborted and no server cache or DB access is needed
      The client eTag is set to minimise repeated calls (this is particulally important for the optimisation of repeated API calls)
    A cahce_key is generated for each list call and a version number for the base list appended to the cache key
    Server lists are aquired from the server cache with this cache_key - else the server cache is populated with the calculated result
    Old cache_key versions wait to expire and are managed by redis - it would be impossible to invalidate every permuncation of kwargs to view a base list

  The site version number is appended to cache_keys because:
    new versions may have differnt returns
    there may be multiple API servers with different versions actives, we do not want the cache to interfear with each other
  It is not nessiary to invalidate the list version numbers between versions as regardless of site version they represent the state of the list and not the final return data
  
  
  The final type of cache is the pickeling of SQLAlchemy objects:
    On a call to get_member or get_content the return type is a SQLAlchmemy object
    This object is pickeled and stored in the member or content bucket
    On a change to a member or content object the cached pickedled blob key is completly removed from the cache
    As the key it not present, it is refetched and placed in the cache next get
"""

from pylons import app_globals, tmpl_context as c, config
from pylons.controllers.util import etag_cache as pylons_etag_cache

from collections import OrderedDict

import logging
log = logging.getLogger(__name__)

# -- Constants -----------------------------------------------------------------

cache_separator     = ':'
key_var_separator   = '='
list_item_separator = ','

cacheable_lists = {
    'contents_index': {
        #'content'     : {                      'creator':None}, # AllanC - Ballz, because dict key order is not reproducatble. A bug where some lists were being identifyed as 'content' because they were matching 'creator'. This dict is converted to an OrderedDict and the 'content' list added to the end
        'drafts'      : {'list':'drafts'     , 'creator':None},
        'articles'    : {'list':'articles'   , 'creator':None},
        'assignments' : {'list':'assignments', 'creator':None},
        'responses'   : {'list':'responses'  , 'creator':None},

        'boomed_by'   : {'boomed_by'  : None},
        'response_to' : {'response_to': None},
        'comments_to' : {'comments_to': None},
        #'assignments_accepted': {'accepted_by': None},
        #'assignments_invited' : {'accepted_by': None},
        #'assignments_active'   # AllanC - humm .. these are date realted? .. how can these be cached? are they cacheable?
        #'assignments_previous'
    },
    'members_index': {
        'followers'   : {'follower_of': None},
        'following'   : {'followed_by': None},
        'groups'      : {'groups_for' : None},
        'members_of'  : {'members_of' : None},
        'boomed'      : {'boomed'     : None},
    },
    'mesages_index': {
        'all'         : {'list':'all'         },
        'to'          : {'list':'to'          },
        'sent'        : {'list':'sent'        },
        'public'      : {'list':'public'      },
        'notification': {'list':'notification'},
    },
    'members_show' : {}, # Not used, just here as a reminder that these lists are tracked with version numbers
    'contents_show': {},
}
cacheable_lists['contents_index'] = OrderedDict(cacheable_lists['contents_index'])
cacheable_lists['contents_index'].update({'content'     : {                     'creator': None}})
#cacheable_lists['contents_index'].update({'drafts'      : {'list':'drafts'     ,'creator': None}})
#cacheable_lists['contents_index'].update({'articles'    : {'list':'articles'   ,'creator': None}})
#cacheable_lists['contents_index'].update({'assignments' : {'list':'assignments','creator': None}})
#cacheable_lists['contents_index'].update({'responses'   : {'list':'responses'  ,'creator': None}})


# Generate a reverse lookup to find the bucket for a list
cacheable_lists_key_lookup = {}
for key, list_dict in cacheable_lists.iteritems():
    for list_name in list_dict.keys():
        cacheable_lists_key_lookup.update({list_name:key})

uncacheable_kwargs = ['include_content', 'exclude_content', 'include_member', 'exclude_member']

# -- Variables -----------------------------------------------------------------

_cache = {} # Global dictionary that is imported by submodule, contins the cache buckets


# -- Init ----------------------------------------------------------------------

def init_cache(config):
    """
    Called by enviroment.py after most of the Pylons setup is done.
    """
    
    if config['beaker.cache.enabled']:
        from beaker.cache import CacheManager
        from beaker.util import parse_cache_config_options
        cache_manager = CacheManager(**parse_cache_config_options(config))
        
        # AllanC - no point in having buckets, these can be represented by a single cache and managed by redis
        #          but without putting them in a dict they cant be imported .. the dict serves as a reference to the conructed objects
        for bucket in ['members', 'contents', 'contents_index', 'members_index', 'messages_index', 'content_show', 'members_show']:
            _cache[bucket] = cache_manager.get_cache(bucket)
            if config['development_mode']: # We don't want to clear the cache on every server update. This could lead to the server undergoing heavy load as ALL the cache is rebuilt. This could be removed if it causes a problem
                _cache[bucket].clear()
        

# -- Exceptions ----------------------------------------------------------------

class ListVersionException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

# -- Utils ---------------------------------------------------------------------

def normalize_kwargs_for_cache(kwargs):
    """
    Do not allow db objects to be used as params
    Normalize everything down to strings or sorted lists of strings
    Skips kwargs beggining with '_'
    """
    for key, value in kwargs.iteritems():
        if not key.startswith('_'): # skip keys beggining with '_' as these have already been processed
            if isinstance(value, list):
                kwargs[key].sort()
            else:
                try   : value = value.id
                except: pass
                # AllanC: Suggestion - do we want to allow primitive types to pass through, e.g. int's and floats, maybe dates as well?
                value = str(value).strip()
                kwargs[key] = value
    return kwargs


# -- Core Version Number Management --------------------------------------------

def _gen_list_key(*args):
    """
    bucket, cacheable_list_name, cacheable_variables
    
    typically called with args to identify the current key e.g.
      'contents_index', 'articles', 'unittest'
    """
    def string_arg(arg):
        if isinstance(arg, list):
            arg = list_item_separator.join(arg)
        if not isinstance(arg, basestring):
            arg = str(arg)
        return arg
    return cache_separator.join(['cache_ver']+[string_arg(arg) for arg in args])

def get_list_version(*args):
    if not _cache: return
    key   = _gen_list_key(*args)
    try:
        value = app_globals.memcache.get(key)
        #print('got list %s as %s' % (key,value))
        return value or 0
    except TypeError:
        e = 'unable to aquire list verison for %s' % key
        log.warn(e)
        raise ListVersionException(e)
    #if value == None:
    #    return invalidate_list_version()

def invalidate_list_version(*args):
    if not _cache: return
    key    = _gen_list_key(*args)

    try:
        value = app_globals.memcache.incr(key)
        #print('inc list %s to %s' % (key,value))
        #import traceback
        #traceback.print_stack()
        return value
    except TypeError:
        #raise ListVersionException('unable to invalidate list verison for %s' % key)
        pass # We dont want to DIE on invalidating, because invalidate is run on every object update regardless of if cache is enabled - but thats why we put the if not _cache above?
    return
    
def get_lists_versions(lists, list_variables):
    """
    lists is a string list of list names
    for each list name - get the cache version number
    return a list of tuples ('list_name',version)
    typically the variables identifying the list will be the same - e.g. in members_show every list refers to
    
    This is not perfect because there could be names in the contens_index and member_index that are the same .. this will cause problems
    """
    list_versions = []
    for list_name in lists:
        bucket = cacheable_lists_key_lookup.get(list_name)
        if bucket:
            list_versions.append(get_list_version(bucket, list_name, list_variables))
        else:
            list_versions.append(get_list_version(        list_name, list_variables))
    #for bucket, cacheable_list_name, cacheable_variables in cacheable_list_name_variables_tuples:
    #    list_versions.append(get_list_version(bucket, cacheable_list_name, cacheable_variables))
    #return cache_separator.join([str(i) for i in list_versions])
    return zip(lists, list_versions)

def gen_key_for_lists(lists, list_variables, **kwargs):
    return '' # AllanC - The content_show and member_show methods dont have version numbers for every list - for now DONT return a key but have the structure in place in the methods so that when this is enabled it'll be rockin
    try:
        cache_key = cache_separator.join([list_name+key_var_separator+str(list_version) for list_name, list_version in get_lists_versions(lists, list_variables)])
    except ListVersionException:
        return ''
    etag_cache(cache_key, **kwargs) # AllanC - it is not sendible at this point to eTag member_show and contents_show as every list does not have a version number .. can we actually ever to this at all with assignments_active and actions?
    return cache_key
    

# -- set eTag cache key --------------------------------------------------------

def etag_cache(cache_key, is_etag_master=False):
    """
    Set the eTag header
    (this could be moved out to the controller actions, but it seems nice to do all the cache work in one place rather than having each controller set it separately)
    We need to know if this has been activated via a master controller call or a sub controller call .. an eTag can only be set once
    
    is_etag_master is designed a flag to indicate that after this eTag is created - no more etags are to be set
    """
    if cache_key and not c.etag_master_generated and config['cache.etags.enabled']:
        log.debug("HTTP eTag being set %s" % cache_key)
        pylons_etag_cache(cache_key) # Set eTag in response header - if etag matchs the eTag in the original request header then abort execution and return the correct HTTP code for "use client etag cached ver"
        log.debug("HTTP eTag does not match client key; continueing ...")
    if is_etag_master:
        c.etag_master_generated = True


# -- Generate Cache Key (from index kwargs) with version number-----------------

def get_cache_key(bucket, kwargs, normalize_kwargs=False):
    """
    Take args for an index action and return
      - '' if not cachable
      - 'xxx tag string xxx' if cachable
      
    ignoring  keys starting with '_' but still using these keys as part of the eTag generation
    
    Checks if the kwargs match the know cachable lists in cacheable_index
    
    it is assumed that kwargs have be pre-processed with 'normalize_kwargs_for_cache', a param is included to do this without the need to call the normalize function specifically
    
    will return and empty string if this item is not cacheable
    
    with version number of idetifyed list
    """
    
    cache_key = ''

    if set(kwargs.keys()) & set(uncacheable_kwargs): # If kwargs contains any of the uncacheable keys - then abort caching
        return cache_key
    
    if normalize_kwargs:
        kwargs = normalize_kwargs_for_cache(kwargs)
    
    #print "cache_input: %s" % kwargs
    
    cacheable_kwargs_keys = [k for (k,v) in kwargs.iteritems() if not k.startswith('_')]  # Strip the keys starting with '_' as they are not needed. We need to preserve the kwargs for later as the _logged_in and _private are going to form part of the cache key
    cacheable_kwargs_keys.sort()
    

    
    # Iterate through all the 
    for cacheable_list_name, cache_args_dict in cacheable_lists[bucket].iteritems():
        #if len(cache_args_dict) != len(cacheable_kwargs_keys): # Optimisation - no point in deeply comparing a list of args that dont match
        #    continue
        
        # Try to match the passed kwargs with the cacheable known lists
        #cacheable_list_name = cache_name
        cacheable_variables = []
        for key in cache_args_dict: # Iterate over kwargs keys to see if they match the cacheable list
            key_match = key in cacheable_kwargs_keys
            if   key_match and not cache_args_dict[key]: # if the value stored in the cache_args_dict is None then that key is a variable and can be added to the variable list
                cacheable_variables.append(kwargs[key])
            elif key_match and     cache_args_dict[key] and cache_args_dict[key]==kwargs[key]: # If the key exisits in cachable_list and the key value is NOT null - then check the value of the keys match
                continue # if the key values match then proceed to check the remaining key values
            else:
                cacheable_list_name = None
                break # If the kwargs contains an arg that isnt in the cacheable list, this item is not cacheable - proceed to check the other lists
        
        # After the for look has run though all the keys, and has not aborted to the next item with continue - the kwargs match this cacheable_list
        if cacheable_list_name:
            #print "cacheable_list_name: %s" % cacheable_list_name
            try:
                list_version = get_list_version(bucket, cacheable_list_name, cacheable_variables)
            except ListVersionException:
                return '' # We cannot allow etags if no list version is present
                #config['cache.etags.enabled'] = False # If we cant get to memcache DONT use etags, lists will never refresh
            
            # Sort keys to normaize the cache_key that is generated
            keys_sorted = [k for k in kwargs.keys()]
            keys_sorted.sort()
            
            # Append all kwarg values and list version number into one string tag to idnetify this cacheable item
            cache_values  = [app_globals.version or 'dev', bucket, "%s%s%s" % (cacheable_list_name, key_var_separator, list_version)]
            cache_values += ["%s%s%s" % (key, key_var_separator, kwargs[key]) for key in keys_sorted]
            cache_key = cache_separator.join(cache_values)
            
            break # There is no need to check any more lists - as we have matched a chacheable item and no other will match
    
    #log.debug("cache_key: %s" % cache_key)
    
    etag_cache(cache_key)
    
    return cache_key



#-- Invalidate Objects ---------------------------------------------------------

def _invalidate_obj_cache(bucket, obj, fields=['id']):
    """
    Some objects can be fetched useing a varity of keys
    This is a pain in the ass as we have to invalidate multiple keys per object, because we dont know how it could be indexed
    Invalidate them ALL!! .. ALL OF THEM!!! .. for this object passed
    """
    assert obj
    cache = _cache.get(bucket)
    if cache:
        keys_to_invalidate = []
        if isinstance(obj, basestring):
            keys_to_invalidate.append(obj)
        else:
            for field in [field for field in fields if hasattr(obj, field)]:
                keys_to_invalidate.append(str(getattr(obj, field)))
        for key in keys_to_invalidate:
            cache.remove_value(key=key)
        

def invalidate_member(member, remove=False):
    _invalidate_obj_cache('member', member, ['id','email'])
    invalidate_list_version('member', member.id)

    # If removing the member entirely - invalidate all sub lists
    if remove:
        for list in ['content','drafts', 'articles', 'assignments', 'responses', 'boomed_by']:
            invalidate_list_version('contents_index', list, member.id)
        # TODO
        # member index lists
        # messages index lists


def invalidate_content(content, remove=False):
    """
    Invalidate:
      1.) The get_content(?) db object cache
      2.) Any lists associated with this content or content.parent
    """
    _invalidate_obj_cache('content', content)
    
    #print "invalidate content: %s %s" %(content.id, content.title)
    
    try   : parent_id = content.parent_id or content.parent.id
    except: parent_id = None
    
    try   : creator_id = content.creator_id or content.creator.id
    except: creator_id = None
    
    if content.__type__ == 'comment':
        #import traceback
        #traceback.print_stack()
        assert parent_id
        invalidate_list_version('contents_index', 'comments_to', parent_id) # Comments always have a parent id
        
    else:
        
        invalidate_list_version('contents_index','content', creator_id)
        
        if parent_id:
            invalidate_list_version('contents_index', 'response_to', parent_id ) # Invalidate responses to the parent content
            invalidate_list_version('contents_index', 'responses'  , creator_id) # Invalidate responses this creator has written
            # we dont need to invalidate the whole parent object - just the responses list
        
        if content.__type__ == 'draft':
            invalidate_list_version('contents_index', 'drafts'      , creator_id)
        
        if content.__type__ == 'article' and not parent_id:
            invalidate_list_version('contents_index', 'articles'    , creator_id)
            
        if content.__type__ == 'assignment':
            invalidate_list_version('contents_index', 'assignments' , creator_id)

    # If removing the content item entirely - invalidate all sub lists
    if remove:
        for list in ['comments_to', 'response_to']:
            invalidate_list_version('contents_index', list, content.id)
        # TODO
        # accepted lists
        # member index lists
