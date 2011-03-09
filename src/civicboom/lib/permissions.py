from decorator import decorator

from pylons import tmpl_context as c, url
from pylons.controllers.util  import redirect

import civicboom.lib.errors as errors

from civicboom.model.member import has_role_required as has_role_required


def account_type(required_account_type):
    """
    Check if logged in user has paid for the services reuqired
    If not sends you to a upgrade account page (if html or redirect) or riase api error
    """
    @decorator
    def wrapper(_target, *args, **kwargs):
        if c.logged_in_persona.has_permission(required_account_type):
            result = _target(*args, **kwargs)
            return result
        
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
    

def raise_if_current_role_insufficent(role_required):
    if has_role_required(role_required, c.logged_in_persona_role):
        return
    raise errors.error_role()
