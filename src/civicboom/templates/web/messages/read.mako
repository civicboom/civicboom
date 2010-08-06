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
	<tr>
		<td>${str(c.msg.source)}</td>
		<td>${c.msg.subject}</td>
		<td>${c.msg.timestamp}</td>
	</tr>
	<tr>
		<td colspan="3">${c.msg.content}</td>
	</tr>
</table>
</%def>
