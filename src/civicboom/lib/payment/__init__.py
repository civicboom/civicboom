from civicboom.lib.payment.api_calls import *
from civicboom.lib.payment.functions import *
from db_methods import *

import db_methods as db_methods

__all__ = [
    'begins', 'cancels', 'returns', 'lookups', 'cancel_recurrings',
    'cbPaymentError', 'cbPaymentAPIError', 'cbPaymentArgumentError', 'cbPaymentTransactionError', 'cbPaymentRecurringTransactionError',
    'db_methods', 'get_payment_options', 
]

begins              = {'paypal_express':    paypal_express_begin}
cancels             = {'paypal_express':    paypal_express_cancel}
returns             = {'paypal_express':    paypal_express_return}
lookups             = {'paypal_express':    paypal_express_lookup}
cancel_recurrings   = {'paypal_recurring':  paypal_recurring_cancel}
check_transactions  = {'paypal_express':    paypal_express_check_transaction}
check_recurrings    = {'paypal_recurring':  paypal_recurring_check}
action_on_regrade   = {'paypal_recurring':  paypal_recurring_cancel}

options     = {
    'providers': {
        'paypal_express': {
            'exclusive_to'  :  ('paypal_recurring',) ,
            'invoice_button': True ,
            'group'         : 'paypal' ,
        } ,
        'paypal_recurring': {
            'exclusive_to'  : ('paypal_recurring',) ,
            'invoice_button': True ,
            'group'         : 'paypal' ,
        } ,
    } ,
    'groups': ['paypal'],
}