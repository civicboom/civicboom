<%inherit file="/frag/common/frag.mako"/>


<%!
    from sets import Set
    rss_url   = False
    help_frag = None #'settings'
%>

<%namespace name="loc" file="/html/web/common/location.mako"/>

<%def name="title()">${_("Edit your account settings")}</%def>

<%def name="body()">
## GregM: have moved as an addition to general group
    ${h.form(h.url('setting', id='None'), method='put', multipart=True)}
    <%
        # Setup Settings groups
        setting_groups = {}
        for setting_meta in d['settings_meta'].values():
            if 'group' not in setting_meta:
               setting_meta['group'] = 'undefined'
            if setting_meta['group'] not in setting_groups:
                setting_groups[setting_meta['group']] = []
            setting_groups[setting_meta['group']].append(setting_meta['name'])
        
        # GMiell: this list contains default order of settings groups
        setting_group_order = ['general', 'contact', 'password', 'location', 'avatar']
        # create a set from the available setting groups
        setting_groups_set  = set(setting_groups.keys())
        # create a set of default order settings that need to be removed from the default order
        setting_groups_remove = set(setting_group_order) - setting_groups_set
        # remove them
        for m in setting_groups_remove:
            if m in setting_group_order:
                setting_group_order.remove (m)
        # extend our default order 
        setting_group_order.extend(setting_groups_set - set(setting_group_order))
              
        #for g in setting_group_order:
        #    log.debug(g)
        #settings_groups_order = (setting_group_order & setting_groups_set) | (setting_group_order - setting_groups_set)
    %>

	<style>
	</style>

    ##% for group_name in setting_groups.keys():
    % for group_name in setting_group_order:
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
                        setting_values = setting_meta.get('value').split(',')
                        setting_value = d['settings'][setting_name] if setting_name in d['settings'] else ''
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
                    % elif setting_type == 'enum':
                        % for value in setting_values:
                            <input type="radio" name="${setting_name}" value="${value}" id="${setting_name}_${value}" />
                            <label for="${setting_name}_${value}">${value.capitalize()}</label>
                        % endfor
                    % elif setting_type == 'location':
            ##</tr><tr><td></td>
						<td colspan="1"><div style="text-align: left;">
						<%
						try:
							(lon, lat) = [float(f) for f in setting_value.split(" ")]
						except:
							(lon, lat) = (None, None)
						%>
						${loc.location_picker(field_name=setting_name, width='100%', height='300px', always_show_map=True, label_class="norm", lon=lon, lat=lat)}
						</div>
                    % endif
					</td>

                    % if 'invalid' in d and setting_name in d['invalid']:
                        <td><span class="error-message">${d['invalid'][setting_name]}</span></td>
                    % endif
                </tr>
            % endfor
##        GregM: Add the janrain & notifications links to the general group.
##            % if group_name == 'contact':
##              <tr><td>&nbsp;</td><td colspan="2"><br />
##                <a href="${url(controller='account' , action='link_janrain')}">${_("Link Additional Accounts (Facebook, LinkedIn, Google and more)")}</a>
##              </td></tr>
##              <tr><td>&nbsp;</td><td colspan="2"><br />
##                <a href="${url(controller='settings', action='messages')}">${_("Edit Notification Preferences")}</a>
##              </td></tr>
##            % endif
			</table>
        </div>
    % endfor
    <input class="button" type="submit" name="submit" value="${_('Save settings')}" style="margin: 16px;"/>
    ${h.end_form()}
</%def>
