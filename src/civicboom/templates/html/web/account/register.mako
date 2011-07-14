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
    ##style="width:61em;margin:auto;text-align:left;"
	<h1>Just a few more details and you'll be booming!</h1>
	
	
    <form action="" method="post">
	<table class="newform">
			
		## Guidence type
		${help_type()}
            
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
            <tr>
                <th>${_("Show us that you're a real person")} </th>
                <td>
                    ${h.get_captcha(c.lang, 'white')}
                    ##<br/>
                    ##<span class="smaller">${_('Please type the text in the box')}</span>'
                    ${invalid('recaptcha_response_field')}
                </td>
            </tr>
            % endif
            
            ## Terms and conditions checkbox
			<tr>
				<th>Agree to <a href="/about/terms" target="_blank">terms</a></th>
				<td>
                    <input type="checkbox" name="terms" value="checked" style="width: 16px;" />
                    ${invalid('terms')}
                </td>
			</tr>
            
            ## Submit button
			<tr>
				<td></td>
				<td>
                    <input type="submit" name="submit" class="button" value="${_("Register")}"/>
                </td>
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

##------------------------------------------------------------------------------
## help_type - radio buttons
##------------------------------------------------------------------------------
<%def name="help_type()">

    <%
        radio_choices = {
            'ind':[_('Individual')  , False],
            'org':[_('Organisation'), False],
        }
        # Iterate to set checked flag
        for radio_key, radio_tuple in radio_choices.iteritems():
            if h.get_data_value('help_type','register', radio_choices.keys()[0]) == radio_key:
                radio_tuple[1] = True
        
    %>

    <tr>
        <th>
		## <p class="step">1.</p>
		${_('Do you...')}
        </th>
        <td style="width: 750px;">
            
            
            ##<p>${_('To help you make the best of _site_name, please tell us if ... ')}</p>
            
            <div class="user_type_option ${'selected' if radio_choices['ind'][1] else ''}" onclick="$('#help_type_ind').click(); $(this).parent().children().removeClass('selected'); $(this).addClass('selected')">
                <img src="/images/default/thumbnail_response.png" alt="response"/>
                
                <h2 class="newformtitle">${_('have _articles?')}</h2>
                <p>${_('People like you are the eyes and ears of the news.')}</p>
                <p>${_('Everyone has a story and now you have an outlet to share it with the world.')}</p>
                
                <%doc>
                <div class="hideable">
                    <p>${_('You can get your stories directly to journalists, news organisations and media outlets in three ways:')}</p>
                    
                    <ol>
                        <li>${_('Respond to their _assignments for your news stories by Following them on _site_name')}</li>
                        <li>${_('Upload your _articles directly to your chosen journalists, publications and news organisations via the _widget - as video, images, audio... as it happens.')}</li>
                        <li>${_('Grab the mobile app and share your stories from source, out in the field directly as it happens.')}</li>
                    </ol>
                </div>
                </%doc>
                <span class="icon16 i_accept"></span>
            </div>
            <div class="or"><p>or</p></div>
            <div class="user_type_option ${'selected' if radio_choices['org'][1] else ''}" onclick="$('#help_type_org').click(); $(this).parent().children().removeClass('selected'); $(this).addClass('selected')">
                <img src="/images/default/thumbnail_assignment.png" alt="request"/>
                <h2 class="newformtitle">${_('want _articles?')}</h2>
                <p>${_('Journalists, blogger, publishers, news organisations.')}</p>
                <p>${_('Your greatest resource is your audience.')}</p>
                <p>${_('After all, news stories start with people - and now you have a tool to tap into those stories.')}</p>
                
                <%doc>
                <div class="hideable">
                    <p>${_('You can get stories directly from your audience in two ways:')}
                    
                    <ol>
                        <li>${_('Post requests for _articles - they are automatically pushed to your _widget and Followers as alerts for them to respond to')}</li>
                        <li>${_('Add the _widget to your site - get video, images, audio from your audience')}</li>
                        <li>${_('Push the mobile app to your users - get news from source, out in the field directly as it happens')}</li>
                    </ol>
                </div>
                </%doc>
                
                <span class="icon16 i_accept"></span>
            </div>
            
            ##<div style="clear:both;"></div>
            
            ##<p>${_('Help shape the news and together make it relevant and meaningful. ')}</p>
            
            ##<p>${_('Why do I need to choose?')}</p>
            ##<p>${_("There are different ways in which you can use _site_name - so to make sure you get the right kind of hand holding as you navigate and learn how to use _site_name we need to know whether you're going to be responding to _assignments for _articles, or asking for _articles. ")}</p>
            
            ## Radio buttons - hidden if js is enabled
            <div class="hide_if_js">
                % for radio_key, (display_text, checked) in radio_choices.iteritems():
                    <%
                        checked = ''
                        if checked:
                            checked = 'checked'
                    %>
                    <input id="help_type_${radio_key}" type="radio" name="help_type" value='${radio_key}' ${checked} />${display_text}<br/>
                % endfor
            </div>
            ${invalid('help_value')}
        </td>
    </tr>




</%def>

