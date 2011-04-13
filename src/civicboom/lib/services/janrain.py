"""
Janrain Engage - http://www.janrain.com/products/engage
Python wrapper for Janrain API calls
"""

from pylons import config

import urllib
import urllib2
import json

import logging
log = logging.getLogger(__name__)

service_url = 'https://rpxnow.com/api/v2/'


def janrain(method, **kargs):  # pragma: no cover - online services aren't active in test mode
    """
    Make Janrain API calls from python - more info for each call at https://rpxnow.com/docs
    """
    kargs['apiKey'] = config['api_key.janrain']
    kargs['format'] = 'json'
    
    try:
        http_response  = urllib2.urlopen(service_url+method, urllib.urlencode(kargs), timeout=10)
        janrain_python = json.loads(http_response.read())
        http_response.close()
    except:
        log.error('network error')
        return None
    
    if janrain_python['stat'] != 'ok':
        log.error(janrain_python['err']['msg'])
        return None
    return janrain_python
