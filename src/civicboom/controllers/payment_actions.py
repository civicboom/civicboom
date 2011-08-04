"""
Group Actions
"""

from civicboom.lib.base import *
import civicboom.lib.helpers as h
from sqlalchemy           import or_, and_, null
#from civicboom.lib.payment.paypal import express_checkout_single_auth, express_checkout_get_details
from civicboom.model import PaymentAccount, Invoice, InvoiceLine, BillingAccount, BillingTransaction
from civicboom.lib.payment.paypal import *
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
    @authorize
    @role_required('admin')
    def paypal_begin(self, id, **kwargs):
        """
        """
        
        invoice_id = kwargs.get('invoice_id')
        
        account = Session.query(PaymentAccount).filter(PaymentAccount.id == id).first()
        if not account:
            raise action_error(_('Payment account does not exist'), code=404)
        if not c.logged_in_persona in account.members:
            raise action_error(_('You do not have permission to view this account'), code=404)
        
        invoice = Session.query(Invoice).filter(Invoice.id==invoice_id and Invoice.payment_account_id==account.id).first()
        
        if not invoice or invoice.status not in ['billed', 'paid']:
            raise action_error(_('This invoice does not exist'), code=404)
        
        if invoice.total_due <= 0:
            return action_error(_('This invoice does not have an outstanding balance'), code=404)
        
        #response = express_checkout_single_auth(invoice.total_due, invoice.currency, h.url(controller='payment_actions', id=id, action='paypal_return', qualified=True))
        
        params = {
            'PAYMENTREQUEST_0_PAYMENTACTION'  : 'Sale', #'PAYMENTREQUEST_0_PAYMENTACTION' 'PAYMENTACTION'
            'PAYMENTREQUEST_0_AMT'            : invoice.total_due, #'PAYMENTREQUEST_0_AMT' 'AMT'
            'PAYMENTREQUEST_0_CURRENCYCODE'   : invoice.currency, #'PAYMENTREQUEST_0_CURRENCYCODE' 'CURRENCYCODE'
            'PAYMENTREQUEST_n_INVNUM'         : 'Civicboom_' + str(invoice.id),
            'RETURNURL'                       : h.url(controller='payment_actions', id=id, action='paypal_return', qualified=True),
            'CANCELURL'                       : h.url(controller='payment_actions', id=id, action='paypal_cancel', qualified=True),
            'NOSHIPPING'                      : 1,
            'USERACTION'                      : 'commit',
            'BRANDNAME'                       : _('_site_name'),
            
        }
        
        if kwargs.get('recurring'):
            params.update({
                #'MAXAMT': invoice.total_due,
                'L_BILLINGTYPE0': 'RecurringPayments',
                'L_BILLINGAGREEMENTDESCRIPTION0': 'Civicboom Subscription'
            })
            pass
        
        response = paypal_interface.set_express_checkout(**params)
        
        if 'Success' not in response.ack:
            return action_error(_('There was an error starting your payment with PayPal, please try again later'))
        
        txn = BillingTransaction()
        txn.invoice = invoice
        txn.amount = invoice.total_due
        txn.provider = 'paypal_express'
        txn.config.update({'set_express_checkout': response.raw})
        txn.config['PAYMENTREQUEST_0_PAYMENTACTION'] = 'Sale'
        if kwargs.get('recurring'):
            txn.config['recurring'] = 'Civicboom Subscription'
        txn.reference = response.token
        Session.add(txn)
        Session.commit()
        
        return redirect(paypal_interface.generate_express_checkout_redirect_url(response.token))
        
    @web
    @authorize
    def paypal_cancel(self, **kwargs):
        if 'token' not in kwargs:
            return action_error(_('Need token to continue'), code=404)
        txn = Session.query(BillingTransaction).filter(BillingTransaction.provider=='paypal_express').filter(BillingTransaction.reference==kwargs['token']).first()
        
        if not txn:
            return action_error(_('PayPal transaction not found'), code=404)
        
        txn.status = 'cancelled'
        Session.commit()
        return redirect(h.url(controller='payment_actions', id=txn.invoice.payment_account.id, action='invoice', invoice_id=txn.invoice.id))
        
    @web
    @authorize
    def paypal_return(self, id, **kwargs):
        if 'token' not in kwargs:
            return action_error(_('Need token to continue'), code=404)
        if 'PayerID' not in kwargs:
            return action_error(_('Need PayerID to continue'), code=404)
        token = kwargs['token']
        payerid = kwargs['PayerID']
        
        txn = Session.query(BillingTransaction).filter(BillingTransaction.provider=='paypal_express').filter(BillingTransaction.reference==kwargs['token']).first()
        
        if not txn:
            return action_error(_('PayPal transaction not found'), code=404)
        
        details_response = paypal_interface.get_express_checkout_details(token=kwargs['token'])
        
        if 'Success' not in details_response.ack:
            return action_error(_('There was an error starting your payment with PayPal, please try again later'))
        
        try:
            response = paypal_interface.do_express_checkout_payment(
                token = kwargs['token'],
                PayerID = kwargs['PayerID'],
                PAYMENTREQUEST_0_PAYMENTACTION  = txn.config.get('PAYMENTREQUEST_0_PAYMENTACTION', 'Sale'),
                PAYMENTREQUEST_0_AMT            = details_response.PAYMENTREQUEST_0_AMT,
                PAYMENTREQUEST_0_CURRENCYCODE   = details_response.PAYMENTREQUEST_0_CURRENCYCODE,
                )
        except PayPalAPIResponseError:
            txn.status = 'error'
            # Alert admins to payment error
            Session.commit()
            return redirect(h.url(controller='payment_actions', id=txn.invoice.payment_account.id, action='invoice', invoice_id=txn.invoice.id))

        if 'Success' not in response.ack:
            return action_error(_('There was an error starting your payment with PayPal, please try again later'))
        
        txn.config['transaction_id'] = response.PAYMENTINFO_0_TRANSACTIONID
        txn.config['payment_type'] = response.PAYMENTINFO_0_PAYMENTTYPE
        txn.config['payment_status'] = response.PAYMENTINFO_0_PAYMENTSTATUS
        txn.config['PayerID'] = kwargs['PayerID']
        
        if response.PAYMENTINFO_0_PAYMENTSTATUS in ('Completed',):
            txn.status = 'complete'
        elif response.PAYMENTINFO_0_PAYMENTSTATUS == 'Pending':
            txn.status = 'pending'
            if response.PAYMENTINFO_0_PENDINGREASON in ('address', 'intl', 'multi-currency', 'other'):
                #alert admins to payment needing manual intervention
                pass
        elif response.PAYMENTINFO_0_PAYMENTSTATUS in ('In-Progress', 'Processed'):
            txn.status = 'pending'
        else:
            txn.status = 'failed'
        Session.commit()

        if txn.config.get('recurring'):
            print '### Trying recurring'
            try:
                # Set up recurring payment profile (begin next day date)
                recurring_params = {
                    'token'             : token,
                    'profileStartDate'  : '2011-09-03T00:00:00Z',
                    'desc'              : txn.config['recurring'],
                    'maxFailedPayments' : '0',
                    'billingPeriod'     : txn.invoice.payment_account.frequency.capitalize(),
                    'billingFrequency'  : '1',
                    'amt'               : '10.00',
                    'currencyCode'      : 'GBP', 
                    }
                recurring_response = paypal_interface.create_recurring_payments_profile(**recurring_params)
            except Exception as error:
                return action_error(_('There was an error creating your recurring billing, please try again later'))
            else:
                print '###', recurring_response
                if 'Success' in recurring_response.ACK:
                    try:
                        if recurring_response.PROFILESTATUS == 'ActiveProfile':
                            bacct = BillingAccount()
                            bacct.status = 'active'
                            bacct.provider = 'paypal-recurring'
                            bacct.reference = recurring_response.PROFILEID 
                            bacct.payment_account = txn.invoice.payment_account
                            bacct.config.update(recurring_response.raw)
                            Session.add(bacct)
                        else:
                            return action_error(_('There was an error creating your recurring billing, please try again later'))
                    except:
                        print '3'
                        return action_error(_('There was an error creating your recurring billing, please try again later'))
                else:
                    print '4'
                    return action_error(_('There was an error creating your recurring billing, please try again later'))
                
            Session.commit()
        return redirect(h.url(controller='payment_actions', id=txn.invoice.payment_account.id, action='invoice', invoice_id=txn.invoice.id))
        