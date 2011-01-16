<%inherit file="/web/common/html_base.mako"/>
<%def name="title()">${_("Sign in")}</%def>

<style>
</style>
<table class="signin">
	<tr>
		<td width="45%">
			${signin()}
		</td>
		<td width="10%" rowspan="3">
			<b>or &rarr;</b>
		</td>
		<td width="45%" rowspan="3">
			${janrain()}
		</td>
	</tr>
	<tr>
		<td class="block">
			${forgot()}
		</td>
	</tr>
	<tr>
		<td class="block">
			${signup()}
		</td>
	</tr>
</table>



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

<%def name="signin()">
<section>
	<h1>${_("Sign in")}</h1>
	<form action="${url.current(format='redirect')}" method="POST">
		<table class="form">
			<tr>
				<td width="50"><label for="username">${_("Username")}</label></td>
				<td><input type="text"     id="username" name="username" placeholder="e.g. dave43"/></td>
			</tr>
			<tr>
				<td><label for="password">${_("Password")}</label></td>
				<td><input type="password" id="password" name="password" /></td>
			</tr>
			<tr>
				<td></td>
				<td><input class="button" type="submit" name="submit" value="${_("Sign in")}"/></td>
			</tr>
		</table>
	</form>
</section>
</%def>

<%def name="signup()">
<section>
	<h1>${_("Sign up (It's free!)")}</h1>
	<form action="${h.url(controller='register', action='email', format='redirect')}" method="post">
		<table class="form">
			<tr>
				<td width="50"><label for="username_register">${_("Username")}</label></td>
				<td><input type="text" id="username_register" name="username" placeholder="e.g. dave43"/></td>
			</tr>
			<tr>
				<td><label for="email_signup">${_("Email")}</label></td>
				<td><input type="email" id="email_signup" name="email" placeholder="e.g. dave@coolnews.net"/></td>
			</tr>
			<tr>
				<td></td>
				<td><input class="button" type="submit" name="submit" value="${_("Sign up")}"/></td>
			</tr>
		</table>
	</form>
</section>
</%def>

<%def name="forgot()">
<section>
	<a class="button" style="float: right; margin: 16px;" href="#" onclick="$('#reminder').show('slow');">Forgotten your password?</a>
	
	<div id="reminder" class="hideable">
	<form action="${h.url(controller='account', action='forgot_password', format='redirect')}" method="post" style="clear:both">
		<table class="form">
			<tr>
				<td width="50"><label for="username_forgotten">${_("Username")}</label></td>
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
				<td></td>
				<td><input class="button" type="submit" name="submit" value="${_("Send password reminder")}"/></td>
			</tr>
		</table>
	</form>
	</div>
</section>
</%def>
