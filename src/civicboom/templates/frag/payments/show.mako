<%inherit file="/frag/common/frag.mako"/>

##------------------------------------------------------------------------------
##
##------------------------------------------------------------------------------
<%def name="init_vars()">
    <%
        self.attr.title     = _('Payment accounts')
        self.attr.icon_type = 'boom'
    %>
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
    <div class="frag_whitewrap" style="float:left;width:42%">
        <h2>Services</h2>
        <p>The following services have been applied to your account:</p>
        <ul>
            % for service in d['services_full']:
                <li>
                    ${service['service']['title']} - ${d['currency']} ${service['price']} (ex VAT) per ${service['frequency']}
                </li>
            % endfor
        </ul>
        <p>
            Total cost:<br />
            % for freq, cost in d['cost_frequency'].items():
            ${cost} billed every ${freq}<br />
            % endfor
        </p>
    </div>
    <div class="frag_whitewrap" style="float:right;width:42%">
        <h2>Invoices</h2>
        <ul>
            % for invoice in d['invoices']:
                <li><a href="${h.url('payment_action', action='invoice', id=d['id'], invoice_id=invoice['id'])}">${invoice.get('id')} - ${invoice.get('timestamp')} - ${invoice.get('status')}</a></li>
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