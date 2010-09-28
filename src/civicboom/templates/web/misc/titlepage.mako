<%inherit file="/web/html_base.mako"/>
<%def name="title()">${_("Welcome")}</%def>

<section class="signup">
	<form action="${h.url(controller='register', action='email', format='redirect')}" method="post">
		##<fieldset><legend>${_("Sign up today")}</legend>dd
		<p>
			<label for="username">${_("Username")}</label>
			<br><input type="text"  name="username" placeholder="e.g. dave23"/>
		</p>
		<p>
			<label for="email">${_("Password")}</label>
			<br><input type="password" name="password" placeholder=""/>
		</p>
		<p>
			<label for="email">${_("Email")}</label>
			<br><input type="email" name="email" placeholder="e.g. dave@coolnews.com"/>
		</p>
		<p>
			<label for="user_type_individual">${_("Author")}</label>
			<input type="radio" id="user_type_individual" name="user_type" value="individual" checked='checked'/>
			<label for="user_type_organisation">${_("Mediator")}</label>
			<input type="radio" id="user_type_organisation" name="user_type" value="organisation"/>
		</p>
		<p>
			<input class="signup_submit" type="submit" name="submit" value="${_("Sign up")}"/>
		</p>

		##</fieldset>
	</form>
</section>

<section class="blurb">
Civicboom is waffle waffle waffle
</section>

