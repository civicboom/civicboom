<%inherit file="/frag/common/frag.mako"/>


<%!
    rss_url   = False
    help_frag = None
%>


<%def name="title()">${_("Settings Menu")}</%def>

<%def name="body()">
<%
    settings_meta = d['settings_meta']
    panels = d['panels']
    if c.result.get('user_type') == 'user':
    	panels['janrain'] = {'weight':100, 'title':'Link additional login accounts', 'panel':'link_janrain'}
    panelorder = sorted(panels, key=panels.__getitem__)
%>
    <%def name="link(title, panel)">
        <li><a href="${h.url('setting_action', id=c.id or 'me', action=panel)}">${title}</a></li>
    </%def>
    <div style="padding: 3px 3px 3px 3px;">
      <ul>
      % for panel in panelorder:
      	<%
      		paneldata = panels[panel]
      	%>
        ${link(paneldata['title'].capitalize(), paneldata['panel'])}
      % endfor
      </ul>
    </div>
</%def>
