<html>
	<table border="1">
		<tr>
			<td>Date / Time</td>
			<td>Module / URL</td>
			<td>Username / IP</td>
			<td>Message</td>
		</tr>
	% for event in events:
		<tr style='color: ${h.priority_to_color(event.priority)}'>
			<td>${str(event.date_sent)[0:19].replace(" ", "<br/>")|n}</td>
			<td>${event.module}
			<br/>${event.url}</td>
			<td>${event.username}
			<br/>${event.address}</td>
			<td>${event.message}</td>
		</tr>
	% endfor
	</table>
</html>
