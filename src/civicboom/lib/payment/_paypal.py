from pylons import config, app_globals, tmpl_context as c, request

from civicboom.lib.web import current_url, url, current_protocol, redirect

from urllib import urlencode
from urlparse import parse_qs
import urllib2

"""
PayPal API Helpers
 
"""

import logging
log = logging.getLogger(__name__)

def pp_generate_credentials():
    return [
        ('user'      , config['api_key.paypal.username']),
        ('pwd'       , config['api_key.paypal.password']),
        ('version'   , '72.0'),
        ('signature' , config['api_key.paypal.signature']),
    ]
    
base_api_params = pp_generate_credentials()
api_url         = config['api_key.paypal.url']
ec_url          = config['api_key.paypal.url_express']

def pp_generate_call(method, params = None):
    api_params = base_api_params[:]
    api_params.append(('method', method))
    if params:
        api_params.extend(params.items())
    return api_params

def express_checkout_single_auth(amount, currency, return_url):
    params = urlencode(pp_generate_call(
        method = 'SetExpressCheckout',
        params = {
            'PAYMENTREQUEST_0_PAYMENTACTION'    : 'Sale', # Could be InstantPaymentOnly to only allow instant (non clear waiting) payments
            'PAYMENTREQUEST_0_AMT'              : '%.2f' % amount,
            'PAYMENTREQUEST_0_CURRENCYCODE'     : currency,
            'RETURNURL'                         : return_url,
            'CANCELURL'                         : return_url,
            'NOSHIPPING'                        : 1,
            'USERACTION'                        : 'commit',
        }), True)
    response = urllib2.urlopen(api_url, params)
    reply = parse_qs(response.read())
    if 'Success' in reply.get('ACK'):
        return (True, {'express_checkout_single_auth': reply}, ec_url + reply['TOKEN'][0])
    return (False, '')

#{"ACK": ["Success"], "LASTNAME": ["User"], "SHIPDISCAMT": ["0.00"], "PAYMENTREQUEST_0_INSURANCEAMT": ["0.00"], "EMAIL": ["gm_1311958484_per@civicboom.com"], "CORRELATIONID": ["c9dcafe8c1bf0"], "SHIPPINGAMT": ["0.00"], "PAYMENTREQUEST_0_INSURANCEOPTIONOFFERED": ["false"], "TAXAMT": ["0.00"], "PAYMENTREQUEST_0_AMT": ["10.00"], "PAYMENTREQUEST_0_HANDLINGAMT": ["0.00"], "PAYMENTREQUEST_0_TAXAMT": ["0.00"], "PAYMENTREQUESTINFO_0_ERRORCODE": ["0"], "AMT": ["10.00"], "PAYERID": ["MBL9UZ2WXKYDW"], "COUNTRYCODE": ["GB"], "PAYMENTREQUEST_0_CURRENCYCODE": ["USD"], "CURRENCYCODE": ["USD"], "TOKEN": ["EC-6B033511UD4230410"], "VERSION": ["72.0"], "PAYMENTREQUEST_0_SHIPDISCAMT": ["0.00"], "BUILD": ["2020243"], "INSURANCEAMT": ["0.00"], "CHECKOUTSTATUS": ["PaymentActionNotInitiated"], "PAYERSTATUS": ["verified"], "FIRSTNAME": ["Test"], "TIMESTAMP": ["2011-08-01T10:46:03Z"], "PAYMENTREQUEST_0_SHIPPINGAMT": ["0.00"], "HANDLINGAMT": ["0.00"]}

def express_checkout_get_details(token, payer_id):
    params = urlencode(pp_generate_call(
        method = 'GetExpressCheckoutDetails',
        params = {
            'TOKEN': token,
        }), True)
    response = urllib2.urlopen(api_url, params)
    reply = parse_qs(response.read())
    if 'Success' in reply.get('ACK'):
        if 'CHECKOUTSTATUS' in reply:
            if 'PaymentActionNotInitiated' in reply['CHECKOUTSTATUS']:
                return do_express_checkout_payment(token, payer_id, reply['PAYMENTREQUEST_0_AMT'][0], reply['PAYMENTREQUEST_0_CURRENCYCODE'][0])
    return (reply.get('ACK'), {'express_checkout_get_details': reply}, False)

def do_express_checkout_payment(token, payer_id, amount, currency):
    params = urlencode(pp_generate_call(
        method = "DoExpressCheckoutPayment",
        params = {
            'TOKEN':token,
            'PAYERID':payer_id,
            'PAYMENTREQUEST_0_PAYMENTACTION': 'Sale',
            'PAYMENTREQUEST_0_AMT': amount,
            'PAYMENTREQUEST_0_CURRENCYCODE': currency
        }), True)
    response = urllib2.urlopen(api_url, params)
    reply = parse_qs(response.read())
    if 'Success' not in reply.get('ACK'):
        return (False,False,False)
    return (reply.get('PAYMENTINFO_0_PAYMENTSTATUS', (False,))[0], {'do_express_checkout_payment': reply}, False)
