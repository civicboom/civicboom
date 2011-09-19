<%inherit file="/html/web/common/frag_container.mako"/>

<%namespace name="frag" file="/frag/common/frag.mako"/>


<%def name="title()">${_("Link other login accounts")}</%def>

<%def name="body()">
	<%
        self.attr.frags = [link_accounts, help]
        self.attr.frag_col_sizes = [2,1]
    %>
</%def>

<%def name="link_accounts()">
	##<%include file="/frag/settings/settings.mako"/>
    ${frag.frag_basic(_("Link other login accounts"), 'settings', link_accounts_frag)}
</%def>

<%def name="link_accounts_frag()">
    <h1>${_("Link accounts")}</h1>
    
    <h2>${_("Currently Linked Accounts")}</h2>
        <ul>
            % for login in c.logged_in_persona.login_details:
            <li>${login.type.capitalize()}</li>
            % endfor
        </ul>
    
    <h2>${_("Add Account")}</h2>
        ${h.get_janrain(lang=c.lang)}
    <br />
    <a class="button" href    = "${h.url('settings')}" title   = "${_('Back to Settings')}">
      <span>${_('Back to Settings')}</span>
    </a>
</%def>

<%def name="help()">
	<!--#include virtual="/help/link_accounts"-->
</%def>





