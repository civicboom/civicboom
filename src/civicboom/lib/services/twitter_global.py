"""
Twitter -
Global status update for Civicboom - (this is a piss poor solution, but it works for now)

Uses - Python Twitter Tools - http://mike.verdone.ca/twitter/
"""

from twitter.api import Twitter, TwitterError
from twitter.oauth import OAuth

import logging
log = logging.getLogger(__name__)


def status(**kargs):
    from cbutils.worker import config as w_config
    from pylons import config as p_config
    t = Twitter(
        auth=OAuth(
            w_config.get('api_key.twitter.oauth_token',
                p_config.get('api_key.twitter.oauth_token')),
            w_config.get('api_key.twitter.oauth_token_secret',
                p_config.get('api_key.twitter.oauth_token_secret')),
            w_config.get('api_key.twitter.consumer_key',
                p_config.get('api_key.twitter.consumer_key')),
            w_config.get('api_key.twitter.consumer_secret',
                p_config.get('api_key.twitter.consumer_secret'))
        ),
        secure=True, #options['secure']
        api_version='1',
        domain='api.twitter.com'
    )
    kargs['status'] = kargs['status'].encode('utf8', 'replace')
    #log.warn('global twitter disabled')
    t.statuses.update(**kargs)

# Old custom ideas
"""

import urllib
import urllib2
import json


service_url = 'http://api.twitter.com/1/'

methods = {update:"statuses/update"}
format  = 'json'

def twitter(method, **kargs):

    #Make Twitter API calls from python - more info for each call at

    #kargs['apiKey'] = config['api_key.twitter']
    
    http_response  = urllib2.urlopen(service_url+methods[method]+"."+format, urllib.urlencode(kargs))
    twitter_python = json.loads(http_response.read())
    if twitter_python['stat'] != 'ok':
        log.error(twitter_python['err']['msg'])
        return None
    return twitter_python
"""
