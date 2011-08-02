from civicboom.lib.base import *
from civicboom.model import User, Group, PaymentAccount

import time

log      = logging.getLogger(__name__)


class PaymentsController(BaseController):
    """
    @title Payments
    @doc payment
    @desc controller for administering payment accounts
    """
    
    @web
    @authorize
    def index(self, **kwargs):
        """
        GET /groups: All groups the current user is a member of
        @api groups 1.0 (WIP)
        @param * (see common list return controls)
        @return 200 - data.list = array of group objects that logged in user is a member including the additional field 'members "role" in the group'
        """
        # url('payments')
        
        raise_if_current_role_insufficent('admin', group=c.logged_in_persona)
        
        if not c.logged_in_persona.payment_account:
            raise action_error(_('There is no payment account associated with this user, please contact us if you wish to set up a payment account'), code=404)
        
        account = c.logged_in_persona.payment_account

        return self.show(account.id)
    
    @web
    @authorize
    def new(self, **kwargs):
        """
        """
        #url_for('new_payment')
        return action_ok()

    @web
    @auth
    def create(self, **kwargs):
        """
        """
        # url('payments') + POST
        return action_ok()

    @web
    @auth
    def update(self, id, **kwargs):
        """
        """
        # url('payment', id=ID)
        return action_ok()
    
    @web
    @auth
    def delete(self, id, **kwargs):
        """
        """
        # url('payment', id=ID)
        return action_ok()
    
    @web
    @authorize
    def show(self, id, **kwargs):
        """
        """
        raise_if_current_role_insufficent('admin', group=c.logged_in_persona)
        
        account = Session.query(PaymentAccount).filter(PaymentAccount.id == id).first()
        
        if not account:
            raise action_error(_('Payment account does not exist'), code=404)
        
        if not c.logged_in_persona in account.members:
            raise action_error(_('You do not have permission to view this account'), code=404)
        
        data = {
            'account_id':       account.id,
            'account_type':     account.type,
            'billing_status':   account.billing_status,
            'members':          [member.to_dict() for member in account.members],
            'invoices':         [invoice.to_dict() for invoice in account.invoices],
            #'billing_accounts': [billing.to_dict() for billing in account.billing_accounts]
            }
        return action_ok(code=200, data=data)
