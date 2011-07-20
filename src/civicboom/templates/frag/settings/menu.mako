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
        <li>
            <div class="name">
                <a class="" href="${h.url('setting_action', id=c.id or 'me', action=panel)}">
                    ${title}:
                </a>
            </div>
            <div class="image">
                % if setting_icons.get(panel):
                    <img src="/images/settings/${setting_icons.get(panel)}.png" />
                % endif
            </div>
            <a href="${h.url('setting_action', id=c.id or 'me', action=panel)}">
                <img src="/images/settings/arrow.png" />
            </a>
        </li>
    </%def>
    <div>
        <h1>${_('%(username)s settings') % dict(username= d['username'].capitalize()) }</h1>
        <ul class="setting_menu">
        % for panel in panelorder:
            ${link(panel['title'].capitalize(), panel['panel'])}
        % endfor
        </ul>
    </div>
</%def>
