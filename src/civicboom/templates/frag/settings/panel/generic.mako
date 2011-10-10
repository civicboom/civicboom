<%inherit file="/frag/common/frag.mako"/>


<%!
    from sets import Set
    from civicboom.lib.constants import setting_icons
    rss_url             = False
    help_frag           = None
    field_name_sizes    = {'boolean': '_long' , }
    field_sizes         = {'boolean': '_short', 'location': '_full' , }
%>
<%namespace name="loc" file="/html/web/common/location.mako"/>

<%def name="title()">${_("Edit your account settings")}</%def>

<%def name="body()">
## GregM: have moved as an addition to general group
    ${h.form(h.url('setting', id=d.get('username', 'me')), method='PUT', multipart=True)}
    <div style="display:none"><input type="hidden" name="panel" value="${c.result.get('panel')}" /></div>
    <%
        panel = c.result.get('panel', d.get('panel'))
        panel_title = d.get('panels', {}).get(panel, {}).get('title')
        panel_name  = d.get('panels', {}).get(panel, {}).get('panel')
        settings_meta = d['settings_meta']
        settings_meta = dict( [ (setting['name'], setting) for setting in settings_meta.values() if setting['group'].split('/')[0] == panel] )
        
        settings_meta = sorted(settings_meta.values(), key=lambda x: x['weight'])
        
        setting_groups = dict( [ (setting['group'].split('/')[1], [(s['name'], s) for s in settings_meta if s['group'].split('/')[1] == setting['group'].split('/')[1]]) for setting in settings_meta ] )
        
        setting_group_order = dict( [ (setting['group'].split('/')[1], setting['weight']) for setting in settings_meta] )
        
        setting_group_order = sorted(setting_group_order.keys(), key=setting_group_order.__getitem__)
        
        settings_hints = d.get('settings_hints', {})
    %>
    % if setting_icons.get(panel_name):
        <img style="float:right;" src="/images/settings/${setting_icons.get(panel_name)}.png" />
    % endif
    <h1>${_('%(username)s %(panel_title)s settings') % dict(username= d['username'].capitalize(), panel_title=panel_title.lower()) }</h1>
    % for group_name in setting_group_order:
        <div style="margin: 0; clear: both;">
        % if group_name.lower() != panel.lower():
     		<div class="setting_group_name setting_pad">${group_name.replace('_',' ').capitalize()}</div>
     	% endif
        ## Insert header for group if it is defined below:
        % if hasattr(self, group_name+"_header") and callable(getattr(self, group_name+"_header")):
            ${getattr(self, group_name+"_header")()}
        % endif
        % for setting_name in setting_groups[group_name]:
            <%
                setting_meta  = d['settings_meta'][setting_name[0]]
                setting_type  = None
                if 'type' in setting_meta:
                    setting_type  = setting_meta['type']
                if setting_type == 'string_location':
                    continue
                setting_value = ''
                setting_values = setting_meta.get('value')
                if setting_name[0] in d['settings']:
                    setting_value = d['settings'][setting_name[0]]
                setting_hint = settings_hints.get(setting_name[0])
            %>
		    <%def name="placeholder()">
		    	% if setting_meta.get('info'):
		    		placeholder="${setting_meta['info']}"
		    	% endif
		    </%def>
		    <%def name="readonly()">
		    	% if '_readonly' in setting_type:
		    		disabled="disabled"
		    	% endif
		    </%def>
            <div class="setting_block">
                <div class="setting_name${ field_name_sizes.get(setting_type, '') } setting_pad">${setting_meta['description'] if setting_meta['description'].lower() != group_name.lower() else ''}</div>
                % if field_sizes.get(setting_type, '') == "_full":
                    <br />
                % endif
                <div class="setting_field${ field_sizes.get(setting_type, '') } setting_pad">
                	% if setting_type == 'boolean':
                        <%
                            selected = setting_value and setting_value!=''
                        %>
                		<select class="yesno" name="${setting_name[0]}" ${readonly()} id="${setting_name[0]}">
                			<option class="yes" value="True" ${'selected="selected"' if selected else ''}>Yes</option>
                			<option class="no" value="" ${'selected="selected"' if not selected else ''}>No</option>
                		</select>
                    % elif setting_type == 'longstring':
                        <textarea name="${setting_name[0]}" ${readonly()} ${placeholder()} rows="4">${setting_value}</textarea>
                    % elif 'password' in setting_type:
                        <input name="${setting_name[0]}" ${readonly()} type="password" />
                    % elif setting_type == 'file':
                        <input name="${setting_name[0]}" ${readonly()} type="file" />
                    % elif setting_type == 'enum':
                        % for value in setting_values:
                            <input type="radio" name="${setting_name}" ${readonly()} value="${value}" id="${setting_name}_${value}" />
                            <label for="${setting_name}_${value}">${value.capitalize()}</label>
                        % endfor
                    % elif setting_type == 'location':
                        <%
                        try:
                          (lon, lat) = [float(f) for f in setting_value.split(" ")]
                        except:
                          (lon, lat) = (None, None)
                        %>
                        ${loc.location_picker(field_name=setting_name[0], width='100%', height='300px', always_show_map=True, label_class="norm", lon=lon, lat=lat)}
                    % elif setting_type == 'display':
                    	<input name="${setting_name[0]}" type="text" readonly="readonly" ${placeholder()} value="${setting_value}">
                        <p class="setting_description">${_('This setting is only for reference and cannot be changed')}</p>
                    % else:
                    	<input name="${setting_name[0]}" type="text" ${readonly()} ${placeholder()} value="${setting_value}">
                    % endif
            	</div>
                % if 'invalid' in d and setting_name[0] in d['invalid']:
                    <div class="setting_error">
                    	<span class="error-message">${d['invalid'][setting_name[0]]}</span>
                    </div>
                % endif
                % if setting_hint:
                    <div class="setting_hint">
                        ${ setting_hint | n }
                    </div>
                % endif
            </div>
		% endfor
		## Insert footer for group if it is defined below:
        % if hasattr(self, group_name+"_footer") and callable(getattr(self, group_name+"_footer")):
            ${getattr(self, group_name+"_footer")()}
        % endif
        </div>
    % endfor
    <input class="button" type="submit" name="submit" value="${_('Save settings')}" style="margin: 16px;"/>
    ${h.end_form()}
