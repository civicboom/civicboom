from pylons import app_globals

from collections import OrderedDict

# -- Constants -----------------------------------------------------------------

cache_separator = ':'

cacheable_lists = {
    'contents_index': {
        #'content'     : {'creator': None}, # AllanC - Ballz, because dict key order is not reproducatble. A bug where some lists were being identifyed as 'content' because they were matching 'creator'. This dict is converted to an OrderedDict and the 'content' list added to the end
        'boomed_by'   : {'boomed_by': None},
        'drafts'      : {'list':'drafts'     , 'creator':None},
        'articles'    : {'list':'articles'   , 'creator':None},
        'assignments' : {'list':'assignments', 'creator':None},
        'responses'   : {'list':'responses'  , 'creator':None},
        'responses_to': {'response_to': None},
        #'comments' : {} # AllanC - todo - comments could come from index?
        #'assignments_accepted': {'accepted_by': None},
        #'assignments_invited' : {'accepted_by': None},
        #'assignments_active'   # AllanC - humm .. these are date realted? .. how can these be cached? are they cacheable?
        #'assignments_previous'
    },
    'members_index': {
        'followers' : {'follower_of': None},
        'following' : {'followed_by': None},
        'groups'    : {'groups_for' : None},
        'members_of': {'members_of' : None},
        'boomed'    : {'boomed'     : None},
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
cacheable_lists['contents_index'].update({'content'     : {'creator': None}})

uncacheable_kwargs = ['include_content', 'exclude_content', 'include_member', 'exclude_member']

# -- Variables -----------------------------------------------------------------

_cache = {} # Global dictionary that is imported by submodule, contins the cache buckets


# -- Init ----------------------------------------------------------------------

def init_cache(config):
    """
    Called by enviroment.py after most of the Pylons setup is done.
    """
    from beaker.cache import CacheManager
    from beaker.util import parse_cache_config_options
    cache_manager = CacheManager(**parse_cache_config_options(config))
    
    if config['beaker.cache.enabled']:
        for bucket in ['members', 'contents', 'contents_index', 'members_index', 'messages_index', 'content_show', 'members_show']:
            _cache[bucket] = cache_manager.get_cache(bucket)
            # AllanC - WTF!! .. this does not clear the individual bucket!! .. it clears ALL of redis! including the sessions .. WTF! ... can I not just clear my bucket?!
            #if config['development_mode']: # We don't want to clear the cache on every server update. This could lead to the server undergoing heavy load as ALL the cache is rebuilt. This could be removed if it causes a problem
            #    _cache[bucket].clear()


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
    """
    def string_arg(arg):
        if isinstance(arg, list):
            arg = ",".join(arg)
        if not isinstance(arg, basestring):
            arg = str(arg)
        return arg
    return cache_separator.join(['cache']+[string_arg(arg) for arg in args])

def get_list_version(*args):
    key   = _gen_list_key(*args)
    value = app_globals.memcache.get(key) or 0
    return value

def invalidate_list_version(*args):
    key    = _gen_list_key(*args)
    value  = app_globals.memcache.get(key) or 0
    value += 1
    app_globals.memcache.set(key, value)
    return value
    
def get_lists_versions(cacheable_identifyer_tuples):
    list_versions = ['cache']
    for bucket, cacheable_list_name, cacheable_variables in cacheable_list_name_variables_tuples:
        list_version.append(get_list_version(bucket, cacheable_list_name, cacheable_variables))
    return cache_separator.join([str(i) for i in list_versions])
    

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
            list_version = get_list_version(bucket, cacheable_list_name, cacheable_variables)
            
            # Sort keys to normaize the cache_key that is generated
            keys_sorted = [k for k in kwargs.keys()]
            keys_sorted.sort()
            
            # Append all kwarg values and list version number into one string tag to idnetify this cacheable item
            cache_values  = [key+'='+str(kwargs[key]) for key in keys_sorted]
            cache_values += ['ver=' +str(list_version)                      ]
            cache_key = cache_separator.join(cache_values)
            
            break # There is no need to check any more lists - as we have matched a chacheable item and no other will match
    
    #print "cache_key: %s" % cache_key
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
        

def invalidate_member(member):
    _invalidate_obj_cache('members', member, ['id','username', 'email'])
    invalidate_list_version('members', member.id)


def invalidate_content(content):
    _invalidate_obj_cache('contents', content)
    invalidate_list_version('contents', content.id)
    
    if content.parent:               # If content has parent
        #invalidate_content(content.parent) # Refreshes parent, this is potentialy overkill for just updateing a reposnse tilte, responses will happen so in-frequently that this isnt a problem for now
        # dissasociate has code to separately update the parent, could thoese lines be ignored?
        pass
