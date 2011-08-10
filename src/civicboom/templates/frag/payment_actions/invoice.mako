<%inherit file="/frag/common/frag.mako"/>

<%!
    from decimal import Decimal
    from civicboom.model.payment import currency_symbols
%>

##------------------------------------------------------------------------------
##
##------------------------------------------------------------------------------
<%def name="init_vars()">
    <%
        self.attr.title     = _('Payment accounts')
        self.attr.icon_type = 'boom'
    %>
</%def>

<%def name="format_currency(full_currency)">
    % if full_currency:
        ${d['currency']}
    % endif
    ${currency_symbols[d['currency']] | n}
</%def>
<%def name="format_price(price, full_currency=False)">
    ${format_currency(full_currency)}
    ${price}
</%def>

<%def name="body()">
    <style type="text/css">
        .invoice .header, .invoice .customer {
            padding-bottom: 1em;
        }
        .invoice .header .detail {
            text-align: right;
        }
        .invoice .header .detail table {
            text-align: left;
        }
        .invoice .header .detail table td {
            padding-left: 1em;
        }
        .invoice .customer .section {
            width: 50%;
        }
        .invoice .customer .section .header {
            width: 30%;
            font-weight: bold;
        }
        .invoice .customer .section .detail {
            width: 70%;
        }
        .invoice .items table thead td, .invoice .items table tfoot .thead td {
            padding-top: 0.75em;
            padding-bottom: 0.25em;
            font-weight: bold;
            background-color: #DCE4F1;
            border-bottom: 2px solid white
        }
        .invoice .items table tbody tr:nth-child(odd) td {
            font-weight: bold;
            background-color: #EEF6F3;
        }
        .invoice .items table tfoot tr td:nth-child(1) {
            text-align: right;
            padding-right: 1em;
        }
    </style>
    <div class="frag_whitewrap">
        <div class="invoice">
            <div class="header">
                <div class="company fl">
                    <img class="logo_img" src="/images/logo-v3-128x28.png?ut=1310987194" alt="Civicboom" /><br />
                    Enterprise Hub,<br />
                    University of Kent,<br />
                    Canterbury, Kent<br />
                    CT2 7NZ
                </div>
                <div class="fr detail">
                    <h1>Invoice</h1>
                    <table>
                        <tr>
                            <td>Invoice #:</td>
                            <td>${d['id']}</td>
                        </tr>
                        <tr>
                            <td>Date:</td>
                            <td>${h.api_datestr_to_datetime(d['timestamp']).strftime('%a, %d %b %Y')}</td>
                        </tr>
                    </table>
                </div>
                <div class="cb"></div>
            </div>
            <div class="customer">
                <div class="fl section name_address">
                    <div class="fl header">
                        Bill To:
                    </div>
                    <div class="fr detail">
                        <b>${d['payment_account']['name']}</b><br />
                        % for line in d['payment_account']['address']:
                            ${line}<br />
                        % endfor
                    </div>
                    <div class="cb"></div>
                </div>
                <div class="fr section overview">
                    <div class="fl header">
                        Overview:
                    </div>
                    <div class="fr detail">
                        Amount due: ${format_price(d['total_due'])}<br />
                        Due on receipt of invoice<br />
                        Currency:${format_currency(True)}<br />
                        Payment account #: ${d['payment_account']['id']}<br />
                        VAT #: N/A
                    </div>
                </div>
                <div class="cb"></div>
            </div>
            <div class="items">
                <table width="100%">
                    <thead>
                        <tr>
                            <td>
                                Item
                            </td>
                            <td>
                                Unit Price
                            </td>
                            <td>
                                Quantity
                            </td>
                            <td>
                                Price
                            </td>
                        </tr>
                    </thead>
                    <tbody>
                    % for line in d['lines']:
                        <tr>
                            <td>
                                ${line.get('title')}
                            </td>
                            <td>
                                ${format_price(line['price'])}
                            </td>
                            <td>
                                ${line.get('quantity')}
                                % if int(line.get('discount',0)) > 0:
                                    (${_('with %d%% discount') % (line.get('discount')*100)})
                                % endif
                            </td>
                            <td>
                                ${format_price(line['price_final'])}
                            </td>
                        </tr>
                    % endfor
                    </tbody>
                    <tfoot>
                        <tr class="thead">
                            <td colspan="3">&nbsp;</td>
                            <td colspan="1">Totals</td>
                        </tr>
                        <tr>
                            <td colspan="3">Total Before Tax:</td>
                            <td>${format_price(d['total_pre_tax'])}</td>
                        </tr>
                        <tr>
                            <td colspan="3">VAT (20.00%):</td>
                            <td>${format_price(d['total_tax'])}</td>
                        </tr>
                        <tr>
                            <td colspan="3">Total:</td>
                            <td>${format_price(d['total'])}</td>
                        </tr>
                    </tfoot>
                </table>
                <div class="foot" style="text-align: right">
                    <b>Registered Office:</b> Enterprise Hub, University of Kent, Canterbury, Kent CT2 7NZ, GB<br />
                    Company No.: 01234567
                    VAT Registration No.: 012 3456 78
                </div>
            </div>
        </div>
    </div>
    % if Decimal(d['total_due']) > 0 and not d['processing']:
        <div class="frag_whitewrap">
            <h2>Payment Options</h2>
            <img src="https://www.paypalobjects.com/en_GB/i/logo/PayPal_mark_60x38.gif" alt="We accept PayPal" style="float:left;padding-right:2em" />
            <div style="float:left;text-align:center;padding-right:2em">
                <a href="${h.url(controller='payment_actions', id=d['payment_account_id'], action='payment_begin', service='paypal_express', invoice_id=d['id'])}">
                    <img src="https://www.paypalobjects.com/en_GB/i/btn/btn_paynowCC_LG.gif" alt="We accept PayPal" />
                </a><br />
                Pay this invoice
            </div>
        
            <div style="float:left;text-align:center">
                <a href="${h.url(controller='payment_actions', id=d['payment_account_id'], action='payment_begin', service='paypal_express', invoice_id=d['id'], recurring=True)}">
                    <img src="https://www.paypalobjects.com/en_US/GB/i/btn/btn_subscribeCC_LG.gif" alt="We accept PayPal" />
                </a><br />
                Set up a regular payment
            </div>
        
            <div style="clear:both"></div>
        </div>
    % endif
    <div class="frag_whitewrap">
        <h2>Payments applied</h2>
        % for trans in d['transactions']:
            ${trans['provider']} - ${trans['status']} - ${trans['amount']}<br />
        % endfor
    </div>
</%def>