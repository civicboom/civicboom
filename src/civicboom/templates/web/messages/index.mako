<%inherit file="/web/html_base.mako"/>

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
		<td><a href="${url.current(action='read', id=msg.id)}">${msg.subject}</a></td>
		<td>${msg.timestamp}</td>
		<td>
			<form action="${url.current(action='delete')}" method="POST">
				<input type="hidden" name="_authentication_token" value="${h.authentication_token()}">
				<input type="hidden" name="msg_id" value="${msg.id}">
				<input type="submit" value="Delete">
			</form>
		</td>
	</tr>
% endfor
</table>
</%def>