</%def>


<%def name="password_footer()">
    <div class="setting_group_name setting_pad" style="padding-top: 12px">${_('Accessing your account via the mobile app:')}</div>
    <div class="setting_pad" style="font-style: italic;">
        ${_('You can set requests, post responses and stories directly from you Android mobile.')} <a href="${h.url(controller='misc', action='about', id='mobile')}">${_('Click here to get it.')}</a>
    </div>
    <div class="setting_pad">
        ${_('If you have signed up to Civicboom via Facebook, Twitter, LinkedIn etc, you will need to set up a password (as above) and use these to log into the mobile app. Your username remains the same.')}
    </div>
</%def>

<%def name="location_header()">
    ##<div class="setting_group_name setting_pad" style="padding-top: 12px">${_('Optional')}</div>
    <div class="setting_pad">
        ${_('_site_name will be adding new features in the coming months. Part of this development is the ability to geo-locate content in your area and get alerted to local story requests based on where you are.')}
    </div>
    <div class="setting_pad">
        ${_('You can add your location now but this will not be used until the features are rolled out.')}
    </div>
    <div class="setting_pad">
        ${_('Your location will not be shared with other users. Your geo-location will be used in order for relevant requests to be pushed to you.')}<br />
    </div>
    <div class="setting_pad">
        <span style="font-size: 130%; font-weight: bold">${_('This is an opt-in function.')}</span>
    </div>
</%def>
