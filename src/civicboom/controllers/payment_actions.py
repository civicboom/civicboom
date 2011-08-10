"""
Group Actions
"""

from civicboom.lib.base import *
import civicboom.lib.helpers as h
from sqlalchemy           import or_, and_, null
#from civicboom.lib.payment.paypal import express_checkout_single_auth, express_checkout_get_details
from civicboom.model import PaymentAccount, Invoice, InvoiceLine, BillingAccount, BillingTransaction
from civicboom.lib.payment.paypal import *
import civicboom.lib.payment.api_calls as api_calls
#from civicboom.controllers.groups import _get_group

log      = logging.getLogger(__name__)

paypal_config = PayPalConfig(
    API_USERNAME  = config['api_key.paypal.username'],
    API_PASSWORD  = config['api_key.paypal.password'],
    API_SIGNATURE = config['api_key.paypal.signature'],
    DEBUG_LEVEL   = 0)

paypal_interface = PayPalInterface(config=paypal_config)

class PaymentActionsController(BaseController):
        
    @web
    @auth
    @role_required('admin')
    def member_remove(self, id, **kwargs):
        """
        """
        # url('payment', id=ID)
        
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
    @role_required('admin')
    def member_add(self, id, **kwargs):
        """
        """
        # url('payment', id=ID)
        
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
    @role_required('admin')
    def invoice(self, id, **kwargs):
        """
        """
        
        invoice_id = kwargs.get('invoice_id')
        
        account = Session.query(PaymentAccount).filter(PaymentAccount.id == id).first()
        if not account:
            raise action_error(_('Payment account does not exist'), code=404)
        if not c.logged_in_persona in account.members:
            raise action_error(_('You do not have permission to view this account'), code=404)
        
        invoice = Session.query(Invoice).filter(and_(Invoice.id==invoice_id, Invoice.payment_account_id==account.id)).first()
        
        if not invoice or invoice.status not in ['billed', 'paid']:
            raise action_error(_('This invoice does not exist'), code=404)
        
        data = invoice.to_dict(list_type='full')
        
        return action_ok(code=200, data=data)
    
    @web
    @auth
    @role_required('admin')
    def billing_account_deactivate(self, id, **kwargs):
        billing_account_id = kwargs.get('billing_account_id')
        
        account = Session.query(PaymentAccount).filter(PaymentAccount.id == id).first()
        if not account:
            raise action_error(_('Payment account does not exist'), code=404)
        if not c.logged_in_persona in account.members:
            raise action_error(_('You do not have permission to view this account'), code=404)
        
        billing_account = Session.query(BillingAccount).filter(and_(BillingAccount.id==billing_account_id, BillingAccount.payment_account_id==account.id)).first()
        
        print billing_account
        
        if not billing_account or billing_account.status == 'error':
            raise action_error(_('This billing account does not exist'), code=404)
        
        if billing_account.provider == 'paypal-recurring':
            billing_account.provider = 'paypal_recurring'
        if billing_account.provider in api_calls.cancel_recurrings:
            try:
                response = api_calls.cancel_recurrings[billing_account.provider](billing_account.reference)
                #response = api_calls.cancel_recurrings['paypal_express'](billing_account.reference)
            except api_calls.cbPaymentError as e:
                raise action_error(e.value, code=400)
        
        billing_account.status = 'deactivated'
        Session.commit()
        
        return action_ok(code=200)
    
    @web
    @auth
    @role_required('admin')
    def billing_account_add(self, id, **kwargs):
        account = Session.query(PaymentAccount).filter(PaymentAccount.id == id).first()
        if not account:
            raise action_error(_('Payment account does not exist'), code=404)
        if not c.logged_in_persona in account.members:
            raise action_error(_('You do not have permission to view this account'), code=404)
        
        
        return action_ok(code=200)
    
    @web
    @authorize
    @role_required('admin')
    def payment_begin(self, id, **kwargs):
        invoice_id = kwargs.get('invoice_id')
        service    = kwargs.get('service')
        if not (invoice_id and service):
            raise action_error(_('Invalid parameters, need invoice_id and service'), code=400)
        account = Session.query(PaymentAccount).filter(PaymentAccount.id == id).first()
        if not account:
            raise action_error(_('Payment account does not exist'), code=404)
        if not c.logged_in_persona in account.members:
            raise action_error(_('You do not have permission to view this account'), code=404)
        
        amount = 0
        currency = account.currency
        
        if invoice_id:
            invoice = Session.query(Invoice).filter(and_(Invoice.id==invoice_id, Invoice.payment_account_id==account.id)).first()
            if not invoice or invoice.status not in ['billed', 'paid']:
                raise action_error(_('This invoice does not exist'), code=404)
            if invoice.total_due <= 0:
                raise action_error(_('This invoice does not have an outstanding balance'), code=404)
            amount = invoice.total_due
            currency = invoice.currency
            
        if service not in api_calls.begins:
            raise action_error(_('Sorry there is a problem with the payment service you requested'), code=400)
        
        try:
            response = api_calls.begins[service](
                payment_account_id  = id,
                amount              = amount,
                currency            = currency,
                invoice_id          = invoice_id,
                recurring           = kwargs.get('recurring'),
            )
        except api_calls.cbPaymentAPIError as e:
            raise action_error(e.value, code=400)
        
        txn = BillingTransaction()
        
        txn.invoice_id = invoice_id
        txn.amount = amount
        txn.provider = response['provider']
        if response['config_update']:
            txn.config.update(response['config_update'])
        txn.reference = response['reference']
        
        Session.add(txn)
        Session.commit()
        
        if response.get('redirect'):
            return redirect(response['redirect'])
        if response.get('template'):
            return action_ok(code=200, template=template)
        return action_ok(code=200)
    
    @web
    @authorize
    def payment_cancel(self, id, **kwargs):
        service    = kwargs.get('service')
        if not service:
            raise action_error(_('Invalid parameters, need service'), code=400)
        
        if service not in api_calls.cancels:
            raise action_error(_('Sorry there is a problem with the payment service you requested'), code=400)
        
        try:
            response = api_calls.lookups[service](
                **kwargs
            )
        except api_calls.cbPaymentAPIError as e:
            raise action_error(e.value, code=400)
        
        txn = Session.query(BillingTransaction).filter(BillingTransaction.provider==response['provider']).filter(BillingTransaction.reference==response['reference']).first()
        
        if not txn:
            return action_error(_('Payment transaction not found'), 404)
        
        try:
            response = api_calls.cancels[service](
                payment_account_id  = id,
                invoice_id          = txn.invoice.id,
                **kwargs
            )
        except api_calls.cbPaymentAPIError as e:
            raise action_error(e.value, code=400)
        txn.status = response['status']
        Session.commit()
        
        if response.get('redirect'):
            return redirect(response['redirect'])
        return action_ok(code=200)
        
    @web
    @authorize
    def payment_return(self, id, **kwargs):
        service    = kwargs.get('service')
        if not service:
            raise action_error(_('Invalid parameters, need service'), code=400)
        
        if service not in api_calls.returns or service not in api_calls.lookups:
            raise action_error(_('Sorry there is a problem with the payment service you requested'), code=400)
        
        response = api_calls.lookups[service](**kwargs)
        
        txn = Session.query(BillingTransaction).filter(BillingTransaction.provider==response['provider']).filter(BillingTransaction.reference==response['reference']).first()
        
        if not txn:
            return action_error(_('Transaction not found'), code=404)
        
        args = dict(
            payment_account_id=id ,
            **kwargs
        )
        
        if txn.config.get('recurring'):
            args.update({
                'recurring' : txn.config['recurring'],
                'next_date' : txn.invoice.payment_account.next_start_date,
                'frequency' : txn.invoice.payment_account.frequency.capitalize(),
                'amount'    : txn.invoice.payment_account.cost_frequency[txn.invoice.payment_account.frequency],
                'currency'  : txn.invoice.payment_account.currency,
            })
        try:
            response = api_calls.returns[service](
                **args
            )
        except api_calls.cbPaymentRecurringTransactionError as e:
            response = e.dict
            #response_message = e.value
        except api_calls.cbPaymentError as e:
            print args
            txn.status = 'error'
            Session.commit()
            raise action_error(e.value, code=400)
        
        txn.status = response['status']
        txn.config.update(response.get('config_update', {}))
        
        if response.get('billing_account_create'):
            b_a_c = response['billing_account_create']
            bacct = BillingAccount()
            bacct.status = b_a_c['status']
            bacct.title = b_a_c['title']
            bacct.provider = b_a_c['provider']
            bacct.reference = b_a_c['reference'] 
            bacct.payment_account = txn.invoice.payment_account
            bacct.config.update(b_a_c.get('config_update', {}))
            Session.add(bacct)
        Session.commit()
        return redirect(h.url(controller='payment_actions', id=txn.invoice.payment_account.id, action='invoice', invoice_id=txn.invoice.id))
        