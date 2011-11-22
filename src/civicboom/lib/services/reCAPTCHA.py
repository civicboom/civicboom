"""
reCAPTCHA - http://www.google.com/recaptcha
Python wrapper for reCAPTCHA
"""

from pylons import config

import urllib
import urllib2

import logging
#log = logging.getLogger(__name__)
user_log = logging.getLogger("user")

service_url = 'https://www.google.com/recaptcha/api/'


#                    'remoteip' :  encode_if_necessary(request.environ['REMOTE_ADDR']),
#                    'challenge':  encode_if_necessary(kwargs['recaptcha_challenge_field']),
#                    'response' :  encode_if_necessary(kwargs['recaptcha_response_field']),

lazy_html        = None
lazy_private_key = None


def reCAPTCHA_html(lang='en', theme='red'):
    global lazy_html
    if not lazy_html:
        lazy_html = """
<script type="text/javascript" src="%(service_url)schallenge?k=%(public_key)s"></script>
<noscript>
   <iframe src="%(service_url)snoscript?k=%(public_key)s" height="300" width="500" frameborder="0"></iframe><br>
   <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
   <input type="hidden" name="recaptcha_response_field" value="manual_challenge">
</noscript>
""" % {'public_key': config['api_key.reCAPTCHA.public' ], 'service_url': service_url}
    return '<script type="text/javascript">var RecaptchaOptions={theme:"%(theme)s", lang:"%(lang)s", tabindex:"0", custom_theme_widget:"null"};</script>' % {'lang':lang, 'theme':theme} + lazy_html



def reCAPTCHA(method, **kwargs):
    """
    Make reCAPTCHA API calls from python
    """
    global lazy_private_key
    if not lazy_private_key:
        lazy_private_key = config['api_key.reCAPTCHA.private']
    kwargs['privatekey'] = lazy_private_key
    
    for i in range(2):
        try:
            http_response        = urllib2.urlopen(service_url+method, urllib.urlencode(kwargs), timeout=10)
            reCAPTCHA_response   = http_response.read().splitlines()
            http_response.close()
            return reCAPTCHA_response
        except Exception as e:
            user_log.error('reCAPTCHA network_failure: %s' % e)
    return None


def reCAPTCHA_verify(**kwargs):
    reCAPTCHA_response = reCAPTCHA('verify', **kwargs)
    
    if not reCAPTCHA_response:
        #return 'recaptcha-not-reachable'
        return True # AllanC - this was included because we dont want users being rejected if we cant contact Google. This should be reinstated later
    
    if reCAPTCHA_response[0] == 'true':
        return True
    
    error = reCAPTCHA_response[1]
    if error not in ['incorrect-captcha-sol']:
        user_log.error(error) # Log real errors
    return error
