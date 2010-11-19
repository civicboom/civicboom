${show_messages(d['list'])}

<%def name="show_messages(messages)">
    <table class='message_list zebra'>
		<thead>
			<tr>
				<th class='from'>${_("From")}</th>
				<th class='subject'>${_("Subject")}</th>
				<th class='date'>${_("Date")}</th>
				<th class='action'>${_("Action")}</th>
			</tr>
		</thead>
		<tbody>
% for message in messages:
			<tr>
				<td>${str(message["source"])}</td>
				<td><a href="${url('message', id=message['id'])}">${message['subject']}</a></td>
				<td>${message["timestamp"][0:16]}</td>
				<td>
					${h.form(url('message', id=message['id']), method="DELETE")}
						<input type="submit" value="Delete">
					${h.end_form()}
				</td>
			</tr>
% endfor
		</tbody>
    </table>
</%def>
