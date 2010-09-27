<%inherit file="/web/html_base.mako"/>
<%def name="title()">${_("Welcome")}</%def>

<section class="signup">
	<form action="${h.url(controller='register', action='email', format='redirect')}" method="post">
		##<fieldset><legend>${_("Sign up today")}</legend>dd
		<p><label for="email"   >${_("Email")}   </label><input type="email" name="email"    placeholder="e.g. dave@coolnews.com"/></p>
		<p><label for="username">${_("Username")}</label><input type="text"  name="username" placeholder="e.g. dave23"/></p>
		<input class="signup_submit" type="submit" name="submit" value="${_("Sign up")}"/>
		##<p><label for="user_type_individual"  >${_("Individual")}  </label><input type="radio" id="user_type_individual"   name="user_type" value="individual"   checked='checked'/></p>
		##<p><label for="user_type_organisation">${_("Organisation")}</label><input type="radio" id="user_type_organisation" name="user_type" value="organisation"                  /></p>

		##</fieldset>
	</form>
</section>

