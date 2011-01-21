<%inherit file="/html/web/common/html_base.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">${_("Link other accounts")}</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">

<h1>${_("Link accounts")}</h1>

<h2>${_("Currently linked accounts")}</h2>
    <ul>
        % for login in c.logged_in_persona.login_details:
        <li>${login.type}</li>
        % endfor
    </ul>

<h2>${_("Add Account")}</h2>
    ${h.get_janrain(lang=c.lang)}

</%def>