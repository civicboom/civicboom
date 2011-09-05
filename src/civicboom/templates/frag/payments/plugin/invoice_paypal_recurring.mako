<%inherit file="paypal_inherit_invoice_button.mako" />

<%def name="url()">
${h.url(controller='payment_actions', id=d['payment_account_id'], action='payment_begin', service='paypal_express', invoice_id=d['id'], recurring=True)}
</%def>

${_('Set up regular payments')}<br />
<img src="/images/payment/pp_pay_sub.gif" alt="Pay and Subscribe with PayPal" />