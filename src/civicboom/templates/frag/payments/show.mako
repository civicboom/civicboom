<%inherit file="/frag/common/frag.mako"/>

<%!
    from decimal import Decimal
    from civicboom.model.payment import currency_symbols
    from civicboom.model.member import PaymentAccount
    _address_config_order = PaymentAccount._address_config_order
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
        <h1>${_('Manage your payment account')}</h1>
        <div class="fl" style="width: 50%">
            <p><h3>${_('Account details')}</h3>
            ${_('Payment account number')}: ${d['id']}<br />
            ${_('Account type')}: ${_('_'+d['type']).capitalize()}<br />
            ${_('Account status')}: ${d['billing_status']}
            % if d['do_not_bill'] == 'True':
                <br />
                ${_('This account is set to be billed manually.')}
            % endif
            
            </p>
        </div>
        <div class="fr" style="width: 50%;">
            <p><h3>${_('Name')}:</h3>${d['name']}</p>
            <p>
                <h3>${_('Address')}:</h3>
                % for key in _address_config_order:
                    % if d['address'].get(key):
                        ${d['address'].get(key,'')}<br />
                    % endif
                % endfor
            </p>
        </div>
        <div class="cb">
            <div class="fl" style="width: 50%;">
                <p><a href="${h.url('payment_action', action='regrade_plans', id=d['id'])}">Upgrade / downgrade</a></p>
            </div>
            <div class="fr" style="width: 50%;">
                <p><a href="${h.url('edit_payment', id=d['id'])}">${_('Edit account information')}</a></p>
            </div>
        </div>
        <div class="cb"></div>
    </div>
    <div class="frag_whitewrap" style="float:left;width:42%; margin-right:0;">
        <h2>${_('Services')}</h2>
        <ul>
            % for service in d['services_full']:
                <li>
                    ${service['service']['title']} - ${format_price(service['price_taxed'])}
                </li>
            % endfor
        </ul>
        <h2>${_('Total cost')}:</h2>
        <p>
            ${format_price(d['cost_taxed'])} billed every ${d['frequency']}<br />
        </p>
        <p>${_('All prices shown are inclusive of taxes')}</p>
    </div>
    <div class="frag_whitewrap" style="float:right;width:42%; margin-left:0;">
        <h2>${_('Payment Methods')}</h2>
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
                            form_data       = dict(json_complete = "[ ['update'] ]"),
                            #json_form_complete_actions = "cb_frag_reload(current_element);" ,
                        )}
                    </div>
                </li>
                % endif
            % endfor
        </ul>
    </div>
    <div class="frag_whitewrap" style="float:right;width:42%; margin-left:0;">
        <h2>${_('Invoices')}</h2>
        <ul>
            % for invoice in d['invoices']:
                <li>
                    <a class="link_new_frag"
                        href="${h.url('payment_action', action='invoice', id=d['id'], invoice_id=invoice['id'])}"
                        data-frag="${h.url('payment_action', format='frag', action='invoice', id=d['id'], invoice_id=invoice['id'])}">
                        ${invoice['id']} - ${h.api_datestr_to_datetime(invoice['timestamp']).strftime('%a, %d %b %Y')} - ${invoice['status']}
                    </a>
                </li>
            % endfor
        </ul>
    </div>
    <div class="cb"></div>
    <div class="frag_whitewrap">
        <h2>${_('Users and hubs associated with this account')}</h2>
        <ul>
            % for member in d['members']:
                <li>
                    <a class="link_new_frag"
                        href="${h.url('member', id=member.get('username'))}"
                        data-frag="${h.url('member', format='frag', id=member.get('username'))}">
                        ${member.get('name')}
                    </a>
                    <div class="fr">
                        ${h.secure_link(
                            h.args_to_tuple('payment_action', action='member_remove', id=d['id'], username=member.get('username'), format='redirect') ,
                            value           = _('Remove') ,
                            title           = _("Remove %s") % member.get('name', '') ,
                            form_data       = dict(json_complete = "[ ['update'] ]"),
                            #json_form_complete_actions = "cb_frag_reload(current_element); " #% url('payment', id=self.id),
                        )}
                    </div>
                    
                </li>
            % endfor
        </ul>
        <br />
        ${h.frag_link(value=_('Add members'), title=_('Add members'), href_tuple=h.args_to_tuple('invite', id=d['id'], invite='payment_add_user'))}
    </div>
</%def>