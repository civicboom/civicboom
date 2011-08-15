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
        self.id             = d['id']
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

##------------------------------------------------------------------------------
## Signin Fragment
##------------------------------------------------------------------------------
<%def name="body()">
    <div class="frag_whitewrap">
        <h1>Manage your payment account</h1>
        <p>Payment account number: ${d['id']}</p>
        <p>Account type: ${_('_'+d['type']).capitalize()}</p>
    </div>
    <div class="frag_whitewrap" style="float:left;width:42%; margin-right:0;">
        <h2>Services</h2>
        <ul>
            % for service in d['services_full']:
                <li>
                    ${service['service']['title']} - ${format_price(service['price_taxed'])}
                </li>
            % endfor
        </ul>
        <h2>Total cost:</h2>
        <p>
            ${format_price(d['cost_taxed'])} billed every ${d['frequency']}<br />
        </p>
        <p>All prices shown are inclusive of taxes</p>
    </div>
    <div class="frag_whitewrap" style="float:right;width:42%; margin-left:0;">
        <h2>Payment Methods</h2>
        <ul>
            % for billing_account in d['billing_accounts']:
                % if billing_account['status'] == 'active':
                <li>
                    ${billing_account['title']}
                    <div class="fr">
                        ${h.secure_link(
                            h.args_to_tuple('payment_action', action='billing_account_deactivate', format='redirect', id=self.id, billing_account_id=billing_account['id']) ,
                            value           = _('Deactivate') ,
                            value_formatted = h.literal("<span class='icon16 i_delete'><span>%s</span></span>" %_('Deactivate')) ,
                            json_form_complete_actions = "cb_frag_reload(current_element);" ,
                        )}
                    </div>
                </li>
                % endif
            % endfor
        </ul>
    </div>
    <div class="frag_whitewrap" style="float:right;width:42%; margin-left:0;">
        <h2>Invoices</h2>
        <ul>
            % for invoice in d['invoices']:
                <li>
                    <a href="${h.url('payment_action', action='invoice', id=d['id'], invoice_id=invoice['id'])}" onclick="cb_frag($(this), '${h.url('payment_action', format='frag', action='invoice', id=d['id'], invoice_id=invoice['id'])}'); return false;">
                        ${invoice.get('id')} - ${invoice.get('timestamp')} - ${invoice.get('status')}
                    </a>
                </li>
            % endfor
        </ul>
    </div>
    <div class="cb"></div>
    <div class="frag_whitewrap">
        <h2>Users and hubs associated with this account</h2>
        <ul>
            % for member in d['members']:
                <li>
                    <a href="${h.url('member', id=member.get('username'))}">${member.get('name')}</a>
                    <div class="fr">
                        ${h.secure_link(
                            h.args_to_tuple('payment_action', action='member_remove', id=d['id'], username=member.get('username'), format='redirect') ,
                            value           = _('Remove') ,
                            title           = _("Remove %s") % member.get('name', '') ,
                        )}
                    </div>
                    
                </li>
            % endfor
        </ul>
        <br />
        ${h.frag_link(value='Add members', title='Add members', href_tuple=h.args_to_tuple('invite', id=d['id'], invite='payment_add_user'))}
    </div>
</%def>