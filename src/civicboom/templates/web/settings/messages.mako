<%inherit file="/web/common/html_base.mako"/>
<%namespace name="prof" file="/web/common/profile.mako"/>
<%def name="col_left()">${prof.sidebar()}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
<form action="${url.current(action='save_messages', id=c.viewing_user.username)}" method="POST">
	<input type="hidden" name="_authentication_token" value="${h.authentication_token()}">
<%
from civicboom.lib.communication.messages import generators

def check(name, tech, default):
	if "route_"+name in c.viewing_user.config:
		route = c.viewing_user.config["route_"+name]
	else:
		route = default

	if tech in route:
		return "checked"
	else:
		return ""
%>
	<table>
		<tr>
			<th>Message</th>
			<th>Notification</th>
			<th>Email</th>
			<th>Comufy</th>
		</tr>
	% for gen in generators:
		<tr>
			<td>${str(gen[2])}</td>
			<td><input name="${gen[0]}_n" type="checkbox" value="n" ${check(gen[0], 'n', gen[1])}></td>
			<td><input name="${gen[0]}_e" type="checkbox" value="e" ${check(gen[0], 'e', gen[1])}></td>
			<td><input name="${gen[0]}_c" type="checkbox" value="c" ${check(gen[0], 'c', gen[1])}></td>
		</tr>
	% endfor
		<tr><td colspan="4"><input type="submit" value="Save" style="width: 100%"></td></tr>
	</table>
</form>
</%def>
