<%inherit file="/html/web/common/html_base.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">${_("Register")}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">

##    % if 'invalid' in c.result['data']:
##    <p>INVALID:</p>
##    <pre>${c.result['data']['invalid']}</pre>
##    % endif

    <form action="" method="post">
		<table class="form">
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
			<tr>
				<td>Agree to <a href="/about/terms" target="_blank">terms</a></td>
				<td><input type="checkbox" name="terms" value="checked" /></td>
        		<td>${invalid('terms')}</td>
			</tr>
			<tr>
				<td></td>
				<td><input type="submit" name="submit" class="button" value="${_("Register")}"/></td>
			</td>
		</table>
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
	<tr>
		<td>Username</td>
		<td><input type="text" name="username" value="${h.get_data_value('username','register',c.logged_in_persona.username)}" /></td>
		<td>${invalid('username')}</td>
	</tr>
</%def>

<%def name="email()">
	<tr>
		<td>Email Address</td>
		<td><input type="text" name="email" value="${h.get_data_value('email','register',c.logged_in_persona.email)}" /></td>
		<td>${invalid('email')}</td>
	</tr>
</%def>

<%def name="dob()">
  <tr>
		<td>Date of Birth</td>
		<td>
		  <input id="datepicker" type="date" name="dob"   value="${h.get_data_value('dob','register' ,c.logged_in_persona.config['dob'])}"><br />
		  ${_('Please pick your year and month of birth before selecting the day.')}
		</td>
		<td>${invalid('dob')}</td>
	</tr>
</%def>

<%def name="password()">
  <tr>
    <td style="vertical-align: middle;">Please type the text in the image</td>
		<td>${h.get_captcha(c.lang, 'white')}</td>
		<td>${invalid('recaptcha_response_field')}</td>
  </tr>
    <tr>
		<td>Password</td>
		<td><input type="password" name="password"         value="" /></td>
		<td>${invalid('password')}</td>
  </tr>
  <tr>
		<td>Password Confirm</td>
		<td><input type="password" name="password_confirm" value="" /></td>
		<td>${invalid('password_confirm')}</td>
  </tr>
</%def>


