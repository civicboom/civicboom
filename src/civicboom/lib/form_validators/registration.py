# Formencode
import formencode
from formencode import validators

from base import DefaultSchema, IsoFormatDateConverter

# Pylons Imports
from pylons.i18n.translation import _

# Database Objects
from civicboom.model.meta              import Session
from civicboom.model.member            import User, Member

# Other utils
from cbutils.misc           import calculate_age, make_username

# Other libs
#import recaptcha.client.captcha as librecaptcha
from civicboom.lib.services.reCAPTCHA import reCAPTCHA_verify

import re

import logging
log      = logging.getLogger(__name__)



#-------------------------------------------------------------------------------
# Individual Validators
#-------------------------------------------------------------------------------

class UniqueUsernameValidator(validators.FancyValidator):
    min =  4
    max = 32
    messages = {
        'too_few'       : _('Your username must be at least %(min)i characters'),
        'too_long'      : _('Your username must be shorter than %(max)i characters'),
        'username_taken': _('The username %(name)s is no longer available, please try a different one'),
        'illegal_chars' : _('Usernames may only contain alphanumeric characters or underscores'),
    }

    def _to_python(self, value, state):
        value = make_username(unicode(value.strip()))
        if not re.search("^[\w-]*$", value):
            raise formencode.Invalid(self.message("illegal_chars", state,), value, state)
        if len(value) < self.min:
            raise formencode.Invalid(self.message("too_few", state, min=self.min), value, state)
        if len(value) > self.max:
            raise formencode.Invalid(self.message("too_long", state, max=self.max), value, state)
            
        from pylons import tmpl_context as c
        if c.logged_in_persona and c.logged_in_persona.username == value: # If the current user has this username then bypass the validator
            return value
        if Session.query(Member).filter(Member.username==value).count() > 0:
            raise formencode.Invalid(self.message("username_taken", state, name=value), value, state)
        return value


class UniqueEmailValidator(validators.Email):
    not_empty = True

    def __init__(self, *args, **kwargs):
        from pylons import config
        kwargs['resolve_domain'] = False
        if config['online']:
            kwargs['resolve_domain'] = True
        validators.Email.__init__(self, *args, **kwargs)

    def _to_python(self, value, state):
        value = unicode(value)
        from pylons import tmpl_context as c
        if c.logged_in_persona and c.logged_in_persona.email == value: # If the current user has this email then bypass the validator
            return value
        if Session.query(User).filter(User.email==value).count() > 0:
            raise formencode.Invalid(_('This email address is already registered with us. Please use a different address, or retrieve your password using the password recovery link.'), value, state)
        return value


#class MinimumAgeValidator(validators.FancyValidator):
#    """Checks that date is ok and doesn't allow under 16"""
#    age_min = 16
#    messages = {
#        'empty'       : _('Please enter a date of birth'),
#    }
#
#    def _to_python(self, value, state):
#         try:
#             import datetime
#             date = datetime.datetime.strptime(value, '%d/%m/%Y')
#         except ValueError:
#              raise formencode.Invalid(_("Please enter your date of birth with the format DD/MM/YYYY"), value, state)
#         if calculate_age(date) < self.age_min:
#              raise formencode.Invalid(_("Sorry, you have to be over %d to use this site") % self.age_min, value, state)
#         return date

class MinimumAgeValidator(IsoFormatDateConverter):
    """Checks that date is ok and doesn't allow under 16"""
    from pylons import config
    age_min = config['setting.age.min_signup'] #16
    messages = {
        'empty'        : _('Please enter a date of birth') ,
        'under_min_age': _("Sorry, you have to be over %d to use this site") % age_min,
    }

    def _to_python(self, value, state):
        date = super(MinimumAgeValidator, self)._to_python(value, state)
        if calculate_age(date) < self.age_min:
            raise formencode.Invalid(self.message('under_min_age', state), value, state)
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
        'network_failure' : _("unable to contact reCAPTCHA server to validate response, our admins have been notifyed"),
        'recapture_error' : _("reCAPTCHA server returned an error %(error_code)s, the problem has been logged and reported to _site_name"),
    }

    __unpackargs__ = ('*', 'field_names')
    validate_partial_form   = True
    validate_partial_python = None
    validate_partial_other  = None

    def __init__(self, remoteip, *args, **kw):
        super(ReCaptchaValidator, self).__init__(args, kw)
        self.remoteip = remoteip
        self.field_names = ['recaptcha_challenge_field',
                            'recaptcha_response_field']
    
    def validate_partial(self, field_dict, state):
        for name in self.field_names:
            if name not in field_dict:
                return
        #self.validate_python(field_dict, state)
        # AllanC . WTF!!! this partial validator was making the validator trigger twice!? seems to work now this is remmed

    def validate_python(self, field_dict, state):
        
        recaptcha_response = reCAPTCHA_verify(
            remoteip  = self.remoteip, #request.environ['REMOTE_ADDR'],
            challenge = field_dict['recaptcha_challenge_field'],
            response  = field_dict['recaptcha_response_field'],
        )
        
        if recaptcha_response == True:
            return True
        if recaptcha_response == 'incorrect-captcha-sol':
            error = formencode.Invalid(self.message('incorrect', state), field_dict, state)
            error.error_dict = {'recaptcha_response_field':self.message('incorrect', state)}
            raise error
        if recaptcha_response == 'recaptcha-not-reachable':
            raise formencode.Invalid(self.message('network_failure', state), field_dict, state)
        raise formencode.Invalid(self.message('recapture_error', state, error_code=recaptcha_response), field_dict, state)


#-------------------------------------------------------------------------------
# Schemas
#-------------------------------------------------------------------------------

class RegisterSchemaEmailUsername(DefaultSchema):
    username  = UniqueUsernameValidator(not_empty=True)
    email     = UniqueEmailValidator   (not_empty=True)
