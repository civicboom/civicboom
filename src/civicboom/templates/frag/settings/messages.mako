<%inherit file="/frag/common/frag.mako"/>

<%!
    rss_url   = False
    help_frag = 'message_routes'
%>

<%def name="title()">${_("Edit your notification settings")}</%def>

<%def name="body()">
${h.form(h.url('setting', id='messages'), method='put')}
<%
from civicboom.lib.communication.messages import generators

ignore_generators = ['msg_test',
                     'assignment_response_mobile',
                     'syndicate_accept',
                     'syndicate_decline',
                     'syndicate_expire',
                    ]
                     
                     

def check(name, tech, default):
	if "route_"+name in c.logged_in_persona.config:
		route = c.logged_in_persona.config["route_"+name]
	else:
		route = default

	if tech in route:
		return "checked"
	else:
		return ""
%>
	<table class="zebra" style="width: 100%">
		<tr>
			<th>Message</th>
			<th>Notification</th>
			<th>Email</th>
			<!--<th>Comufy</th>-->
		</tr>
	% for gen in generators:
	   % if not gen[0] in ignore_generators:
		<tr>
			<td>${str(gen[2]).capitalize()}</td>
			<td><input name="${gen[0]}_n" type="checkbox" value="n" ${check(gen[0], 'n', gen[1])}></td>
			<td><input name="${gen[0]}_e" type="checkbox" value="e" ${check(gen[0], 'e', gen[1])}></td>
			<!--<td><input name="${gen[0]}_c" type="checkbox" value="c" ${check(gen[0], 'c', gen[1])}></td>-->
		</tr>
	   % endif
	% endfor
		<tr><td>
         <a class="button" href    = "${h.url('settings')}" title   = "${_('Back to Settings')}">
          <span>${_('Back to Settings')}</span>
         </a>
		</td><td colspan="2"><input class="button" type="submit" value="Save" style="width: 100%"></td></tr>
	</table>
${h.end_form()}
</%def>
