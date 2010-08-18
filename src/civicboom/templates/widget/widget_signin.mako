<%inherit file="./widget_content.mako"/>

<%
  authkit_form_action  = "FORM_ACTION" # A string that is replaced by the authkit system
  authkit_form_action += c.widget_query_string
%>

% if hasattr(c,'janrain_return_url'):
  <iframe src="http://civicboom.rpxnow.com/openid/embed?token_url=${c.janrain_return_url}&language_preference=${c.lang}"  scrolling="auto"  frameBorder="no"  allowtransparency="true"  style="width:400px;height:240px"></iframe>
  <% authkit_form_action = ""%>
% endif

<%doc>
<a class="rpxnow" onclick="return false;" href="https://civicboom.rpxnow.com/openid/v2/signin?token_url=http%3A%2F%2Flocalhost%2F"> Sign In Janrain</a> 
<script type="text/javascript">
  var rpxJsHost = (("https:" == document.location.protocol) ? "https://" : "http://static.");
  document.write(unescape("%3Cscript src='" + rpxJsHost + "rpxnow.com/js/lib/rpx.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
  RPXNOW.overlay = true;
  RPXNOW.language_preference = 'en';
</script>
</%doc>


##TESTING ONLY!!! REMOVE so authkit can degrade
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

<%def name="popup(popup_content, javascript_function_name='popup', title='popup2', height=200, width=150)">
    ## Reference: http://www.quirksmode.org/js/popup.html
    <script language="javascript" type="text/javascript">
        function ${javascript_function_name}() {
            var newwindow=window.open('','${title}','height=${height}, width=${width}, left=400, top=200, status=False, location=False');
            var tmp = newwindow.document;
            tmp.write('<html><head><title>${title}</title>');
            //tmp.write('<link rel="stylesheet" href="js.css">');
            tmp.write('</head><body>');
            tmp.write('${popup_content}');
            tmp.write('</body></html>');
            tmp.close();
        }
    </script>
</%def>

<a href="" onclick="return janrain_signin();">Link to popup</a>
${popup(h.get_janrain(lang=c.lang, popup_close=True), javascript_function_name='janrain_signin', title=_('Sign in to _site_name'), height=260, width=420)}


