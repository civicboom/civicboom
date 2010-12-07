from decorator import decorator

from pylons import tmpl_context as c, url
from pylons.controllers.util  import redirect

import civicboom.lib.errors as errors


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
        raise errors.account_level
    
    return wrapper