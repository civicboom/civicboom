"""
Janrain Engage - http://documentation.janrain.com/
Python wrapper for Janrain API calls
"""

from pylons import config

import urllib
import urllib2
import json

import logging
log = logging.getLogger(__name__)

service_url = 'https://rpxnow.com/api/v2/'


def janrain(method, **kwargs):  # pragma: no cover - online services aren't active in test mode
    """
    Make Janrain API calls from python - more info for each call at https://rpxnow.com/docs
    """
    if 'apiKey' not in kwargs:
        kwargs['apiKey'] = config['api_key.janrain']
    kwargs['format'] = 'json'
    
    try:
        http_response  = urllib2.urlopen(service_url+method, urllib.urlencode(kwargs), timeout=10)
        janrain_python = json.loads(http_response.read())
        http_response.close()
    except:
        log.error('network error')
        return None
    
    if janrain_python['stat'] != 'ok':
        log.error(janrain_python['err']['msg'])
        #print janrain_python['err']['msg']
        return None
    return janrain_python
