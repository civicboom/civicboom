"""
Consistant action_error type returns
"""
from pylons.i18n.translation  import _

from civicboom.lib.web import action_error

account_level = action_error(
            status   = 'error' ,
            code     = 402 ,
            message  = _('operation requires account upgrade') ,
        )
