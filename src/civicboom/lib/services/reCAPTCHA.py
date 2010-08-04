import recaptcha.client.captcha as librecaptcha

from pylons import config   #, tmpl_context as c

from webhelpers.html import literal

"""
References
http://pypi.python.org/pypi/recaptcha-client
http://www.google.com/recaptcha
http://code.google.com/apis/recaptcha/intro.html

http://k0001.wordpress.com/2007/11/15/using-recaptcha-with-python-and-django/
"""

def get_captcha(lang='en', theme='white'):
    """
    Generate reCAPTCHA html
    (currently the python-recaptcha API does not support the lang or theme option, but these are fields in the html, maybe we need a modifyed version, see the django example for more info)
    """
    return literal(librecaptcha.displayhtml(config['api_key.reCAPTCHA.public'])) #, lang="es", theme='white'

#state should be set to request.environ
from formencode.validators import FormValidator
class CaptchaValidator(FormValidator):
    def validate_python(self, field_dict, state):
        try:
            response  = field_dict['recaptcha_response_field']
            challenge = field_dict['recaptcha_challenge_field']
        except:
            raise Invalid(_('reCAPTCHA fields not present in form'), field_dict, state)

        recaptcha_response = librecaptcha.submit(challenge, response, config['api_key.reCAPTCHA.private'], state['REMOTE_ADDR']) #request.environ['SERVER_ADDR'] ? our server address or the clients ip address?
        if recaptcha_response.is_valid:
            return True
        else:
            raise formencode.Invalid(_('reCAPTURE failed to validate %s ') % recaptcha_response.error_code, value, state)