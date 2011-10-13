<%inherit file="/html/mobile/common/mobile_base.mako"/>


<%namespace name="signin_web_inlcudes"      file="/html/web/account/signin.mako" />

<%def name="title()">${_("Sign in")}</%def>

<%def name="body()">
    <div data-role="page">
        <div data-role="content">
            ${self.title_logo()}
    	    ${parent.flash_message()}
            
            ## AllanC - is this the correct place for this?
            ${signin_web_inlcudes.signin_actions()}
            
        	<div class="signin_title">
        	   <h1>${_("Sign in to _site_name!")}</h1>
        	</div>
	        ${signin()}
            % if config['development_mode']:
                <div class="signin_title">
                   <h1>${_("Don't have an account? Sign up to _site_name now!")}</h1>
                </div>
                ${signup()}
                <hr />
                ${janrain()}
            % endif
	   </div>
	</div>
</%def>

<%def name="signin()">
	<form action="${h.url('current', format='redirect')}" method="POST" data-ajax="false">
	    <div data-role="fieldcontain" data-theme="b">
			<label for="username">${_("Username")}</label>
			<input type="text" id="username" name="username" placeholder="e.g. dave43"/>
			<label for="password">${_("Password")}</label>
			<input  type="password" id="password" name="password" />
		</div>
        <div data-role="fieldcontain" data-theme="b">
		    <input class="button" type="submit" name="submit" value="${_("Sign in")}"/>
		</div>
	</form>
</%def>

<%def name="signup()">
    <form action="${h.url(controller='register', action='email', format='redirect')}" method="POST" data-ajaz="false">
        <div data-role="fieldcontain" data-theme="b">
            <label for="username_register">${_("Username")}</label>
            <input type="text" id="username_register" name="username" placeholder="e.g. dave43"/>
            <label for="email_signup">${_("Email")}</label>
            <input type="email" id="email_signup" name="email" placeholder="e.g. dave@coolnews.net"/>
        </div>
        <div data-role="fieldcontain" data-theme="b">
            <input class="button" type="submit" name="submit" value="${_("Sign up")}"/>
        </div>
    </form>
</%def>

## ----------------------------------------------------------------------------
## Janrain testing
## ----------------------------------------------------------------------------
<%def name="janrain()">
    % if 'api_key.janrain' in config:
        <section>
            % if config['online']:
                ${h.get_janrain(lang=c.lang)}
            % else:
                <img src="/images/test/janrain.png">
            % endif
        </section>
    % endif
</%def>