<%inherit file="paypal_inherit_invoice_button.mako" />

<%def name="url()">
${h.url(controller='payment_actions', id=d['payment_account_id'], action='payment_begin', service='paypal_express', invoice_id=d['id'])}
</%def>

${_('Pay this invoice')}<br />
<img src="https://www.paypalobjects.com/en_GB/i/btn/btn_paynowCC_LG.gif" alt="Pay with PayPal" />