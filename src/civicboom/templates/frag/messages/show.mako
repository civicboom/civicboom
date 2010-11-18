${show_message(c.result['data']['message'])}

<%def name="show_message(message)">
<table>
	<tr>
		<th>${_("From")}</th>
		<th>${_("Subject")}</th>
		<th>${_("Date")}</th>
	</tr>
	<tr>
		<td>${str(message["source"])}</td>
		<td>${message["subject"]}</td>
		<td>${message["timestamp"][0:16]}</td>
	</tr>
	<tr>
		<td colspan="3">${message["content"]}</td>
	</tr>
</table>
</%def>
