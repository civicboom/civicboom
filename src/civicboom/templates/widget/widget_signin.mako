<%inherit file="./widget_content.mako"/>

<form action="FORM_ACTION${c.widget_query_string}" method="post">
  <fieldset><legend>Sign in</legend>
    <label for="username">Username</label><input type="text"     id="username" name="username" size="15" />
    <br/>
    <label for="password">Password</label><input type="password" id="password" name="password" size="15" />
    <br/>
    <input class="sign_submit" type="submit" name="submit" value="Sign in"/>
  </fieldset>
</form>

<form action="${h.url_for(controller='register', action='register_email')}${c.widget_query_string}" method="post">
  <fieldset><legend>Sign up</legend>
    <label for="username_register"     >Username</label><input type="text"  id="username_register"      name="username" size="15" />
    <br/>
    <label for="email_signup"          >Email   </label><input type="text"  id="email_signup"           name="email"    size="15" />
    <br/>
    
    ## Passthrough variables on signup
    
    ## Auto follow
    % if c.widget_reporter:
    <input type="hidden" name="refered_by" value="${c.widget_reporter.ReporterName}"/>
    %endif
    
    ## Auto accept - accept_assignment
    % if c.action == 'accept_assignment':
    <input type="hidden" name="${c.action}" value="${c.action_id}"/>
    % endif
    
    
    <input class="sign_submit" type="submit" name="submit" value="Sign up"/>
  </fieldset>
</form>

