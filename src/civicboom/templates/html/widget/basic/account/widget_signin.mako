<%inherit file="../common/widget_content.mako"/>


##------------------------------------------------------------------------------
## Janrain Login
##------------------------------------------------------------------------------

% if 'api_key.janrain' in config:
    ##% if int(c.widget_width) >= 420:
    ##    ${h.get_janrain(lang=c.lang)}
    ##% else:
        <a href="" onclick="return janrain_signin();">Sign in with other services</a>
        ${popup(h.get_janrain(lang=c.lang, popup_close=True), javascript_function_name='janrain_signin', title=_('Sign in to _site_name'), height=260, width=420)}
    ##% endif
% endif

<%doc>
<a href="" onclick="test(); return false;">Test</a>
${popup(h.literal("hello"), javascript_function_name='test', title=_('Test'), height=260, width=420)}
<a href="" onclick="t(); return false;">Test</a>
<script>
    window.status = "This message will display in the window status bar.";
    civicboom_window = window;
    function t() {
        YAHOO.log("t click");
        if (newwindow!=null) {
            YAHOO.log(newwindow);
            newwindow.focus();
            newwindow.location.reload(true);
        }
    }
</script>
</%doc>


##------------------------------------------------------------------------------
## Standard Login
##------------------------------------------------------------------------------

<form action="" method="post">
  <fieldset><legend>Sign in</legend>
    <label for="username">Username</label><input type="text"     id="username" name="username" size="15" />
    <br/>
    <label for="password">Password</label><input type="password" id="password" name="password" size="15" />
    <br/>
    <input class="sign_submit" type="submit" name="submit" value="Sign in"/>
  </fieldset>
</form>


##------------------------------------------------------------------------------
## Sign up
##------------------------------------------------------------------------------

<form action="${h.url(controller='register', action='email')}" method="post">
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
    <input type="hidden" name="${c.action}" value="${c.id}"/>
    % endif
    
    
    <input class="sign_submit" type="submit" name="submit" value="Sign up"/>
  </fieldset>
</form>



##------------------------------------------------------------------------------
## Popup window (used for janrain IFRAME as it is wider than the widget)
##------------------------------------------------------------------------------

<%def name="popup(popup_content, javascript_function_name='popup', title='popup', height=200, width=150)">
    ## Reference inspriation: http://www.quirksmode.org/js/popup.html
    <script language="javascript" type="text/javascript">
        function ${javascript_function_name}() {
            var newwindow = window.open('','${title}','height=${height}, width=${width}, left=400, top=200, status=False, location=False');
            ##newwindow.parent = window;
            var d = newwindow.document;
            d.write('<html><head><title>${title}</title>');
            d.write('</head><body>');
            d.write('${popup_content}');
            d.write('</body></html>');
            d.close();
            ## On close focus back on the parent frame and reload it
            newwindow.onunload = function(){
                ##alert('perform refresh to ${url(controller='account', action='login_redirect')}');
                ##focus();
                ##location.reload(true);
                ##history.go(0);
                ##window.parent.location.href = "${url(controller='account', action='login_redirect')}";
                ##window.parent.document.getElementById('CivicboomWidget').contentDocument.location.reload(true);
                ##alert(window.location.href);
                window.location.href = window.location.href+'&';
                ##window.location.reload(true);
                ##window.frames['frameNameOrIndex'].location.reload();
                ##alert(window.location.href);
                ##parent.CivicboomWidget.location.href = 'wwww.google.com';
            }
        }
    </script>
</%def>

