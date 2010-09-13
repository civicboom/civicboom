# Formencode
import formencode
from formencode import validators, compound

from base import DefaultSchema

# Pylons Imports
from pylons.i18n.translation import _

# Database Objects
from civicboom.model.meta              import Session
from civicboom.model.member            import User, Member

# Other utils
from civicboom.lib.misc           import calculate_age

# Other libs
import recaptcha.client.captcha as librecaptcha
import datetime

import logging
log      = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# Individual Validators
#-------------------------------------------------------------------------------

class UniqueUsernameValidator(validators.FancyValidator):
    min =  4
    max = 32
    messages = {
        'too_few'       : _('Your username must be longer than %(min)i characters'),
        'too_long'      : _('Your username must be shorter than %(max)i characters'),
        'username_taken': _('The username %(name)s is no longer available, please try a different one'),
        }
    def _to_python(self, value, state):
        value = unicode(value.strip())
        # TODO: Strip or alert any characters that make it non URL safe, see feature #54
        if len(value) <= self.min:
            raise formencode.Invalid(self.message("too_few", state, min=self.min), value, state)
        if len(value) >= self.max:
            raise formencode.Invalid(self.message("too_long", state, max=self.max), value, state)
        if Session.query(Member).filter(Member.username==value).count() > 0:
            raise formencode.Invalid(self.message("username_taken", state, name=value), value, state)
        return value

class UniqueEmailValidator(validators.Email):
    def __init__(self, resolve_domain=True, *args, **kwargs):
        kwargs.update(resolve_domain=True)
        validators.Email.__init__(self, *args, **kwargs)
    def _to_python(self, value, state):
        value = unicode(value)
        if Session.query(User).filter(User.email==value).count() > 0:
            raise formencode.Invalid(_('This email address is already registered with us. Please use a different address, or retrieve your password using the password recovery link.'), value, state)
        return value


class MinimumAgeValidator(validators.FancyValidator):
    """Checks that date is ok and doesn't allow under 16"""
    age_min = 16
    def _to_python(self, value, state):
         try:
             date = datetime.datetime.strptime(value, '%d/%m/%Y')
         except ValueError:
              raise formencode.Invalid(_("Please enter your date of birth with the format DD/MM/YYYY"), value, state)
         if calculate_age(date) < self.age_min:
              raise formencode.Invalid(_("Sorry, you have to be over %d to use this site") % self.age_min, value, state)
         return date


class ReCaptchaValidator(validators.FancyValidator):
    """    
    References
        http://toscawidgets.org/hg/tw.recaptcha/file/f846368854fe/tw/recaptcha/validator.py
        http://pypi.python.org/pypi/recaptcha-client
        http://www.google.com/recaptcha
    """
    
    messages = {
        'incorrect'       : _('reCAPTCHA field is incorrect'),
        'missing'         : _("Missing reCAPTCHA value."),
        'network_failure' : _("unable to contact reCAPTCHA server to validate response"),
        'recapture_error' : _("reCAPTCHA server returned an error %(error_code)s, the problem has been logged and reported to _site_name"),
    }

    __unpackargs__ = ('*', 'field_names')
    validate_partial_form   = True
    validate_partial_python = None
    validate_partial_other  = None

    def __init__(self, remote_ip, *args, **kw):
        super(ReCaptchaValidator, self).__init__(args, kw)
        self.remote_ip = remote_ip
        self.field_names = ['recaptcha_challenge_field',
                            'recaptcha_response_field']
    
    def validate_partial(self, field_dict, state):
        for name in self.field_names:
            if not field_dict.has_key(name):
                return
        self.validate_python(field_dict, state)

    def validate_python(self, field_dict, state):
        #print "reCAPTCHA validator"
        challenge = field_dict['recaptcha_challenge_field']
        response  = field_dict['recaptcha_response_field']
        if response == '' or challenge == '':
            error = formencode.Invalid(self.message('missing', state), field_dict, state)
            error.error_dict = {'recaptcha_response_field':'Missing value'}
            raise error

        from pylons import config
        #print "captcha validator call"
        print "IP:%s Chal:%s Resp:%s" % (self.remote_ip, challenge, response)
        recaptcha_response = librecaptcha.submit(challenge, response, config['api_key.reCAPTCHA.private'], self.remote_ip)

        if recaptcha_response and recaptcha_response.is_valid:
            return True
        if not recaptcha_response:
            error = formencode.Invalid(self.message('network_failure', state), field_dict, state)
            log.error(self.message('network_failure', state))
            raise error
        if recaptcha_response.error_code == 'incorrect-captcha-sol':
            print "Solution incorrect"
            error = formencode.Invalid(self.message('incorrect', state), field_dict, state)
            error.error_dict = {'recaptcha_response_field':self.message('incorrect', state)}
            raise error
        else:
            error = formencode.Invalid(self.message('recapture_error', state, error_code=recaptcha_response.error_code), field_dict, state)
            log.error('reCAPTCHA error %s' % recaptcha_response.error_code)
            raise error


#-------------------------------------------------------------------------------
# Schemas
#-------------------------------------------------------------------------------
    
class RegisterSchemaEmailUsername(DefaultSchema):
  username  = UniqueUsernameValidator(not_empty=True)
  email     = UniqueEmailValidator   (not_empty=True)
