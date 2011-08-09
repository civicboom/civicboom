"""
  Cache
 
  Consolidate all cache methods and utils here
  
  Reference:
    - http://www.sqlalchemy.org/trac/browser/examples/beaker_caching/environment.py
"""

from beaker import cache
import os
import time

import caching_query


# Beaker CacheManager.  A home base for cache configurations.
cache_manager = cache.CacheManager()

cache_folder = "./data/cache/beaker_test"

if not os.path.exists(cache_folder):
    os.makedirs(cache_folder)

# configure the "default" cache region.
cache_manager.regions['default'] ={
    'type'      : 'file' , # using type 'file' to illustrate serialized persistence.  In reality, use memcached.   Other backends are much, much slower.
    'data_dir'  : cache_folder ,
    'expire'    : 3600 ,
    'start_time': time.time() , # set start_time to current time to re-cache everything upon application startup
}