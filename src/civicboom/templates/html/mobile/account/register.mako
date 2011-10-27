<%inherit file="/html/mobile/common/mobile_base.mako"/>


<%def name="title()">${_("Register")}</%def>

<%def name="body()">
    <div data-role="page">
        ${self.header()}
        
        <div data-role="content" id="register">
            
            ##${self.title_logo()}
            <h1>${_("Just a few more details and you'll be booming!")}</h1>

            <div id="reg_form">
                <form action="" method="post" data-ajax="false">
                    ## AllanC - Addition to show invalid states without the need to pass through the JS hide if the registration form is invalid - bit messy but works
                    <% help_type_invalid = c.result['status']=='invalid' and c.result['data']['invalid'].get('help_type') %>
                    % if c.result['status']!='invalid' or help_type_invalid:
                        ${help_type()}
                    % endif

                    ## AllanC - if we are not displaying the help selection - we still need to include the original selsection if it was valid
                    % if c.result['status']=='invalid' and not help_type_invalid:
                        <input type='hidden' name='help_type' value='${h.get_data_value('help_type','register')}'>
                    % endif

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
                    <div data-role="fieldcontain">
                        <input type="submit" name="submit" class="button" value="${_("Register")}"/>
                    </div>
                </form>
            </div>
       </div>
    </div>
</%def>

##------------------------------------------------------------------------------
## Optional Required component defs
##------------------------------------------------------------------------------

<%def name="invalid(field_name)">
    % if 'invalid' in c.result['data'] and field_name in c.result['data']['invalid']:
    <p class="error">${c.result['data']['invalid'][field_name]}</p>
    % endif
</%def>

<%def name="username()">
    <div data-role="fieldcontain">
        ${invalid('username')}
        <p>We could not allocate your preferred username as it has already been taken, if you have signed up once before check your email.</p>
        <label for="username"><b>Username</b></label>
        <input type="text" name="username" value="${h.get_data_value('username','register',c.logged_in_persona.username)}" />
    </div>
</%def>

<%def name="name()">
    <div data-role="fieldcontain">
        ${invalid('name')}
        <label for="name"><b>Display name</b></label>
        <input type="text" name="name" value="${h.get_data_value('name','register',c.logged_in_persona.name)}" />
    </div>
</%def>

<%def name="email()">
    <div data-role="fieldcontain">
        ${invalid('email')}
        <label for="email"><b>Email address</b></label>
        <input type="text" name="email" value="${h.get_data_value('email','register',c.logged_in_persona.email)}" />
    </div>
</%def>

<%def name="dob()">
    <%doc>
    <div data-role="fieldcontain">
        ${invalid('dob')}
        <label for="dob"><b>Date of birth</b></label>
        <input id="datepicker" type="date" name="dob"   value="${h.get_data_value('dob','register' ,c.logged_in_persona.config['dob'])}">
        <script type="text/javascript">
            $.datepicker.setDefaults({
                dateFormat: 'yy-mm-dd',
                changeYear: true,
                // maxDate:    '-18y',
            });
        </script>
        <small>Civicboom has age restrictions for some features, See <a href="/about/terms" target="_blank">Terms</a>.</small>
    </div>
    </%doc>
    <div data-role="fieldcontain">
        ${invalid('dob')}
        <label for="dob"><b>Date of birth</b> <small>(yyyy-mm-dd)</small></label>
        <input id="dob" name="dob" type="text" value="${h.get_data_value('dob','register','')}" />
    </div>
</%def>

<%def name="password()">
    <div data-role="fieldcontain">
        ${invalid('password')}
        <label for="password"><b>Password</b> <small>(Minimum of 5 characters)</small></label>
        <input type="password" name="password" value="" />
        <br />
        <label for="password_confirm"><b>Confirm password</b></label>
        <input type="password" name="password_confirm" value="" />
    </div>
</%def>

<%def name="captcha()">
    <div data-role="fieldcontain">
        ${invalid('recaptcha_response_field')}
        <label><b>${_("Show us that you're a real person")}</b></label>
        ${h.get_captcha(c.lang, 'white')}
    </div>
</%def>
            
<%def name="terms()">
    ## Terms and conditions checkbox
    <div data-role="fieldcontain">
        ${invalid('terms')}
        <fieldset data-role="controlgroup">
            <legend><b>Agree to <a href="/about/terms" data-rel="dialog" data-transition="fade">terms</a></b></legend>
            <input type="checkbox" name="terms" id="terms" />
            <label for="terms">I agree</label>
        </fieldset>
    </div>
</%def>

##------------------------------------------------------------------------------
## help_type - radio buttons
##------------------------------------------------------------------------------
<%def name="help_type()">
    <div data-role="fieldcontain">
        ${invalid('help_value')}
        <fieldset data-role="controlgroup">
            <legend><b>Choose a help type:</b></legend>
            <%
                radio_choices = {
                    'ind':[_('Individual'   ), False],
                    'org':[_('Organisation' ), False],
                }
                descriptions = {
                    'ind': _('Want to share your _articles? Got pictures, videos, audio clips or text and want to get them to the journalists, bloggers, publishers and news organisations who want them? This option is for you!'),
                    'org': _('Need _articles? Choose this option if you want to source news directly from your audience. News starts with the people, so use _site_name to get content from pictures and videos to audio clips and text!'),
                } 
            %>
            % for radio_key, (display_text, checked) in radio_choices.iteritems():
                <%
                    if checked:
                        checked = 'checked'
                %>
                <input type="radio" name="help_type" id="help_type_${radio_key}" value='${radio_key}' />
                <label for="help_type_${radio_key}">
                    ${display_text}
                    
                    <p><small>${descriptions[radio_key]}</small></p>
    
                </label>
            % endfor
        </fieldset>
        <small>${_("This will simply alter what guidance appears to you on the desktop website and will not affect any features!")}</small>
    </div>
</%def>
