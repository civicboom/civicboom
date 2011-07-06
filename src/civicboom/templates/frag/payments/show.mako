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
        <h1>Details of your payment account</h1>
        <p>Payment account number: ${d['account_id']}</p>
        <p>Account type: ${_('_'+d['account_type']).capitalize()}</p>
        <h2>Users and hubs associated with this account</h2>
        <ul>
            % for member in d['members']:
                <li>
                    <a href="${h.url('member', id=member.get('username'))}">${member.get('name')}</a>
                    <div class="fr">
                        ${h.secure_link(
                            h.args_to_tuple('payment_action', action='member_remove', id=d['account_id'], username=member.get('username'), format='redirect') ,
                            value           = _('Remove') ,
                            title           = _("Remove") ,
                        )}
                    </div>
                    
                </li>
            % endfor
        </ul>
        <br />
        ${h.frag_link(value='Add members', title='Add members', href_tuple=h.args_to_tuple('invite', id=d['account_id'], invite='payment_add_user'))}
    </div>
</%def>