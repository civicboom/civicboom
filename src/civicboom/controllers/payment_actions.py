"""
Group Actions
"""

from civicboom.lib.base import *
from civicboom.model import PaymentAccount, Invoice, InvoiceLine, BillingAccount, BillingTransaction
#from civicboom.controllers.groups import _get_group

log      = logging.getLogger(__name__)



class PaymentActionsController(BaseController):
    
    @web
    @auth
    def member_remove(self, id, **kwargs):
        """
        """
        # url('payment', id=ID)
        
        raise_if_current_role_insufficent('admin', group=c.logged_in_persona)
        
        account = Session.query(PaymentAccount).filter(PaymentAccount.id == id).first()
        
        if not account:
            raise action_error(_('Payment account does not exist'), code=404)
        
        if not c.logged_in_persona in account.members:
            raise action_error(_('You do not have permission to view this account'), code=404)
        
        username = kwargs.get('username')
        
        member = get_member(username)
        
        if not member:
            raise action_error(_('The user does not exist'), code=404)
        
        if not account.member_remove(member):
            raise action_error(_('Member not in this payment account'), code=404)
        
        return action_ok()
    
    @web
    @auth
    def member_add(self, id, **kwargs):
        """
        """
        # url('payment', id=ID)
        
        raise_if_current_role_insufficent('admin', group=c.logged_in_persona)
        
        account = Session.query(PaymentAccount).filter(PaymentAccount.id == id).first()
        
        if not account:
            raise action_error(_('Payment account does not exist'), code=404)
        
        if not c.logged_in_persona in account.members:
            raise action_error(_('You do not have permission to view this account'), code=404)
        
        new_user = get_member(kwargs.get('username'))
        
        if not new_user:
            raise action_error(_('The user does not exist'), code=404)
        
        if not account.member_add(new_user):
            raise action_error(_('User is already associated with a payment account'), code=404)
        
        return action_ok()
    
    @web
    @authorize
    def invoice(self, id, **kwargs):
        """
        """
        
        invoice_id = kwargs.get('invoice_id')
        
        raise_if_current_role_insufficent('admin', group=c.logged_in_persona)
        account = Session.query(PaymentAccount).filter(PaymentAccount.id == id).first()
        if not account:
            raise action_error(_('Payment account does not exist'), code=404)
        if not c.logged_in_persona in account.members:
            raise action_error(_('You do not have permission to view this account'), code=404)
        
        invoice = Session.query(Invoice).filter(Invoice.id==invoice_id and Invoice.payment_account_id==account.id).one()
        
        if not invoice or invoice.status not in ['billed', 'paid']:
            raise action_error(_('This invoice does not exist'), code=404)
        
        data = invoice.to_dict(list_type='full')
        
        return action_ok(code=200, data=data)
    