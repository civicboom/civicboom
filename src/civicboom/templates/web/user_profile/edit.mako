<%inherit file="/web/html_base.mako"/>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="settings_general()">
<fieldset>
	<legend>${_("General Info")}</legend>
		Display name: <input name="name" value="${c.viewing_user.name}">
	<br>Home Location: <input name="location" value="${c.viewing_user.config["location"]}">
	<br>Description: <textarea name="description">${c.viewing_user.config["description"]}</textarea>
	<br>Home page: <input name="home_page" value="${c.viewing_user.config["home_page"]}">
</fieldset>
</%def>

<%def name="settings_email()">
<fieldset>
	<legend>${_("Email Address")}</legend>
		Address: <input name="email" value="${c.viewing_user.email}">
</fieldset>
</%def>

<%def name="settings_login()">
<fieldset>
	<legend>${_("Login Details")}</legend>
		Current password: <input name="current_password" type="password">
	<br>New password: <input name="new_password_1" type="password">
	<br>Repeat new password: <input name="new_password_2" type="password">
	<br>&nbsp;
	<br><a href="">Link with Google, Facebook, etc</a>
</fieldset>
</%def>

<%def name="settings_aggregation()">
<fieldset>
	<legend>${_("Aggregation")}</legend>
		Twitter username: <input name="twitter_username" value="${c.viewing_user.config["twitter_username"]}">
	<br>Twitter auth key: <input name="twitter_auth_key" value="${c.viewing_user.config["twitter_auth_key"]}">
	<br>Broadcast instant news: <input type="checkbox" name="broadcast_instant_news" value="${c.viewing_user.config["broadcast_instant_news"]}">
	<br>Broadcast content posts: <input type="checkbox" name="broadcast_content_posts" value="${c.viewing_user.config["broadcast_content_posts"]}">
</fieldset>
</%def>

<%def name="settings_avatar()">
<fieldset>
	<legend>${_("Avatar")}</legend>
% if c.viewing_user.config["avatar"]:
	Civicboom no longer manages user avatars itself, we now link to Gravatar, a service for
	letting users keep their avatars consistent all across the internet. We're keeping old
	avatars active while people switch over, but recommend switching.
	<p>Move to <a href="http://www.gravatar.com/">Gravatar</a>? <input type="checkbox" name="move_to_gravatar">
% else:
	Manage your avatar with <a href="http://www.gravatar.com">gravatar.com</a>
% endif
</fieldset>
</%def>

<%def name="body()">
<style>
#user_settings TD {
	padding: 8px;
	vertical-align: top;
}
#user_settings FIELDSET {
	margin-bottom: 16px;
	border: 1px solid black;
	border-radius: 8px;
	padding: 8px;
}
#user_settings FIELDSET LEGEND {
	padding-left: 4px;
	padding-right: 4px;
}
</style>
<form action="${url.current(action='save', id=c.viewing_user.username)}" method="POST">
	<input type="hidden" name="_authentication_token" value="${h.authentication_token()}">
	<table id="user_settings"><tr>
		<td class="avatar">
			<img class="avatar" src="${c.viewing_user.avatar_url}">
			<br>${c.viewing_user.name}
			<br>(${c.viewing_user.username})
		</td>
		<td>
			${settings_general()}
			${settings_email()}
			${settings_login()}
		</td>
		<td>
			${settings_aggregation()}
			${settings_avatar()}
		</td>
	</tr>
		<tr>
			<td></td>
			<td colspan="2"><input type="submit" value="Save" style="width: 100%"></td>
		</tr>
	</table>
</form>
</%def>
