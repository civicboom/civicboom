<%inherit file="/frag/common/frag.mako"/>


<%!
    from sets import Set
    rss_url   = False
    help_frag = 'settings'
%>

<%namespace name="loc" file="/html/web/common/location.mako"/>

<%def name="title()">${_("Edit your account settings")}</%def>

<%def name="body()">
## GregM: have moved as an addition to general group
    ${h.form(h.url('setting', id=c.result.get('username', 'me')), method='PUT', multipart=True)}
    <div style="display:none"><input type="hidden" name="panel" value="${c.result.get('panel')}" /></div>
    <%
        panel = c.result.get('panel', d.get('panel'))
        settings_meta = d['settings_meta']
        settings_meta = dict( [ (setting['name'], setting) for setting in settings_meta.values() if setting['group'].split('/')[0] == panel] )
        
        settings_meta = sorted(settings_meta.values(), key=lambda x: x['weight'])
        
        setting_groups = dict( [ (setting['group'].split('/')[1], [(s['name'], s) for s in settings_meta if s['group'].split('/')[1] == setting['group'].split('/')[1]]) for setting in settings_meta ] )
        
        setting_group_order = dict( [ (setting['group'].split('/')[1], setting['weight']) for setting in settings_meta] )
        
        setting_group_order = sorted(setting_group_order.keys(), key=setting_group_order.__getitem__)
        
        settings_hints = d.get('settings_hints') or {}
    %>

    ##% for group_name in setting_groups.keys():
    % for group_name in setting_group_order:
        <div style="margin: 16px;">
      <div style="font-weight: bold;">${group_name.capitalize()}</div>
      <div class="settinginfo">
        <p><b>OPTIONAL</b></p>
        <p>Civicboom will be adding new features in the coming months. Part of this is the ability to geo-locate content in your area, get alerted to local requests and participate fully in the crowdsourcing experience.</p>
        <p>You can add your location now, but this will not be used until the features are rolled out.</p>
        <p><b>Your location will not be shared with other users. Your geo-location will be used in order for relevant requests to be pushed to you. <br/><u>This is an opt-in function.</u></b></p>
      </div>
      <table class="form" style="width: 100%;">
            % for setting_name in setting_groups[group_name]:
                <tr>
                    <%
                        setting_meta  = d['settings_meta'][setting_name[0]]
                        setting_type  = None
                        if 'type' in setting_meta:
                            setting_type  = setting_meta['type']
                        setting_value = ''
                        setting_values = setting_meta.get('value').split(',')
                        if setting_name[0] in d['settings']:
                            setting_value = d['settings'][setting_name[0]]
                    %>

                    <td width="130" class='descr'>${setting_meta['description']}</td>
                    
          <td>
                    % if settings_hints.get(setting_name[0]):
                        <div class="settinghint">${settings_hints.get(setting_name[0])}</div>
                    % endif
                    % if not setting_type or setting_type == 'string' or setting_type == 'url' or setting_type == 'email':
                        <input name="${setting_name[0]}" type="text" value="${setting_value}">
                    % elif setting_type == 'boolean':
                        <%
                            checked = None
                            if setting_value and setting_value!='': checked="checked='%s'" % setting_value
                        %>
                        <input name="${setting_name[0]}" value="True" type='checkbox' ${checked}>
                    % elif setting_type == 'longstring':
                        <textarea name="${setting_name[0]}" rows="4">${setting_value}</textarea>
                    % elif 'password' in setting_type:
                        <input name="${setting_name[0]}" type="password" />
                    % elif setting_type == 'file':
                        <input name="${setting_name[0]}" type="file" />
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
                        ${loc.location_picker(field_name=setting_name[0], width='100%', height='300px', always_show_map=True, label_class="norm", lon=lon, lat=lat)}
                        </div>
                    % endif
          </td>

                    % if 'invalid' in d and setting_name[0] in d['invalid']:
                        <td><span class="error-message">${d['invalid'][setting_name[0]]}</span></td>
                    % endif
                </tr>
            % endfor
##        GregM: Add the janrain & notifications links to the general group.
            % if group_name == 'contact':
              <tr><td>&nbsp;</td><td colspan="2"><br />
                <a href="${url(controller='account' , action='link_janrain')}">${_("Link Additional Accounts (Facebook, LinkedIn, Google and more)")}</a>
              </td></tr>
            % endif
      </table>
        </div>
    % endfor
    <input class="button" type="submit" name="submit" value="${_('Save settings')}" style="margin: 16px;"/>
    ${h.end_form()}
</%def>
