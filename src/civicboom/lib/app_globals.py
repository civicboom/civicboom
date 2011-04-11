"""The application's Globals object"""

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

from pylons import config
from pylons.i18n.translation  import _


from paste.deploy.converters import asbool

import redis
from ConfigParser import SafeConfigParser

import os


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

        if os.path.exists(".version"):
            self.version   = file(".version").read().strip()
        else:  # pragma: no cover - all released versions have a version
            self.version   = None

        self.cache         = CacheManager(**parse_cache_config_options(config))
        self.cache_enabled = asbool(config['beaker.cache.enabled']) # Also used by lib.database

        self.cache         = redis.Redis(config['service.redis.server'], db=1)

        self.user_defaults = SafeConfigParser()
        self.user_defaults.read("user_defaults.ini")

        self.subdomains = {
            ''      : 'web'    ,
            'www'   : 'web'    ,
            'widget': 'widget' ,
            #'w'     : 'widget' ,
            #'mobile': 'mobile' ,
            'm'     : 'mobile' ,
            'api-v1': 'api'    ,
        }
