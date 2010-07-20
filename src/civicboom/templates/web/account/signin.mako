<%inherit file="/web/html_base.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">Signin</%def>

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
  <div class="yui-gb">
  
    <div class="yui-u first">
      <form action="FORM_ACTION" method="post">
        <fieldset><legend>Sign in</legend>
          <p><label for="username">Username</label><input type="text"     id="username" name="username"/></p>
          <p><label for="password">Password</label><input type="password" id="password" name="password"/></p>
          <input type="submit" name="submit" value="Sign in"/>
        </fieldset>
      </form>
    </div>

    <div class="yui-u inverted">
      <form action="${h.url(controller='register', action='register_email')}" method="post">
        <fieldset><legend>Sign up</legend>
          <p><label for="username_register"     >Username        </label><input type="text"  id="username_register"      name="username"/></p>
          <p><label for="email_signup"          >Email           </label><input type="text"  id="email_signup"           name="email"   /></p>
          <p><label for="user_type_individual"  >Individual      </label><input type="radio" id="user_type_individual"   name="user_type" value="individual"   checked='checked'/></p>
          <p><label for="user_type_organisation">Organisation    </label><input type="radio" id="user_type_organisation" name="user_type" value="organisation"                  /></p>
          ##<input type="hidden" name="user_type" value="organisation"/>
          <input type="submit" name="submit" value="Sign up"/>
        </fieldset>
      </form>
    </div>

    <div class="yui-u">
      <form action="${h.url(controller='account', action='forgot_password_reminder')}" method="post">
        <fieldset><legend>Forgotten Password?</legend>
          <p><label for="username_forgoten">Username</label><input type="text" id="username_forgoten" name="username"/></p>
          <p><label>or</label></p>
          <p><label for="email_forgoten"   >Email   </label><input type="text" id="email_forgotten"   name="email"   /></p>
          <input type="submit" name="submit" value="Send password reminder"/>
        </fieldset>
      </form>
    </div>

  </div>

</%def>