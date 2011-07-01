from civicboom.lib.base import *
from civicboom.model import User, Group

import time

log      = logging.getLogger(__name__)

class PaymentsController(BaseController):
    """
    @title Payments
    @doc payment
    @desc controller for administering payment accounts
    """
    
    @web
    @auth
    def index(self, **kwargs):
        """
        GET /groups: All groups the current user is a member of
        @api groups 1.0 (WIP)
        @param * (see common list return controls)
        @return 200 - data.list = array of group objects that logged in user is a member including the additional field 'members "role" in the group'
        """
        user = c.logged_in_persona
        raise_if_current_role_insufficent('admin', group=user)
        
        if not c.logged_in_persona.payment_account:
            raise action_error(_('There is no payment account associated with this user, please contact us if you wish to setup a payment account'), code=404)
        
        account = user.payment_account
        
        data = {
            'account_id':   account.id,
            'account_type': account.type,
            'members':      [member.username for member in account.members],
            }
        return action_ok(code=200, data=data, template="account/payment")
    
    @web
    @auth
    def show(self):
        return action_ok()
    
    @web
    @auth
    def create(self):
        return action_ok()
    
    @web
    @auth
    def create(self):
        return action_ok()
    
    @web
    @auth
    def delete(self):
        return action_ok()