"""The application's Globals object"""

#from pylons import config
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

from pylons import config

from paste.deploy.converters import asbool


class Globals(object):

  """Globals acts as a container for objects available throughout the
  life of the application
  
  """

  def __init__(self, config):
    """One instance of Globals is created during application
    initialization and is available during requests via the
    'app_globals' variable

    """
    
    self.cache         = CacheManager(**parse_cache_config_options(config))
    self.cache_enabled = asbool(config['beaker.cache.enabled'])

    self.development_mode = config['debug']
    
    self.site_name        = config['text.site_name']
    self.site_description = config['text.site_description']
    self.tagline          = config['text.tagline']
    self.email_contact    = config['email.contact']
    self.terminology      = eval(config['text.terminology']) #AllanC - Security!? is this safe? as this value comes from the server cfg file and is just a dictonary I am happy to use eval here. terminolgy is a dictonary of terms

    self.feature_agregate_twitter   = asbool(config['feature.aggregate.twitter'])
    self.feature_agregate_email     = asbool(config['feature.aggregate.email'])
    self.feature_profanity_filter   = asbool(config['feature.profanity_filter'])
    
