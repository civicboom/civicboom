<%inherit file="/web/common/layout_2cols.mako"/>

<%namespace name="private_profile" file="/web/profile/index.mako"/>

##------------------------------------------------------------------------------
## Side Col
##------------------------------------------------------------------------------

<%def name="col_side()">${private_profile.col_left()}</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    ${h.form(h.url('setting', id='None'), method='put')}
    % for group_name in d.keys():
        <fieldset><legend>${group_name.capitalize()}</legend>
            % for field in d[group_name]:
                <p>
                    ${field['description']} :
                    % if 'type' not in field:
                        <input name="${field['name']}" value="${field['value']}">
                    % elif field['type'] == 'boolean':
                        <%
                            checked = None
                            if field['value']: checked="checked='%s'" % field['value']
                        %>
                        <input name="${field['name']}" value="True" type='checkbox' ${checked}>
                    % elif field['type'] == 'password':
                        <input name="${field['name']}" type="password" />
                    % endif
                ##% for key in field.keys():
                ##    <p>${key}</p>
                ##% endfor
                % if field.get('error'):
                    <span class="error-message">${field['error']}</span>
                % endif
                </p>
            % endfor
        </fieldset>
    % endfor
    <input type="submit" name="submit" value="${_('Save settings')}"/>
    ${h.end_form()}
</%def>


##------------------------------------------------------------------------------
## Setting Sections and renderers - OLD DEPRICATED
##------------------------------------------------------------------------------

<%doc>

<%def name="settings_general()">
<fieldset>
	<legend>${_("General Info")}</legend>
	<table>
	<tr><td>Display name:</td><td><input name="name" value="${c.viewing_user.name}"></td></tr>
	<tr><td>Home Location:</td><td><input name="location" value="${c.viewing_user.config["location"]}"></td></tr>
	<tr><td>Description:</td><td><textarea name="description">${c.viewing_user.config["description"]}</textarea></td></tr>
	<tr><td>Home page:</td><td><input name="home_page" value="${c.viewing_user.config["home_page"]}"></td></tr>
	</table>
</fieldset>
</%def>

<%def name="settings_email()">
<fieldset>
	<legend>${_("Email Address")}</legend>
	<table>
	<tr><td>Address:</td><td><input name="email" value="${c.viewing_user.email}"></td></tr>
	</table>
</fieldset>
</%def>

<%def name="settings_login()">
<fieldset>
	<legend>${_("Login Details")}</legend>
	<table>
	<tr><td>Current password:</td><td><input name="current_password" type="password"></td></tr>
	<tr><td>New password:</td><td><input name="new_password_1" type="password"></td></tr>
	<tr><td>Repeat new password:</td><td><input name="new_password_2" type="password"></td></tr>
	</table>
	<br><a href="">Link with Google, Facebook, etc</a>
</fieldset>
</%def>

<%def name="settings_aggregation()">
<fieldset>
	<legend>${_("Aggregation")}</legend>
	<table>
	<tr><td>Twitter username:</td><td><input name="twitter_username" value="${c.viewing_user.config["twitter_username"]}"></td></tr>
	<tr><td>Twitter auth key:</td><td><input name="twitter_auth_key" value="${c.viewing_user.config["twitter_auth_key"]}"></td></tr>
	<tr><td>Broadcast instant news:</td><td><input type="checkbox" name="broadcast_instant_news" value="${c.viewing_user.config["broadcast_instant_news"]}"></td></tr>
	<tr><td>Broadcast content posts:</td><td><input type="checkbox" name="broadcast_content_posts" value="${c.viewing_user.config["broadcast_content_posts"]}"></td></tr>
	</table>
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
#user_settings FIELDSET TD {
	padding: 2px;
	vertical-align: top;
}
#user_settings FIELDSET TABLE,
#user_settings FIELDSET INPUT,
#user_settings FIELDSET TEXTAREA {
	width: 100%;
}
#user_settings FIELDSET LEGEND {
	padding-left: 4px;
	padding-right: 4px;
}
</style>
<form action="${url.current(action='save_general', id=c.viewing_user.username)}" method="POST">
	<input type="hidden" name="_authentication_token" value="${h.authentication_token()}">
	<table id="user_settings"><tr>
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
			<td colspan="2"><input type="submit" value="Save" style="width: 100%"></td>
		</tr>
	</table>
</form>

</%doc>