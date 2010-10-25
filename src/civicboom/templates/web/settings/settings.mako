<%inherit file="/web/common/html_base.mako"/>

<%namespace name="private_profile" file="/web/profile/index.mako"/>

##------------------------------------------------------------------------------
## Side Col
##------------------------------------------------------------------------------

<%def name="col_left()">${private_profile.col_left()}</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    ${h.form(h.url('setting', id='None'), method='put')}
    <%
        # Setup Settings groups
        setting_groups = {}
        for setting_meta in d['settings_meta'].values():
            if 'group' not in setting_meta:
               setting_meta['group'] = 'undefined'
            if setting_meta['group'] not in setting_groups:
                setting_groups[setting_meta['group']] = []
            setting_groups[setting_meta['group']].append(setting_meta['name'])
    %>
    
    % for group_name in setting_groups.keys():
        <fieldset><legend>${group_name.capitalize()}</legend>
            % for setting_name in setting_groups[group_name]:
                <p>
                    <%
                        setting_meta  = d['settings_meta'][setting_name]
                        setting_type  = None
                        if 'type' in setting_meta:
                            setting_type  = setting_meta['type']
                        setting_value = ''
                        if setting_name in d['settings']:
                            setting_value = d['settings'][setting_name]
                    %>

                    ${setting_meta['description']}:
                    
                    % if not setting_type:
                        <input name="${setting_name}" value="${setting_value}">
                    % elif setting_type == 'boolean':
                        <%
                            checked = None
                            if setting_value and setting_value!='': checked="checked='%s'" % setting_value
                        %>
                        <input name="${setting_name}" value="True" type='checkbox' ${checked}>
                    % elif setting_type == 'password':
                        <input name="${setting_name}" type="password" />
                    % endif

                    % if 'invalid' in d and setting_name in d['invalid']:
                        <span class="error-message">${d['invalid'][setting_name]}</span>
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
