<%inherit file="/web/html_base.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">${_("Sign in")}</%def>

##------------------------------------------------------------------------------
## Navigation override - remove it
##------------------------------------------------------------------------------
<%def name="navigation()"></%def>

##------------------------------------------------------------------------------
## Style Overrides
##------------------------------------------------------------------------------
##<%def name="styleOverides()">
##fieldset{height: 12em;}
##</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">

  <%
    authkit_form_action = "FORM_ACTION" # A string that is replaced by the authkit system
  %>

  % if hasattr(app_globals,'janrain_signin_url'):
    ${h.get_janrain(lang=c.lang)}
    <% authkit_form_action = ""%>
  % endif

  <div class="form_signin yui-gb">
  
    <div class="yui-u first">
      <form action="${authkit_form_action}" method="post">
        <fieldset><legend>${_("Sign in")}</legend>
          <p><label for="username">${_("Username")}</label><input type="text"     id="username" name="username"/></p>
          <p><label for="password">${_("Password")}</label><input type="password" id="password" name="password"/></p>
          <input type="submit" name="submit" value="${_("Sign in")}"/>
        </fieldset>
      </form>
    </div>

    <div class="yui-u inverted">
      <form action="${h.url(controller='register', action='email')}" method="post">
        <fieldset><legend>${_("Sign up")}</legend>
          <p><label for="username_register"     >${_("Username")}        </label><input type="text"  id="username_register"      name="username"/></p>
          <p><label for="email_signup"          >${_("Email")}           </label><input type="text"  id="email_signup"           name="email"   /></p>
          <p><label for="user_type_individual"  >${_("Individual")}      </label><input type="radio" id="user_type_individual"   name="user_type" value="individual"   checked='checked'/></p>
          <p><label for="user_type_organisation">${_("Organisation")}    </label><input type="radio" id="user_type_organisation" name="user_type" value="organisation"                  /></p>
          ##<input type="hidden" name="user_type" value="organisation"/>
          <input type="submit" name="submit" value="${_("Sign up")}"/>
        </fieldset>
      </form>
    </div>

    <div class="yui-u">
      <form action="${h.url(controller='account', action='forgot_password_reminder')}" method="post">
        <fieldset><legend>${_("Forgotten Password?")}</legend>
          <p><label for="username_forgoten">${_("Username")}</label><input type="text" id="username_forgoten" name="username"/></p>
          <p><label>or</label></p>
          <p><label for="email_forgoten"   >${_("Email")}   </label><input type="text" id="email_forgotten"   name="email"   /></p>
          <input type="submit" name="submit" value="${_("Send password reminder")}"/>
        </fieldset>
      </form>
    </div>

  </div>

</%def>
