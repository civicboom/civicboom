cache_separator = ':'

_cache = {} # Global dictionary that is imported by submodule, contins the cache buckets

def init_cache(config):
    from beaker.cache import CacheManager
    from beaker.util import parse_cache_config_options
    cache_manager = CacheManager(**parse_cache_config_options(config))
    
    if config['beaker.cache.enabled']:
        for bucket in ['members', 'contents', 'contents_index', 'members_index', 'content_show', 'members_show']: #
            _cache[bucket] = cache_manager.get_cache(bucket)
            #if config['development_mode']:
            _cache[bucket].clear()


cacheable_lists = {
    'contents_index': {
        'content'     : {'creator': None},
        'boomed_by'   : {'boomed_by': None},
        'drafts'      : {'list':'drafts'     , 'creator':None},
        'articles'    : {'list':'articles'   , 'creator':None},
        'assignments' : {'list':'assignments', 'creator':None},
        'responses'   : {'list':'responses'  , 'creator':None},
        'responses_to': {'response_to': None},
        #'comments' : {} # AllanC - todo - comments should come from index?
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
    }
}

def normalize_kwargs_for_cache(kwargs):
    """
    do not allow db objects to be used as params
    """
    for key, value in kwargs.iteritems():
        if not key.startswith('_'): # skip keys beggining with '_' as these have already been processed
            #try   : value = value.__db_index__() # AllanC if it has an id use it. This should work for all db objects and not require the __db_index__ function
            try   : value = value.id
            except: pass
            # AllanC: Suggestion - do we want to allow primitive types to pass through, e.g. int's and floats, maybe dates as well?
            value = str(value).strip()
        kwargs[key] = value
    return kwargs


def _gen_list_key(bucket, cacheable_list_name, cacheable_variables):
    if isinstance(cacheable_variables, list):
        cacheable_variables = ",".join(cacheable_variables)
    if not isinstance(cacheable_variables, basestring):
        cacheable_variables = str(cacheable_variables)
    return cache_separator.join(['cache', bucket, cacheable_list_name, cacheable_variables])

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
    

def get_cache_key(bucket, kwargs, normalize_kwargs=False):
    """
    Take args for an index action and return
      - '' if not cachable
      - 'xxx tag string xxx' if cachable
      
    ignoring  keys starting with '_' but still using these keys as part of the eTag generation
    
    Checks if the kwargs match the know cachable lists in cacheable_index
    
    it is assumed that kwargs have be pre-processed with 'normalize_kwargs_for_cache', a param is included to do this without the need to call the normalize function specifically
    
    will return and empty string if this item is not cacheable
    """
    
    cache_key = ''
    
    if normalize_kwargs:
        kwargs = normalize_kwargs_for_cache(kwargs)
    
    cacheable_kwargs_keys = [k for (k,v) in kwargs.iteritems() if not k.startswith('_')]  # Strip the keys starting with '_' as they are not needed. We need to preserve the kwargs for later as the _logged_in and _private are going to form part of the cache key
    cacheable_kwargs_keys.sort()
    
    # Iterate through all the 
    for cacheable_list_name, cache_args_dict in cacheable_lists[bucket].iteritems():
        if len(cache_args_dict) != len(cacheable_kwargs_keys): # Optimisation - no point in deeply comparing a list of args that dont match
            continue
        
        # Try to match the passed kwargs with the cacheable known lists
        #cacheable_list_name = cache_name
        cacheable_variables = []
        for key in cacheable_kwargs_keys: # Iterate over kwargs keys to see if they match the cacheable list
            key_match = key in cache_args_dict
            if   key_match and not cache_args_dict[key]: # if the value stored in the cache_args_dict is None then that key is a variable and can be added to the variable list
                cacheable_variables.append(kwargs[key])
            elif key_match and     cache_args_dict[key] and cache_args_dict[key]==kwargs[key]: # If the key exisits in cachable_list and the key value is NOT null - then check the value of the keys match
                continue # if the key values match then proceed to check the remaining key values
            else:
                cacheable_list_name = None
                break # If the kwargs contains an arg that isnt in the cacheable list, this item is not cacheable - proceed to check the other lists
        
        # After the for look has run though all the keys, and has not aborted to the next item with continue - the kwargs match this cacheable_list
        if cacheable_list_name:
            list_version = get_list_version(bucket, cacheable_list_name, cacheable_variables)
            
            # Sort keys to normaize the cache_key that is generated
            keys_sorted = [k for k in kwargs.keys()]
            keys_sorted.sort()
            
            # Append all kwarg values and list version number into one string tag to idnetify this cacheable item
            cache_values  = [str(kwargs[key]) for key in keys_sorted]
            cache_values += [str(list_version)]
            cache_key = cache_separator.join(cache_values)
            
            break # There is no need to check any more lists - as we have matched a chacheable item and no other will match
        
    return cache_key
