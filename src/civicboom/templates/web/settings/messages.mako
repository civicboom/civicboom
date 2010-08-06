<%inherit file="/web/layout_2cols.mako"/>

<%def name="col_side()">
	<div class="avatar">
		<img class="avatar" src="${c.viewing_user.avatar_url}">
		<br>${c.viewing_user.name}
		<br>(${c.viewing_user.username})
	</div>

	<h2>Tools</h2>
	    <a href="${url(controller='user_profile', action='index')}">My Profile</a>
	<br><a href="${url(controller='settings', action='general')}">Edit Settings</a>
	<br><a href="${url(controller='settings', action='messages')}">Edit Notifications</a>
	<br><a href="${url(controller='messages', action='index')}">My Messages</a>
</%def>

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
