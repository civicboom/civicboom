<%inherit file="/frag/common/frag.mako"/>


<%!
    from sets import Set
    rss_url   = False
    help_frag = None
%>


<%def name="title()">${_("Settings Menu")}</%def>

<%def name="body()">
<%
    settings_meta = d['settings_meta']
    #panels = dict( [ ( setting['group'].split('/')[0], setting['weight'] ) for setting in settings_meta.values() if setting.get('who', user_type) == user_type] )
    panels = d['panels']
    panels = sorted(panels, key=panels.__getitem__)
    print panels
%>
    <%def name="link(title, panel)">
        <li><a href="/settings/${c.id or 'me'}/${panel}">${title}</a></li>
    </%def>
    <div style="padding: 3px 3px 3px 3px;">
      <ul>
      %for panel in panels:
        ${link(panel.capitalize(), panel)}
      %endfor
      </ul>
    </div>
</%def>
