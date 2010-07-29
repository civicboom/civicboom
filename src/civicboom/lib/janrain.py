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

def janrain(method, **kargs):
    """
    Make Janrain API calls from python - more info for each call at https://rpxnow.com/docs
    """
    kargs['apiKey'] = config['janrain.api_key']
    kargs['format'] = 'json'
    http_response  = urllib2.urlopen('https://rpxnow.com/api/v2/'+method, urllib.urlencode(kargs))
    janrain_python = json.loads(http_response.read())
    if janrain_python['stat'] != 'ok':
        log.error(janrain_python['err']['msg'])
        return None
    return janrain_python