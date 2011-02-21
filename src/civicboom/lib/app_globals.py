"""The application's Globals object"""

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

from pylons import config
from pylons.i18n.translation  import _


from paste.deploy.converters import asbool

import memcache
from ConfigParser import SafeConfigParser



class Globals(object):
    """
    Globals acts as a container for objects available throughout the
    life of the application
    """

    def __init__(self, config):
        """
        One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable
        """

        self.version       = "temp string" #Needs to be replaced with version hash of this git build

        self.cache         = CacheManager(**parse_cache_config_options(config))
        self.cache_enabled = asbool(config['beaker.cache.enabled']) # Also used by lib.database

        self.memcache      = memcache.Client(config['service.memcache.server'].split(), debug=0)

        self.user_defaults = SafeConfigParser()
        self.user_defaults.read("user_defaults.ini")

        self.subdomains = {
            ''      : 'web'    ,
            'www'   : 'web'    ,
            'widget': 'widget' ,
            'w'     : 'widget' ,
            'mobile': 'mobile' ,
            'm'     : 'mobile' ,
            'api-v1': 'api'    ,
        }

