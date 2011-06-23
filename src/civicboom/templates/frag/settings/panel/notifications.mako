<%inherit file="/frag/common/frag.mako"/>

<%!
    from civicboom.lib.constants import setting_icons
    rss_url   = False
    help_frag = 'settings_panel_messages'
%>

<%def name="title()">${_("Edit your notification settings")}</%def>

<%def name="body()">
    ${h.form(h.url('setting', id=c.result.get('username', 'me')), method='PUT')}
    <div style="display:none"><input type="hidden" name="panel" value="${c.result.get('panel')}" /></div>
    % if setting_icons.get('messages'):
        <img style="float:right;" src="/images/settings/${setting_icons.get('messages')}.png" />
    % endif
    <h1>${_('%(username)s notification settings') % dict(username= c.logged_in_persona.username.capitalize()) }</h1>
    <%
        panel = c.result.get('panel', 'messages')
        settings_meta = d['settings_meta']
        settings_meta = dict( [ (setting['name'], setting) for setting in settings_meta.values() if setting['group'].split('/')[0] == panel] )
        
        settings_meta = sorted(settings_meta.values(), key=lambda x: x['weight'])
        
        setting_groups = dict( [ (setting['group'].split('/')[1], [(s['name'], s) for s in settings_meta if s['group'].split('/')[1] == setting['group'].split('/')[1]]) for setting in settings_meta ] )
        
        setting_group_order = dict( [ (setting['group'].split('/')[1], setting['weight']) for setting in settings_meta] )
        
        setting_group_order = sorted(setting_group_order.keys(), key=setting_group_order.__getitem__)
        
        notification_types = settings_meta[0]['value']
        
        user = get_user
        
        def check(name, tech, default):
          if name in d['settings']:
            route = d['settings'][name]
          else:
            route = ''
          if tech in route:
            return "checked"
          else:
            return ""
        
        def select(name, tech, opt):
          if name in d['settings']:
            route = d['settings'][name]
          else:
            route = ''
          if route:
	          if (tech in route) and opt:
	            return 'selected=selected'
	          elif (not tech in route) and not opt:
	            return 'selected=selected'
	          else:
	            return ''
        
        notif_names = { 'n': 'Notification',
                         'e': 'Email'
                       }
    %>
    
    % for group_name in setting_groups.keys():
      <table class="zebra" style="width: 100%">
        <tr>
          <th>Type<span style="float: right;">via&nbsp;&nbsp;</span></th>
          % for notif_type in notification_types:
            <th>${notif_names.get(notif_type, '').replace('Notification', 'Website').capitalize()}</th>
          % endfor
        </tr>
      % for setting_name in setting_groups[group_name]:
        <tr>
          <td>${d['settings_meta'][setting_name[0]]['description']}</td>
          % for notif_type in notification_types:
            <td>
              <select class="yesno" name="${setting_name[0]}-${notif_type[0]}">
                <option class="yes" ${select(setting_name[0],notif_type[0],True )} value="${notif_type[0]}">Yes</option>
                <option class="no"  ${select(setting_name[0],notif_type[0],False)} value="">No</option>
              </select>
            </td>
          % endfor
        </tr>
      % endfor
      </table>
    % endfor
    <input class="button" type="submit" name="submit" value="${_('Save settings')}" style="margin: 16px;"/>
${h.end_form()}
</%def>
