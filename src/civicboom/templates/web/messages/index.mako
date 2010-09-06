<%inherit file="/web/layout_2cols.mako"/>

<%def name="col_side()">
	<div class="avatar">
		<img class="avatar" src="${c.viewing_user.avatar_url}">
		<br>${c.viewing_user.name}
		<br>(${c.viewing_user.username})
	</div>

	<h2>Tools</h2>
	    <a href="${url(controller='profile', action='index')}">My Profile</a>
	<br><a href="${url(controller='settings', action='general')}">Edit Settings</a>
	<br><a href="${url(controller='settings', action='messages')}">Edit Notifications</a>
	<br><a href="${url('messages')}">My Messages</a>
</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
<table>
	<tr>
		<th>From</th>
		<th>Subject</th>
		<th>Date</th>
		<th>Action</th>
	</tr>
% for msg in c.viewing_user.messages_to:
	<tr>
		<td>${str(msg.source)}</td>
		<td><a href="${url('message', id=msg.id)}">${msg.subject}</a></td>
		<td>${msg.timestamp}</td>
		<td>
			<form action="${url('message', id=msg.id)}" method="POST">
				<input type="hidden" name="_method" value="DELETE" />
				<input type="hidden" name="_authentication_token" value="${h.authentication_token()}">
				<input type="hidden" name="type" value="message">
				<input type="submit" value="Delete">
			</form>
		</td>
	</tr>
% endfor
</table>
</%def>
