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
		<td>${str(c.data["source"])}</td>
		<td>${c.data["subject"]}</td>
		<td>${c.data["timestamp"][0:16]}</td>
	</tr>
	<tr>
		<td colspan="3">${c.data["content"]}</td>
	</tr>
</table>
</%def>
