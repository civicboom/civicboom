<%inherit file="/web/html_base.mako"/>
<%def name="title()">${_("Sign in")}</%def>

% if 'api_key.janrain' in config:
<section>
	${h.get_janrain(lang=c.lang)}
</section>
% endif

<div class="cols">
<section>
	<form action="" method="post">
		<fieldset><legend>${_("Sign in")}</legend>
			<p><label for="username">${_("Username")}</label><input type="text"     id="username" name="username" placeholder="e.g. dave43"/></p>
			<p><label for="password">${_("Password")}</label><input type="password" id="password" name="password"                          /></p>
			<input type="submit" name="submit" value="${_("Sign in")}"/>
		</fieldset>
	</form>
</section>

<section>
	<form action="${h.url(controller='register', action='email')}" method="post">
		<fieldset><legend>${_("Sign up")}</legend>
			<p><label for="username_register"     >${_("Username")}    </label><input type="text"  id="username_register"      name="username" placeholder="e.g. dave43"/></p>
			<p><label for="email_signup"          >${_("Email")}       </label><input type="email" id="email_signup"           name="email"    placeholder="e.g. dave@coolnews.net"/></p>
			<p>
				<label for="user_type_individual"  >${_("Individual")}  </label><input type="radio" id="user_type_individual"   name="user_type" value="individual"   checked='checked'/>
				<label for="user_type_organisation">${_("Organisation")}</label><input type="radio" id="user_type_organisation" name="user_type" value="organisation"                  />
			</p>
			##<input type="hidden" name="user_type" value="organisation"/>
			<input type="submit" name="submit" value="${_("Sign up")}"/>
		</fieldset>
	</form>
</section>

<section>
	<form action="${h.url(controller='account', action='forgot_password_reminder')}" method="post">
		<fieldset><legend>${_("Forgotten Password?")}</legend>
			<p><label for="username_forgotten">${_("Username")}</label><input type="text"  id="username_forgotten" name="username" placeholder="e.g. dave43"/></p>
			<p><label>or</label></p>
			<p><label for="email_forgotten"   >${_("Email")}   </label><input type="email" id="email_forgotten"    name="email"    placeholder="e.g. dave@coolnews.net"/></p>
			<input type="submit" name="submit" value="${_("Send password reminder")}"/>
		</fieldset>
	</form>
</section>
</div>
