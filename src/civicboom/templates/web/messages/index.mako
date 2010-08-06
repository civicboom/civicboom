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
	</tr>
% for msg in c.viewing_user.messages_to:
	<tr>
		<td>${str(msg.source)}</td>
		<td><a href="${url.current(action='read', id=msg.id)}">${msg.subject}</a></td>
		<td>${msg.timestamp}</td>
	</tr>
% endfor
</table>
</%def>
