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
<div class="layout page_border">
	<h1>Just a few more details and you'll be booming!</h1>
	
	<div id="reg_form">
    <form action="" method="post">
        ${help_type()}
        <table class="newform user hide_if_js">
            
            <tr><td colspan="2">
                <p class="step">2. Fill in the following:</p>
            </td></tr>
            % if 'username' in c.required_fields:
              ${username()}
            % endif
            % if 'name' in c.required_fields:
              ${name()}
            % endif
            % if 'email' in c.required_fields:
              ${email()}
            % endif
            % if 'password' in c.required_fields:
              ${password()}
            % endif
            % if 'dob' in c.required_fields:
              ${dob()}
            % endif
            ## recaptcha - if login account is not janrain
            % if config['online'] and 'password' in c.required_fields:
              ${captcha()}
            % endif
            % if True:
              ${terms()}
            % endif
            
            ## Submit button
			<tr>
				<td></td>
				<td>
                    <p class="button" id="user_details_back"><a>Back</a></p>
                    <input type="submit" name="submit" class="button" value="${_("Register")}"/>
                </td>
			</td>
		</table>
    </form>
    </div>
    
    <script type="text/javascript">
        help_type_error = $('#help_type_continue').parent().find('.error');
        $('#help_type_continue').click(function() {
            if (!$('#help_type_ind').is(':checked') && !$('#help_type_org').is(':checked')) {
                help_type_error.slideDown();
            } else {
                help_type_error.slideUp();
                $('.newform.help').fadeOut(function() {
                    $('.newform.user').fadeIn();
                });
            }
        });
        
        $('#user_details_back').click(function() {
            $('.newform.user').fadeOut(function() {
                $('.newform.help').fadeIn();
            });
        });
    </script>
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
		<th>Username</th>
		<td>
            <input type="text" name="username" value="${h.get_data_value('username','register',c.logged_in_persona.username)}" />
            ${invalid('username')}
        </td>
	</tr>
</%def>

<%def name="name()">
	<tr>
		<th>Display name</th>
		<td>
            <input type="text" name="name" value="${h.get_data_value('name','register',c.logged_in_persona.name)}" />
            ${invalid('name')}
        </td>
	</tr>
</%def>

<%def name="email()">
	<tr>
		<td class="newformtitle">Email address:</td>
		<td>
            <input type="text" name="email" value="${h.get_data_value('email','register',c.logged_in_persona.email)}" />
            ${invalid('email')}
        </td>
	</tr>
</%def>

<%def name="dob()">
  	<tr>
		<th>Date of birth</th>
		<td>
            <input id="datepicker" type="date" name="dob"   value="${h.get_data_value('dob','register' ,c.logged_in_persona.config['dob'])}">
            <p class="smaller">${_('Please pick your YEAR and MONTH of birth BEFORE selecting the day.')}</p>
            <p class="smaller">Civicboom has age restrictions for some features, See <a href="/about/terms" target="_blank">Terms</a>.</p>
            ${invalid('dob')}
		</td>
	</tr>
</%def>

<%def name="password()">
    <tr>
		<th>Password</th>
		<td>
            <input type="password" name="password"         value="" />
            <br/>
            <p class="smaller">(minimum of 5 characters):</p>
            ${invalid('password')}
        </td>
    </tr>
    <tr>
		<th>Confirm password</th>
		<td>
            <input type="password" name="password_confirm" value="" />
            ${invalid('password_confirm')}
        </td>
    </tr>
</%def>

<%def name="captcha()">
    <tr>
        <th>${_("Show us that you're a real person")}</th>
        <td>
            ${h.get_captcha(c.lang, 'white')}
            ##<br/>
            ##<span class="smaller">${_('Please type the text in the box')}</span>'
            ${invalid('recaptcha_response_field')}
        </td>
    </tr>
</%def>
            
<%def name="terms()">
    ## Terms and conditions checkbox
    <tr>
        <th>Agree to <a href="/about/terms" target="_blank">terms</a></th>
        <td>
            <input type="checkbox" name="terms" value="checked" style="width: 16px;" />
            ${invalid('terms')}
        </td>
    </tr>
</%def>

##------------------------------------------------------------------------------
## help_type - radio buttons
##------------------------------------------------------------------------------
<%def name="help_type()">
<%
    radio_choices = {
        'ind':[_('Individual')  , False],
        'org':[_('Organisation'), False],
    }
%>
<table class="newform help" style="margin: auto;">
    <tr>
        <td>${invalid('help_type')}</td>
    </tr>
    <tr>
        <td>
            <div class="user_type_option">
                <img src="/images/default/thumbnail_response.png" alt="response"/>
                
                <h2 class="newformtitle">${_('Want to share your _articles?')}</h2>
                <b>${_('Are you the eyes and ears of your community?')}</b>
                <ul>
                    <li>${_('Everyone has stories - _site_name makes it easy to share them with the world')}</li>
                    <li>${_('Got pictures, videos, audio clips or text? Journalists, bloggers, publishers and news organisations want them!')}</li>
                </ul>

                <input class="button" style="width: 100%" type="button" name="help_type" value="I want to share my stories">
            </div>
            <div class="or"></div>
            <div class="user_type_option">
                <img src="/images/default/thumbnail_assignment.png" alt="request"/>
                <h2 class="newformtitle">${_('Need _articles?')}</h2>
                <b>${_('Journalists, bloggers, publishers and news organisations:')}</b>
                <ul>
                    <li>${_('Your greatest resource is your audience because news starts with people')}</li>
                    <li>${_('So use _site_name to get content - from pictures and videos to audio clips and text - directly from source!')}</li>
                </ul>
                <input class="button" style="width: 100%" type="button" name="help_type" value="I want to find stories">
            </div>
            
            <div class="hide_if_js">
                % for radio_key, (display_text, checked) in radio_choices.iteritems():
                    <%
                        if checked:
                            checked = 'checked'
                    %>
                    <input id="help_type_${radio_key}" type="radio" name="help_type" value='${radio_key}' ${checked} />${display_text}<br/>
                % endfor
            </div>
            ${invalid('help_value')}
        </td>
    </tr>
    <tr>
        <td style="text-align: center;"><span id="help_type_continue">If you just want to explore, click here to continue without guides</span></td>
    </tr>
</table>
</%def>
