<%inherit file="/frag/common/frag.mako"/>

<%!
    from civicboom.lib.constants import setting_icons
    from sets import Set

    rss_url   = False
    help_frag = None
%>


<%def name="title()">${_("Settings Menu")}</%def>

<%def name="body()">
<%
    settings_meta = d['settings_meta']
    panels = d['panels']
    if c.result.get('user_type') == 'user':
    	panels['janrain'] = {'weight':1000, 'title':'Link additional login accounts', 'panel':'link_janrain'}
    panelorder = sorted(panels.values(), key=lambda x: int(x['weight']))
%>
    <%def name="link(title, panel)">
        <li style="vertical-align: middle; padding-top:1em;">
            <a href="${h.url('setting_action', id=c.id or 'me', action=panel)}">
                <div style="vertical-align: middle;display: inline-block;width: 8em;">${title}:</div>
                <div style="vertical-align: middle;display: inline-block;width: 6em;">
                    % if setting_icons.get(panel):
                        <img src="/images/settings/${setting_icons.get(panel)}.png" />
                    % endif
                </div>
                <img src="/images/settings/arrow.png" />
            </a>
        </li>
    </%def>
    <div style="padding: 3px 3px 3px 3px;">
        <h1>Username settings</h1>
      <ul>
      % for panel in panelorder:
        ${link(panel['title'].capitalize(), panel['panel'])}
      % endfor
      </ul>
    </div>
</%def>
