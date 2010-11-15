<%inherit file="/web/common/html_base.mako"/>
<%def name="title()">${_("Sign in")}</%def>

<table class="signin">
	<tr>
		<td class="block">
			${signin()}
		</td>
		<td class="block" rowspan="3">
			${janrain()}
		</td>
	</tr>
	<tr>
		<td>
			------------- or -------------
		</td>
	</tr>
	<tr>
		<td class="block">
			${signup()}
		</td>
	</tr>
	<tr>
		<td class="block">
			${forgot()}
		</td>
	</tr>
</table>



<%def name="janrain()">
% if 'api_key.janrain' in config:
<section>
	${h.get_janrain(lang=c.lang)}
</section>
% endif
</%def>

<%def name="signin()">
<section>
	<form action="${url.current(format='redirect')}" method="post">
		<table class="form">
			<tr>
				<th colspan="2">${_("Sign in")}</th>
			</tr>
			<tr>
				<td><label for="username">${_("Username")}</label></td>
				<td><input type="text"     id="username" name="username" placeholder="e.g. dave43"/></td>
			</tr>
			<tr>
				<td><label for="password">${_("Password")}</label></td>
				<td><input type="password" id="password" name="password" /></td>
			</tr>
			<tr>
				<td colspan="2"><input type="submit" name="submit" value="${_("Sign in")}"/></td>
			</tr>
		</table>
	</form>
</section>
</%def>

<%def name="signup()">
<section>
	<form action="${h.url(controller='register', action='email', format='redirect')}" method="post">
		<table class="form">
			<tr>
				<th colspan="2">${_("Sign up")}</th>
			</tr>
			<tr>
				<td><label for="username_register">${_("Username")}</label></td>
				<td><input type="text" id="username_register" name="username" placeholder="e.g. dave43"/></td>
			</tr>
			<tr>
				<td><label for="email_signup">${_("Email")}</label></td>
				<td><input type="email" id="email_signup" name="email" placeholder="e.g. dave@coolnews.net"/></td>
			</tr>
			<tr>
				<td colspan="2">
					<label for="user_type_individual">${_("Individual")}</label> <input type="radio" id="user_type_individual"   name="user_type" value="individual"   checked='checked'/>
					<label for="user_type_organisation">${_("Organisation")}</label> <input type="radio" id="user_type_organisation" name="user_type" value="organisation"                  />
				</td>
			</tr>
			<tr>
				<td colspan="2"><input type="submit" name="submit" value="${_("Sign up")}"/></td>
			</tr>
		</table>
	</form>
</section>
</%def>

<%def name="forgot()">
<section>
	<form action="${h.url(controller='account', action='forgot_password_reminder', format='redirect')}" method="post">
		<table class="form">
			<tr>
				<th colspan="2">${_("Forgotten Password?")}</th>
			</tr>
			<tr>
				<td><label for="username_forgotten">${_("Username")}</label></td>
				<td><input type="text"  id="username_forgotten" name="username" placeholder="e.g. dave43"/></td>
			</tr>
			<tr>
				<td colspan="2"><label>or</label></td>
			</tr>
			<tr>
				<td><label for="email_forgotten">${_("Email")}</label></td>
				<td><input type="email" id="email_forgotten" name="email" placeholder="e.g. dave@coolnews.net"/></td>
			</tr>
			<tr>
				<td colspan="2"><input type="submit" name="submit" value="${_("Send password reminder")}"/></td>
			</tr>
		</table>
	</form>
</section>
</%def>
