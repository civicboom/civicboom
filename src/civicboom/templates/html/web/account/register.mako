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
<div class="page_border">
    ##style="width:61em;margin:auto;text-align:left;"
	<h1>Just a few more details and you'll be all set!</h1>
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
        
            ## Terms and conditions checkbox
			<tr>
				<td class="newformtitle">Agree to <a href="/about/terms" target="_blank">terms</a></td>
				<td><input type="checkbox" name="terms" value="checked" /></td>
        		<td>${invalid('terms')}</td>
			</tr>
            
            ${help_type()}
            
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

##------------------------------------------------------------------------------
## help_type - radio buttons
##------------------------------------------------------------------------------
<%def name="help_type()">

    
    <%doc>
    <tr>
        <td class="newformtitle">User type</td>
        <td>

        </td>
        <td>${invalid('help_type')}</td>
    </tr>
    </%doc>

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
        <td colspan="3">
            
            
            ##<p>${_('To help you make the best of _site_name, please tell us if ... ')}</p>
            <p>${_('Let us know how to help you ...')}</p>
            
            <div class="user_type_option ${'selected' if radio_choices['ind'][1] else ''}" style="float:left;" onclick="$('#help_type_ind').click(); $(this).parent().children().removeClass('selected'); $(this).addClass('selected')">
                ##<img src="/images/default/avatar.png" alt="individual"/><p>Individuals</p>
                
                <h2 class="newformtitle">${_('I have _articles:')}</h2>
                <p>${_('People like you are the eyes and ears of the news. Everyone has a story and now you have an outlet to share it with the world: _site_name.')}</p>
                
                <div class="hideable">
                    <p>${_('You can get your stories directly to journalists, news organisations and media outlets in three ways:')}</p>
                    
                    <ol>
                        <li>${_('Respond to their _assignments for your news stories by Following them on _site_name')}</li>
                        <li>${_('Upload your _articles directly to your chosen journalists, publications and news organisations via the _widget - as video, images, audio... as it happens.')}</li>
                        <li>${_('Grab the mobile app and share your stories from source, out in the field directly as it happens.')}</li>
                    </ol>
                </div>
            </div>
            
            <div class="user_type_option ${'selected' if radio_choices['org'][1] else ''}" style="float:right;" onclick="$('#help_type_org').click(); $(this).parent().children().removeClass('selected'); $(this).addClass('selected')">
                ##<img src="/images/default/avatar_group.png" alt="group"/><p>Organisations</p>
                <h2 class="newformtitle">${_('I want _articles:')}</h2>
                <p>${_('Journalists, blogger, publishers, news organisations - your greatest resource is your audience. After all, news stories start with people - and now you have a tool to tap into those stories: _site_name.')}
                
                <div class="hideable">
                    <p>${_('You can get stories directly from your audience in two ways:')}
                    
                    <ol>
                        <li>${_('Post requests for _articles - they are automatically pushed to your _widget and Followers as alerts for them to respond to')}</li>
                        <li>${_('Add the _widget to your site - get video, images, audio from your audience')}</li>
                        <li>${_('Push the mobile app to your users - get news from source, out in the field directly as it happens')}</li>
                    </ol>
                </div>
            </div>
            
            <div style="clear:both;"></div>
            
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
        </td>
    </tr>




</%def>

