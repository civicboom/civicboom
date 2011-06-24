from decorator import decorator

from pylons import tmpl_context as c

import civicboom.lib.errors as errors

from civicboom.model.member             import has_role_required as has_role_required


from cbutils.misc                 import calculate_age
from civicboom.lib.form_validators.base import IsoFormatDateConverter
api_datestr_to_datetime = IsoFormatDateConverter().to_python
#from civicboom.lib.helpers import api_datestr_to_datetime #This is not suffience because some of the DOB's are not in API form. We may need to normaliz this in future

import logging
log = logging.getLogger(__name__)


def account_type(required_account_type):
    """
    Check if logged in user has paid for the services reuqired
    If not sends you to a upgrade account page (if html or redirect) or riase api error
    """
    @decorator
    def wrapper(_target, *args, **kwargs):
        #print "user: %s account: %s required: %s" % (c.logged_in_persona.username, c.logged_in_persona.account_type, required_account_type)
        if c.logged_in_persona.has_account_required(required_account_type):
            result = _target(*args, **kwargs)
            return result
        # user_log.info('Insufficent prvilages for - %s-%s-%s' % (c.controller, c.action, c.id)) # AllanC - unneeded as we log all errors in @auto_format_output now
        # The auto formater will redirect to the upgrade account page on account_level errors
        raise errors.error_account_level()
    
    return wrapper


def role_required(role_required):
    """
    lock controller actions to require certan permissions
    users always have full rights. checks the c.logged_in_persona_role
    
    this is always called after authroize (listed above)
    """
    @decorator
    def wrapper(_target, *args, **kwargs):
        raise_if_current_role_insufficent(role_required)
        result = _target(*args, **kwargs)
        return result
    
    return wrapper


def age_required(age_required):
    """
    Decorator to protect actions with an age limit
    """
    age_required = int(age_required)
    
    @decorator
    def wrapper(_target, *args, **kwargs):
        if c.logged_in_persona.config.get('dob'):
            dob_str = c.logged_in_persona.config.get('dob')
            age     = age_required
            try:
                age = calculate_age(api_datestr_to_datetime(dob_str))
            except:
                log.warn('tryed to convert member.config[dob] to datetime and failed for user %s, please investigate: %s' % (c.logged_in_persona.username, dob_str))
            if age < age_required:
                raise errors.error_age()
        result = _target(*args, **kwargs)
        return result
    
    return wrapper

    

def raise_if_current_role_insufficent(role_required, group=None):
    if not group or (group and group == c.logged_in_persona):
        if has_role_required(role_required, c.logged_in_persona_role):
            return
    raise errors.error_role()
