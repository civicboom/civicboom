"""
API Calls for Payment Methods
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

class cbPaymentError(Exception):
    def __init__(self, value, saved_dict=None):
        self.value = value
        self.dict  = saved_dict
        
    def __str__(self):
        return repr(self.value)

class cbPaymentAPIError(cbPaymentError):
    pass
    
class cbPaymentArgumentError(cbPaymentError):
    pass
    
class cbPaymentTransactionError(cbPaymentError):
    pass

class cbPaymentRecurringTransactionError(cbPaymentError):
    pass

def paypal_express_begin(payment_account_id, amount, currency, invoice_id=None, recurring=None, **kwargs):
    
    if amount == 0 and not recurring:
        raise cbPaymentAPIError('Need amount or recurring')
    
    params = {
        'PAYMENTREQUEST_0_PAYMENTACTION'  : 'Sale', #'PAYMENTREQUEST_0_PAYMENTACTION' 'PAYMENTACTION'
        'PAYMENTREQUEST_0_AMT'            : amount, #'PAYMENTREQUEST_0_AMT' 'AMT'
        'PAYMENTREQUEST_0_CURRENCYCODE'   : currency, #'PAYMENTREQUEST_0_CURRENCYCODE' 'CURRENCYCODE'
        'RETURNURL'                       : h.url(controller='payment_actions', id=payment_account_id, action='payment_return', service="paypal_express", qualified=True),
        'CANCELURL'                       : h.url(controller='payment_actions', id=payment_account_id, action='payment_cancel', service="paypal_express", qualified=True),
        'NOSHIPPING'                      : 1,
        'USERACTION'                      : 'commit',
        'BRANDNAME'                       : _('_site_name'),
    }
    if invoice_id:
        params['PAYMENTREQUEST_0_INVNUM'] = str(invoice_id)
    
    if recurring:
        params.update({
            #'MAXAMT': invoice.total_due,
            'L_BILLINGTYPE0': 'RecurringPayments',
            'L_BILLINGAGREEMENTDESCRIPTION0': 'Civicboom Subscription'
        })
    try:
        response = paypal_interface.set_express_checkout(**params)
    except:
        raise cbPaymentAPIError(_('There was an error starting your payment with PayPal, please try again later'))
    
    if 'Success' not in response.ack:
        raise cbPaymentTransactionError(_('There was an error starting your payment with PayPal, please try again later'))
    
    result = paypal_express_lookup(token = response.token)
    result.update({
        'config_update'         : {
            'set_express_checkout'  : response.raw,
        },
        'redirect'              : paypal_interface.generate_express_checkout_redirect_url(response.token)
    })
    
    if recurring:
        result['config_update']['recurring'] = params['L_BILLINGAGREEMENTDESCRIPTION0']
    
    return result

def paypal_express_lookup(**kwargs):
    if 'token' not in kwargs:
        raise cbPaymentArgumentError(_('Need token to continue'))
    result = {
        'provider' : 'paypal_express',
        'reference': kwargs.get('token'),
    }
    return result

def paypal_express_cancel(**kwargs):
    result = paypal_express_lookup(**kwargs)
    result.update({
        'status'   : 'cancelled',
        'redirect' : h.url(controller='payment_actions', id=kwargs.get('payment_account_id'), action='invoice', invoice_id=kwargs.get('invoice_id')), 
    })
    return result

def paypal_express_return(**kwargs):
    if 'PayerID' not in kwargs:
        raise cbPaymentArgumentError(_('Need PayerID to continue'))
    payerid = kwargs['PayerID']
    token   = kwargs['token']
    
    # Try getting express checkout details
    try:
        details_response = paypal_interface.get_express_checkout_details(token=token)
    except PayPalAPIResponseError:
        cbPaymentAPIError('')
        # Return error
        return {
            'status' : 'error'
        }
    print '###', details_response
    # Check action was successful!
    if 'Success' not in details_response.ack:
        return action_error(_('There was an error starting your payment with PayPal'))
    # Try finalising express checkout payment
    try:
        response = paypal_interface.do_express_checkout_payment(
            token = token,
            PayerID = payerid,
            # Oops, we don't have access to the transaction as we are abstracted from the civicboom orm!
            #PAYMENTREQUEST_0_PAYMENTACTION  = txn.config.get('PAYMENTREQUEST_0_PAYMENTACTION', 'Sale'),
            PAYMENTREQUEST_0_AMT            = details_response.PAYMENTREQUEST_0_AMT,
            PAYMENTREQUEST_0_CURRENCYCODE   = details_response.PAYMENTREQUEST_0_CURRENCYCODE,
            )
    except:
        raise cbPaymentAPIError('There was an error communicating with PayPal.')
        # Return error
        return {
            'status' : 'error'
        }
    # Check action was successful!
    if 'Success' not in response.ack:
        raise cbPaymentTransactionError(_('There was an error processing your payment with PayPal'))
    
    result = {
        'status'  : 'complete',
        'config_update' : {
            'transaction_id': response.PAYMENTINFO_0_TRANSACTIONID,
            'payment_type'  : response.PAYMENTINFO_0_PAYMENTTYPE,
            'payment_status': response.PAYMENTINFO_0_PAYMENTSTATUS,
            'payerid'       : payerid,
        }
    }
    
    if response.PAYMENTINFO_0_PAYMENTSTATUS in ('Completed',):
        result['status'] = 'complete'
    elif response.PAYMENTINFO_0_PAYMENTSTATUS == 'Pending':
        result['status'] = 'pending'
        if response.PAYMENTINFO_0_PENDINGREASON in ('address', 'intl', 'multi-currency', 'other'):
            #alert admins to payment needing manual intervention
            pass
    elif response.PAYMENTINFO_0_PAYMENTSTATUS in ('In-Progress', 'Processed'):
        result['status'] = 'pending'
    else:
        result['status'] = 'failed'
    
    if kwargs.get('recurring'):
        # Do recurring stuff here
        try:
            # Set up recurring payment profile (begin next day date)
            recurring_params = {
                'token'             : token,
                'profileStartDate'  : kwargs['next_date'].strftime('%Y-%m-%dT00:00:00Z'),
                'desc'              : kwargs['recurring'],
                'maxFailedPayments' : '0',
                'billingPeriod'     : kwargs['frequency'],
                'billingFrequency'  : '1',
                'amt'               : kwargs['amount'],
                'currencyCode'      : kwargs['currency'],
                }
            print '###rp###', recurring_params
            recurring_response = paypal_interface.create_recurring_payments_profile(**recurring_params)
        except Exception as error:
            raise cbPaymentRecurringTransactionError(_('There was an error creating your recurring billing, please try again later'), result)
        else:
            print '###', recurring_response
            if 'Success' in recurring_response.ACK:
                result.update({
                    'billing_account_create': {
                        'status'        : 'active' if recurring_response.PROFILESTATUS == 'ActiveProfile' else 'pending',
                        'title'         : 'PayPal Subscription **%s' % recurring_response.PROFILEID[-4:],
                        'provider'      : 'paypal_recurring',
                        'reference'     : recurring_response.PROFILEID,
                        'config_update' : recurring_response.raw,
                    }
                })
            else:
                raise cbPaymentRecurringTransactionError('There was an error communicating with PayPal, please try again later', result)
    Session.commit()
    return result

def paypal_recurring_cancel(reference):
    try:
        response = paypal_interface.manage_recurring_payments_profile_status(reference, 'Cancel')
    except:
        raise cbPaymentAPIError('There was an error communicating with PayPal, please try again later')
    if 'Success' not in response.ACK:
        raise cbPaymentTransactionError('Error cancelling recurring payment with PayPal')
    return {
        'status'    : 'deactivated'
    }
    
def paypal_express_check_transaction(reference):
    try:
        response = paypal_interface.get_transaction_details(
            transactionid = reference,
        )
    except:
        raise cbPaymentAPIError('There was an error communicating with PayPal, please try again later')
    if 'Success' not in response.ACK:
        raise cbPaymentTransactionError('Error finding the PayPal transaction')
    result = {}
    if response.PAYMENTSTATUS in ('Completed','Canceled-Reversal'):
        result['status'] = 'complete'
    elif response.PAYMENTSTATUS in ('Denied', 'Expired', 'Failed', 'Refunded', 'Reversed', 'Voided'):
        result['status'] = 'cancelled'
    else:
        result['status'] = 'pending'
    return result

def paypal_recurring_check(reference):
    paypal_to_civicboom_status = {
        'Active'     :'active',
        'Pending'    :'pending',
        'Cancelled'  :'deactivated',
        'Suspended'  :'flagged',
        'Expired'    :'deactivated',
    }
    try:
        response = paypal_interface.get_recurring_payments_profile_details(profileid=billing_account.reference)
    except:
        raise cbPaymentAPIError('There was an error communicating with PayPal, please try again later')
    if 'Success' not in response.ACK:
        raise cbPaymentTransactionError('Error finding the PayPal subscription')
    
    result = {}
    if response.STATUS in paypal_to_civicboom_status.keys():
        result['status'] = paypal_to_civicboom_status[response.STATUS]
    else:
        result['status'] = 'error'
    if 'LASTPAYMENTDATE' in response.raw:
        last_date = datetime.strptime(response.LASTPAYMENTDATE, '%Y-%m-%dT%H:%M:%SZ')
        result['create_transaction'] = {
            'timestamp' : last_date,
            'status'    : 'complete',
            'amount'    : response.LASTPAYMENTAMT,
            'provider'  : 'paypal_recurring',
            'reference' : response.PROFILEID
        }
    return result
# GregM: Integrating all payment services into one set of calls
#    @web
#    @authorize
#    @role_required('admin')
#    def paypal_begin(self, id, **kwargs):
#        """
#        """
#        
#        invoice_id = kwargs.get('invoice_id')
#        
#        account = Session.query(PaymentAccount).filter(PaymentAccount.id == id).first()
#        if not account:
#            raise action_error(_('Payment account does not exist'), code=404)
#        if not c.logged_in_persona in account.members:
#            raise action_error(_('You do not have permission to view this account'), code=404)
#        
#        invoice = Session.query(Invoice).filter(Invoice.id==invoice_id and Invoice.payment_account_id==account.id).first()
#        
#        if not invoice or invoice.status not in ['billed', 'paid']:
#            raise action_error(_('This invoice does not exist'), code=404)
#        
#        if invoice.total_due <= 0:
#            return action_error(_('This invoice does not have an outstanding balance'), code=404)
#        
#        #response = express_checkout_single_auth(invoice.total_due, invoice.currency, h.url(controller='payment_actions', id=id, action='paypal_return', qualified=True))
#        
#        params = {
#            'PAYMENTREQUEST_0_PAYMENTACTION'  : 'Sale', #'PAYMENTREQUEST_0_PAYMENTACTION' 'PAYMENTACTION'
#            'PAYMENTREQUEST_0_AMT'            : invoice.total_due, #'PAYMENTREQUEST_0_AMT' 'AMT'
#            'PAYMENTREQUEST_0_CURRENCYCODE'   : invoice.currency, #'PAYMENTREQUEST_0_CURRENCYCODE' 'CURRENCYCODE'
#            'PAYMENTREQUEST_n_INVNUM'         : 'Civicboom_' + str(invoice.id),
#            'RETURNURL'                       : h.url(controller='payment_actions', id=id, action='paypal_return', qualified=True),
#            'CANCELURL'                       : h.url(controller='payment_actions', id=id, action='paypal_cancel', qualified=True),
#            'NOSHIPPING'                      : 1,
#            'USERACTION'                      : 'commit',
#            'BRANDNAME'                       : _('_site_name'),
#        }
#        
#        if kwargs.get('recurring'):
#            params.update({
#                #'MAXAMT': invoice.total_due,
#                'L_BILLINGTYPE0': 'RecurringPayments',
#                'L_BILLINGAGREEMENTDESCRIPTION0': 'Civicboom Subscription'
#            })
#            pass
#        
#        response = paypal_interface.set_express_checkout(**params)
#        
#        if 'Success' not in response.ack:
#            return action_error(_('There was an error starting your payment with PayPal, please try again later'))
#        
#        txn = BillingTransaction()
#        txn.invoice = invoice
#        txn.amount = invoice.total_due
#        txn.provider = 'paypal_express'
#        txn.config.update({'set_express_checkout': response.raw})
#        txn.config['PAYMENTREQUEST_0_PAYMENTACTION'] = 'Sale'
#        if kwargs.get('recurring'):
#            txn.config['recurring'] = 'Civicboom Subscription'
#        txn.reference = response.token
#        Session.add(txn)
#        Session.commit()
#        
#        return redirect(paypal_interface.generate_express_checkout_redirect_url(response.token))

begins              = {'paypal_express':    paypal_express_begin}
cancels             = {'paypal_express':    paypal_express_cancel}
returns             = {'paypal_express':    paypal_express_return}
lookups             = {'paypal_express':    paypal_express_lookup}
cancel_recurrings   = {'paypal_recurring':  paypal_recurring_cancel}
check_transactions  = {'paypal_express':    paypal_express_check_transaction}
check_recurrings    = {'paypal_recurring':  paypal_recurring_check}