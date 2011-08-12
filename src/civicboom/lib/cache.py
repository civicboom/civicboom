
_cache = {}

def init_cache(config):
    from beaker.cache import CacheManager
    from beaker.util import parse_cache_config_options
    cache_manager = CacheManager(**parse_cache_config_options(config))
    
    if config['beaker.cache.enabled']:
        for region in ['contents_index', 'members_index', 'content_show', 'members_show']: #'members', 'contents', 
            _cache[region] = cache_manager.get_cache(region)
            #if config['development_mode']:
            _cache[region].clear()
