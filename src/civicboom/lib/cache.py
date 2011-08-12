
_cache = {} # Global dictionary that is imported by submodule, contins the cache buckets

def init_cache(config):
    from beaker.cache import CacheManager
    from beaker.util import parse_cache_config_options
    cache_manager = CacheManager(**parse_cache_config_options(config))
    
    if config['beaker.cache.enabled']:
        for bucket in ['contents_index', 'members_index', 'content_show', 'members_show']: #'members', 'contents', 
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


def is_cacheable(bucket, **kwargs):
    """
    Take args for an index action and return
      - False if not cachable
      >0 of etag count for this cacheable item
      
    ignoring  keys starting with '_'
    """
    #app_globals.memcache.get
    pass


def invalidate(region, identifyer, id):
    pass
