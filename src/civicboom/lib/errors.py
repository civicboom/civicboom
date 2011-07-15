"""
Consistant action_error type returns
"""
from pylons.i18n.translation  import _

from civicboom.lib.web import action_error


def error_view_permission():
    return action_error(
            status   = 'error' ,
            code     = 403 ,
            message  = _('The _content you requested is not viewable') ,
        )


#@property
def error_account_level():
    return action_error(
            status   = 'error' ,
            code     = 402 ,
            message  = _('operation requires account upgrade') ,
        )


#@property
def error_role():
    return action_error(
            status   = 'error' ,
            code     = 403 ,
            message  = _('current persona does not posses the role required to perform this operation') ,
        )


def error_age():
    return action_error(
            status   = 'error' ,
            code     = 403 ,
            message  = _('current user is not a suitable age to perform this operation') ,
        )
