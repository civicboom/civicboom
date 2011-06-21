"""
Tools for the generation, managment and invalidation of eTags
"""
from pylons import request, session, tmpl_context as c, app_globals
from pylons.controllers.util import etag_cache

import hashlib


import logging
log = logging.getLogger(__name__)
#-------------------------------------------------------------------------------

# List of dependencys to keep in memory
etag_keys = {} #"assignment":{}, "article":{}, "member_articles":{}, "member":{}, "member_assignments_active":{}, "member_messages":{}, "member_assignments_accepted":{},"syndication_list":{}
# AllanC: TODO this should be in memcache and not a python array, 1.) memcache expires (useful under heavy load) 2.) memcahce state remains after a python restart if needed


def add_etag_dependency_key(dependecy_key):
    etag_keys[dependecy_key] = {}


#-------------------------------------------------------------------------------

def etag_key_incement(key, value):
    """
    eTags can be invalidated
    to be called when an object is commited to the database and requires the tag to be updated
    e.g.
    """
    value    = str(value)
    etag_key = etag_keys[key]
    if value in etag_key:
        etag_key[value] += 1
    else:
        etag_key[value]  = 0


#-------------------------------------------------------------------------------

def gen_cache_key(**kargs):
    """
    eTags are generated for a page depending on the pages known dependancys
    e.g.
      cache_key = gen_cache_key(member=c.widget_member.id, assignment=id)  #if the etag is dependent on content of the listed member and listed assingnment
    """
    def getsafe_current_username():
        if c.logged_in_persona:
            return c.logged_in_persona.username
        return ""

    def getsafe_flash_message():
        #if 'flash_message' in session: return session['flash_message']
        return ""

    cache_key = app_globals.version + request.environ.get('PATH_INFO') + request.environ.get('QUERY_STRING') + getsafe_current_username() + getsafe_flash_message()
    #for arg in args:
    #  dependecys+=arg
    for key in kargs:
        #if key in etag_keys: #Unnessisary as if the code is using a non setup tag then it's wrong damn it!
        etag_key   = etag_keys[key]
        seek_value = str(kargs[key])
        if seek_value in etag_key:
            cache_key+=str(etag_key[seek_value])+"-"
        else:
            cache_key+=                         "X-"
    if not app_globals.cache_enabled:
        log.debug('Cache disabled: eTag hash generated from: %s' % cache_key)
    cache_key = hashlib.md5(cache_key).hexdigest()
    if app_globals.cache_enabled:
        etag_cache(cache_key)
    return cache_key
