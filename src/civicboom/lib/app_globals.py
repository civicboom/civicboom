"""The application's Globals object"""

#from pylons import config
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

from pylons import config


class Globals(object):

  """Globals acts as a container for objects available throughout the
  life of the application
  
  """

  def __init__(self, config):
    """One instance of Globals is created during application
    initialization and is available during requests via the
    'app_globals' variable

    """
    
    self.cache = CacheManager(**parse_cache_config_options(config))

    self.development_mode = True #AllanC - to be moved to config ASAP
    
    # AllanC - Placeholders for config globals
    #site_name        = config['site_name']
    #site_description = "Building the world's first true community and audience assignment system"
    #email_contact    = config['email_contact']
    #terminology      = config['terminology']
