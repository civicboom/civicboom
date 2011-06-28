<%inherit file="/frag/common/frag.mako"/>


<%!
    from sets import Set
    rss_url   = False
    help_frag = 'link_accounts'
%>

<%def name="title()">${_("%s Link additional login accounts") % (c.logged_in_persona.username)}</%def>

<%def name="body()">
    <h1>${_('%(username)s link additional login accounts') % dict(username= c.logged_in_persona.username.capitalize()) }</h1>
    
    <h2>${_("Currently Linked Accounts")}</h2>
        <ul>
            % for login in c.logged_in_persona.login_details:
            <li>${login.type.capitalize()}</li>
            % endfor
        </ul>
    
    <h2>${_("Add Account")}</h2>
        ${h.get_janrain(lang=c.lang, return_url=h.url('account/link_janrain', id=c.result.get('username'), qualified=True))}
    <br />
##    <a class="button" href    = "${h.url('settings')}" title   = "${_('Back to Settings')}">
##      <span>${_('Back to Settings')}</span>
##    </a>
</%def>
