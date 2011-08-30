"""
Group Actions
"""

from civicboom.lib.base import *
import civicboom.lib.helpers as h
from sqlalchemy           import or_, and_, null
from civicboom.model import PaymentAccount, Invoice, InvoiceLine, BillingAccount, BillingTransaction, Service
from civicboom.model.member import account_types_level
from decimal import Decimal
import civicboom.lib.payment as payment
import datetime
#from civicboom.controllers.groups import _get_group

log      = logging.getLogger(__name__)

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
        
        if len(account.members) <= 1:
            raise action_error(_("You can't remove the last member from the account"), code=400)
        
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
        
        if not billing_account or billing_account.status in ('error', 'deactivated'):
            raise action_error(_('This billing account does not exist'), code=404)
        
        if billing_account.provider in payment.cancel_recurrings:
            try:
                response = payment.cancel_recurrings[billing_account.provider](billing_account.reference)
            except payment.cbPaymentError as e:
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
        # TODO: Finish me!
        
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
            
        if service not in payment.begins:
            raise action_error(_('Sorry there is a problem with the payment service you requested'), code=400)
        
        try:
            response = payment.begins[service](
                payment_account_id  = id,
                amount              = amount,
                currency            = currency,
                invoice_id          = invoice_id,
                recurring           = kwargs.get('recurring'),
            )
        except payment.cbPaymentAPIError as e:
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
        
        if service not in payment.cancels:
            raise action_error(_('Sorry there is a problem with the payment service you requested'), code=400)
        
        try:
            response = payment.lookups[service](
                **kwargs
            )
        except payment.cbPaymentAPIError as e:
            raise action_error(e.value, code=400)
        
        txn = Session.query(BillingTransaction).filter(BillingTransaction.provider==response['provider']).filter(BillingTransaction.reference==response['reference']).first()
        
        if not txn:
            return action_error(_('Payment transaction not found'), 404)
        
        try:
            response = payment.cancels[service](
                payment_account_id  = id,
                invoice_id          = txn.invoice.id,
                **kwargs
            )
        except payment.cbPaymentAPIError as e:
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
        
        if service not in payment.returns or service not in payment.lookups:
            raise action_error(_('Sorry there is a problem with the payment service you requested'), code=400)
        
        response = payment.lookups[service](**kwargs)
        
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
                'amount'    : txn.invoice.payment_account.cost_taxed,
                'currency'  : txn.invoice.payment_account.currency,
            })
        try:
            response = payment.returns[service](
                **args
            )
        except payment.cbPaymentRecurringTransactionError as e:
            response = e.dict
            #response_message = e.value
        except payment.cbPaymentError as e:
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
    
    @web
    @authorize
    @role_required('admin')
    def regrade(self, id, **kwargs):
        account = Session.query(PaymentAccount).filter(PaymentAccount.id == id).first()
        if not account:
            raise action_error(_('Payment account does not exist'), code=404)
        if not c.logged_in_persona in account.members:
            raise action_error(_('You do not have permission to view this account'), code=404)
        new_account_type = kwargs.get('new_type')
        if new_account_type not in account_types_level:
            raise action_error(_('Invalid account type'), code=400)
        if new_account_type == account.type:
            raise action_error(_('Cannot re-grade account to the same as it is now.'), code=400)
        
        time_now = now()
        
        apply_payment = []
        
        if account.cost_taxed > 0:
            # Do paid account stuff here!
            current_service = Session.query(Service).filter(Service.payment_account_type == account.type).one()
            psd = payment.previous_start_date(account.start_date, account.frequency, time_now) # FIXME
            nsd = payment.calculate_start_date(account.start_date, account.frequency, time_now)
            days_this_period = (nsd - psd).days
            
            def get_invoice_line(status, start_date):
                return Session.query(InvoiceLine)\
                    .join((Invoice, Invoice.id == InvoiceLine.invoice_id))\
                    .filter(Invoice.status == status)\
                    .filter(Invoice.payment_account_id == account.id)\
                    .filter(InvoiceLine.start_date == start_date)\
                    .filter(InvoiceLine.service_id == current_service.id).first()
            
            # Check paid invoice line
            prev_invoice_line = get_invoice_line("paid", psd)
            if prev_invoice_line:
                if len(prev_invoice_line.invoice.lines) == 1:
                    days_elapsed = (time_now.date() - psd).days
                    days_left = days_this_period - days_elapsed
                    apply_payment_prev = BillingTransaction()
                    apply_payment_prev.amount = (((prev_invoice_line.price_final * prev_invoice_line.invoice.tax_rate) / days_this_period) * days_left).quantize(Decimal('0.00'))
                    apply_payment_prev.status = 'complete'
                    apply_payment_prev.provider = 'refund_unused'
                    apply_payment_prev.reference = prev_invoice_line.invoice_id
                    apply_payment.append(apply_payment_prev)
                else:
                    # also raise error to admins?
                    raise action_error(_("Sorry we can't automatically change your account type, please contact us using the feedback form."), code=400)
                
            # Check billed invoice line
            prev_invoice_line = get_invoice_line("billed", psd) or []
            prev_invoice_line.append(get_invoice_line("billed", nsd))
            for line in prev_invoice_line:
                if len(line.invoice.lines) == 1:
                    line.invoice.status = "disregarded"
                else:
                    # also raise error to admins?
                    raise action_error(_("Sorry we can't automatically change your account type, please contact us using the feedback form."), code=400)
                
            prev_invoice_line = get_invoice_line("paid", nsd)
            if prev_invoice_line:
                if len(prev_invoice_line.invoice.lines) == 1:
                    line.invoice.status = "disregarded"
                    apply_payment_next = BillingTransaction()
                    apply_payment_next.amount = prev_invoice_line.invoice.paid_total
                    apply_payment_next.status = 'complete'
                    apply_payment_next.provider = 'refund_unused'
                    apply_payment_next.reference = prev_invoice_line.invoice_id
                    apply_payment.append(apply_payment_next)
                else:
                    # also raise error to admins?
                    raise action_error(_("Sorry we can't automatically change your account type, please contact us using the feedback form."), code=400)
        
        for pas in account.services:
            if pas.service.payment_account_type == account.type:
                Session.delete(pas)
                
        active_billing_accounts = Session.query(BillingAccount).filter(BillingAccount.payment_account_id == account.id)\
            .filter(BillingAccount.status == 'active').all()
        
        for billing_account in active_billing_accounts:
            if billing_account.provider in payment.action_on_regrade:
                try:
                    response = payment.action_on_regrade[billing_account.provider](billing_account.reference)
                except payment.cbPaymentError as e:
                    raise action_error(e.value, code=400)
                billing_account.status = response['status']
            pass
        
        account.start_date = datetime.date.today()
        account.type = new_account_type
        invoice = payment.db_methods.generate_invoice(account, account.start_date)
        invoice.status = 'billed'
        for _payment in apply_payment:
            _payment.invoice = invoice
        Session.commit()
        
        if invoice.total_due <= 0:
            invoice.status = 'paid'
            Session.commit()
            
        return redirect(h.url(controller='payment_actions', id=id, action='invoice', invoice_id = invoice.id))