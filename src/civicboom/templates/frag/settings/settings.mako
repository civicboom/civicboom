<%inherit file="/frag/common/frag.mako"/>

<%!
    rss_url   = False
    help_frag = 'settings'
%>

<%namespace name="loc" file="/html/web/common/location.mako"/>

<%def name="body()">
    <a href="${url(controller='settings', action='messages')}">${_("Edit Notifications")}</a>
    <a href="${url(controller='account' , action='link_janrain')}">${_("Link Addtional Accounts")}</a>
    <br/>

    ${h.form(h.url('setting', id='None'), method='PUT', multipart=True)}
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

	<style>
	</style>
    % for group_name in setting_groups.keys():
        <div style="margin: 16px;">
			<div style="font-weight: bold;">${group_name.capitalize()}</div>
			<table class="form" style="width: 100%;">
            % for setting_name in setting_groups[group_name]:
                <tr>
                    <%
                        setting_meta  = d['settings_meta'][setting_name]
                        setting_type  = None
                        if 'type' in setting_meta:
                            setting_type  = setting_meta['type']
                        setting_value = ''
                        if setting_name in d['settings']:
                            setting_value = d['settings'][setting_name]
                    %>

                    <td width="130" class='descr'>${setting_meta['description']}</td>
                    
					<td>
                    % if not setting_type:
                        <input name="${setting_name}" type="text" value="${setting_value}">
                    % elif setting_type == 'boolean':
                        <%
                            checked = None
                            if setting_value and setting_value!='': checked="checked='%s'" % setting_value
                        %>
                        <input name="${setting_name}" value="True" type='checkbox' ${checked}>
                    % elif setting_type == 'textarea':
                        <textarea name="${setting_name}" rows="4">${setting_value}</textarea>
                    % elif setting_type == 'password':
                        <input name="${setting_name}" type="password" />
                    % elif setting_type == 'file':
                        <input name="${setting_name}" type="file" />
                    % elif setting_type == 'location':
						</tr><tr><td colspan="2">
						${loc.location_picker(field_name=setting_name, width='100%', height='300px', always_show_map=True)}
                    % endif
					</td>

                    % if 'invalid' in d and setting_name in d['invalid']:
                        <td><span class="error-message">${d['invalid'][setting_name]}</span></td>
                    % endif
                </tr>
            % endfor
			</table>
        </div>
    % endfor
    <input class="button" type="submit" name="submit" value="${_('Save settings')}" style="margin: 16px;"/>
    ${h.end_form()}
</%def>
