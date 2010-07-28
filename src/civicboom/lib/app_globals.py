"""The application's Globals object"""

#from pylons import config
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

from pylons import config

from paste.deploy.converters import asbool

from civicboom.model.content           import License
from civicboom.model.meta              import Session

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

        self.user_defaults = SafeConfigParser()
        self.user_defaults.read("user_defaults.ini")

        #self.development_mode = config['debug']

        # Setup paths dictonary
        #self.path = {}
        #for p in ["temp"]:
        #    self.path[p] = config['path.'+p]


    def load_database_globals(self):
        """
        Base database objects cannot be loaded into memory on __init__ as the database model has not been setup
        this method call is activated after initial setup
        """
        self.licenses = Session.query(License).all()