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
<div style="width:61em;margin:auto;text-align:left;">
	<h1>Just a few more details and you're done!</h1>
    <form action="" method="post">
		<table class="newform">
        % for field in c.required_fields:
            % if field=='username':
              ${username()}
            % endif
            % if field=='name':
              ${name()}
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
        
            ## help_type - radio buttons - this needs layout
            <tr>
                <td class="newformtitle">User type</td>
                <td>
                    <%
                        radio_choices = [
                            ('individual',_('Individual')  ),
                            ('org'       ,_('Organisation')),
                        ]
                    %>
                    % for radio_option, display_text in radio_choices:
                        <%
                            checked = ''
                            if h.get_data_value('help_type','register', default_value='individual') == radio_option:
                                checked = 'checked'
                        %>
                        <input type="radio" name="help_type" value='${radio_option}' ${checked} />${display_text}<br/>
                    % endfor
                </td>
        		<td>${invalid('help_type')}</td>
            </tr>
            
            ## Terms and conditions checkbox
			<tr>
				<td class="newformtitle">Agree to <a href="/about/terms" target="_blank">terms</a></td>
				<td><input type="checkbox" name="terms" value="checked" /></td>
        		<td>${invalid('terms')}</td>
			</tr>
            
            ## Submit button
			<tr>
				<td></td>
				<td><input type="submit" name="submit" class="button" value="${_("Register")}"/></td>
			</td>
		</table>
    </form>
</div>

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
    <p>We could not allocate your preferred username as it has already been taken, if you have signed up once before check your email.</p>
	<tr>
		<td class="newformtitle">Username</td>
		<td><input type="text" name="username" value="${h.get_data_value('username','register',c.logged_in_persona.username)}" /></td>
		<td>${invalid('username')}</td>
	</tr>
</%def>

<%def name="name()">
	<tr>
		<td class="newformtitle">Display name:</td>
		<td><input type="text" name="name" value="${h.get_data_value('name','register',c.logged_in_persona.name)}" /></td>
		<td>${invalid('name')}</td>
	</tr>
</%def>

<%def name="email()">
	<tr>
		<td class="newformtitle">Email address:</td>
		<td><input type="text" name="email" value="${h.get_data_value('email','register',c.logged_in_persona.email)}" /></td>
		<td>${invalid('email')}</td>
	</tr>
</%def>

<%def name="dob()">
  	<tr>
		<td class="newformtitle">Date of birth:</td>
		<td>
		  <input id="datepicker" type="date" name="dob"   value="${h.get_data_value('dob','register' ,c.logged_in_persona.config['dob'])}"><br />
		</td>
		<td>${invalid('dob')}</td>
	</tr>
  	<tr>
		<td class="newformtitle"></td>
		<td>
		   <b>${_('Please pick your YEAR and MONTH of birth BEFORE selecting the day.')}</b><br />
		   <span class="smaller">Civicboom has age restrictions for some features, See <a href="/about/terms" target="_blank">Terms</a>.</span>
		</td>
		<td></td>
	</tr>
</%def>

<%def name="password()">
  % if config['online']:
  <tr>
    <td style="vertical-align: middle;" class="newformtitle"> Please type the text in the box:</td>
		<td>${h.get_captcha(c.lang, 'white')}</td>
		<td>${invalid('recaptcha_response_field')}</td>
  </tr>
  % endif
  <tr>
		<td class="newformtitle">Password <span class="smaller">(minimum of 5 characters):</span></td>
		<td><input type="password" name="password"         value="" /></td>
		<td>${invalid('password')}</td>
  </tr>
  <tr>
		<td class="newformtitle">Confirm password:</td>
		<td><input type="password" name="password_confirm" value="" /></td>
		<td>${invalid('password_confirm')}</td>
  </tr>
</%def>


