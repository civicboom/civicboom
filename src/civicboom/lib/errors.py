"""
Consistant action_error type returns
"""

from civicboom.lib.web import action_error

account_level = action_error(
            status   = 'error' ,
            code     = 403 ,
            message  = _('operation requires account upgrade') ,
            data     = data ,
        )
