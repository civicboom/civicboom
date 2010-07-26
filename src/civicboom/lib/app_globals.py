"""The application's Globals object"""

#from pylons import config
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

from pylons import config

from paste.deploy.converters import asbool


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

        if 'warehouse_url' in config:
            self.warehouse_url = config['warehouse_url']

        self.development_mode = config['debug']

        self.email_contact    = config['email.contact']

        self.feature_agregate_twitter   = asbool(config['feature.aggregate.twitter'])
        self.feature_agregate_email     = asbool(config['feature.aggregate.email'])
        self.feature_profanity_filter   = asbool(config['feature.profanity_filter'])

        # Setup paths dictonary
        self.path = {}
        for p in ["temp"]:
            self.path[p] = config['path.'+p]
          