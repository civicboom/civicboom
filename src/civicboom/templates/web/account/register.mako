<%inherit file="/web/common/html_base.mako"/>

<%namespace name="YUI" file="/web/common/YUI_components.mako" />

##------------------------------------------------------------------------------
## Additional CSS and Javascripts
##------------------------------------------------------------------------------
##<%def name="head_links()">
##    ${parent.head_links()}
  
    <!-- Additional YUI imports-->
    ##<link   type="text/css"        href="http://yui.yahooapis.com/2.8.1/build/calendar/assets/skins/sam/calendar.css" rel="stylesheet" />
    ##<script type="text/javascript" src ="http://yui.yahooapis.com/2.8.1/build/calendar/calendar-min.js"></script>

    ##<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.8.1/build/button/assets/skins/sam/button.css" />
    ##<script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/container/container_core-min.js"></script>
    ##<script type="text/javascript" src="http://yui.yahooapis.com/2.8.1/build/button/button-min.js"></script>
##</%def>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">${_("Register")}</%def>


##------------------------------------------------------------------------------
## Style Overrides
##------------------------------------------------------------------------------
##<%def name="styleOverides()">
##</%def>



##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">

    % if 'invalid' in c.result['data']:
    <p>INVALID:</p>
    <pre>${c.result['data']['invalid']}</pre>
    % endif

    <form action="" method="post">
        % for field in c.required_fields:
            % if field=='username':
              ${username()}
            % endif
            % if field=='email':
              ${email()}
            % endif
            % if field=='dob':
              ${dob()}
            % endif
            % if field=='password':
              ${password()}
            % endif
            ##${eval(field)} wanted to just eval the field name but mako defs use differnt python names :( it's going to have to be a set of IF's
            

        % endfor
        <input type="checkbox" name="terms" value="checked" />${_("Agree to terms")}
        ${invalid('terms')}
        <input type="submit" name="submit" value="${_("Register")}"/>
    </form>

</%def>

##------------------------------------------------------------------------------
## Optional Required component defs
##------------------------------------------------------------------------------



<%def name="invalid(field_name)">
    % if 'invalid' in c.result['data'] and field_name in c.result['data']['invalid']:
    <span class="error">${c.result['data']['invalid'][field_name]}</span>
    % endif
</%def>

<%def name="username()">
    <p>could not allocate your prefered username as it has already been taken, if you are xxx then you can link accounts</p>
    Username<input type="text" name="username" value="${h.get_data_value('username','register',c.logged_in_persona.username)}" />
    ${invalid('username')}
</%def>

<%def name="email()">
    email<input type="text" name="email" value="${h.get_data_value('email','register',c.logged_in_persona.email)}" />
    ${invalid('email')}
</%def>

<%def name="dob()">
    <script>
        $(function() {$( "#datepicker" ).datepicker();});
    </script>
    <p>Date of Birth:<input id="datepicker" type="date" name="dob"   value="${h.get_data_value('dob','register' ,c.logged_in_persona.config['dob'])}"></p>
    ${invalid('dob')}
    ##${YUI.calendar(form_field_name='dob')}
</%def>

<%def name="password()">
  ${h.get_captcha(c.lang, 'white')}
  ${invalid('recaptcha_response_field')}
  
  password<input type="password" name="password"         value="" />
  password confirm<input type="password" name="password_confirm" value="" />
  ${invalid('password')}
  ${invalid('password_confirm')}
</%def>


