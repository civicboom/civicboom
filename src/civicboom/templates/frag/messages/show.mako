<table>
	<tr>
		<th>From</th>
		<th>Subject</th>
		<th>Date</th>
	</tr>
	<tr>
		<td>${str(c.result['data']["source"])}</td>
		<td>${c.result['data']["subject"]}</td>
		<td>${c.result['data']["timestamp"][0:16]}</td>
	</tr>
	<tr>
		<td colspan="3">${c.result['data']["content"]}</td>
	</tr>
</table>
