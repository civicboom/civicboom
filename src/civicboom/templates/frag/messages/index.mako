<table>
	<tr>
		<th>From</th>
		<th>Subject</th>
		<th>Date</th>
		<th>Action</th>
	</tr>
% for msg in d.messages:
	<tr>
		<td>${str(msg["source"])}</td>
		<td><a href="${url('message', id=msg['id'])}">${msg['subject']}</a></td>
		<td>${msg["timestamp"][0:16]}</td>
		<td>
			${h.form(url('message', id=msg['id']), method="DELETE")}
				<input type="submit" value="Delete">
			${h.end_form()}
		</td>
	</tr>
% endfor
</table>
