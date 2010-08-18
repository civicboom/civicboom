<%inherit file="./widget_content.mako"/>

<%
  authkit_form_action  = "FORM_ACTION" # A string that is replaced by the authkit system
  authkit_form_action += c.widget_query_string
%>

% if hasattr(c,'janrain_return_url'):
  <iframe src="http://civicboom.rpxnow.com/openid/embed?token_url=${c.janrain_return_url}&language_preference=${c.lang}"  scrolling="no"  frameBorder="no"  allowtransparency="true"  style="width:400px;height:240px"></iframe>
  <% authkit_form_action = ""%>
% endif

## FOR TESTING, to be removeed to maintain authkit backwards compatability
<% authkit_form_action = ""%>

<form action="${authkit_form_action}" method="post">
  <fieldset><legend>Sign in</legend>
    <label for="username">Username</label><input type="text"     id="username" name="username" size="15" />
    <br/>
    <label for="password">Password</label><input type="password" id="password" name="password" size="15" />
    <br/>
    <input class="sign_submit" type="submit" name="submit" value="Sign in"/>
  </fieldset>
</form>

<form action="${h.url_from_widget(controller='register', action='email')}" method="post">
  <fieldset><legend>Sign up</legend>
    <label for="username_register"     >Username</label><input type="text"  id="username_register"      name="username" size="15" />
    <br/>
    <label for="email_signup"          >Email   </label><input type="text"  id="email_signup"           name="email"    size="15" />
    <br/>
    
    ## Passthrough variables on signup
    
    ## Auto follow
    % if c.widget_owner:
    <input type="hidden" name="refered_by" value="${c.widget_owner.username}"/>
    %endif
    
    ## Auto accept - accept_assignment
    % if c.action == 'accept':
    <input type="hidden" name="${c.action}" value="${c.action_id}"/>
    % endif
    
    
    <input class="sign_submit" type="submit" name="submit" value="Sign up"/>
  </fieldset>
</form>

