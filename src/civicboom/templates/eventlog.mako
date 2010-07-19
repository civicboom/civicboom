<html>
    <head>
        <style>
.log0  {color: #0F0;} /* undefined, green     */
.log10 {color: #999;} /* debug, grey          */
.log20 {color: #000;} /* info, black          */
.log30 {color: #800;} /* warning, dark red    */
.log40 {color: #C00;} /* error, mid red       */
.log50 {background: #F00;} /* critical, bright red background */
        </style>
    </head>
	<table border="1">
		<tr>
			<td>Date / Time</td>
			<td>Module</td>
            <td>URL</td>
			<td>Username / IP</td>
			<td>Message</td>
		</tr>
	% for event in events:
		<tr class='log${event.priority}'>
			<td>${str(event.date_sent)[0:19].replace(" ", " ")|n}</td>
			<td><a href="?module=${event.module}" title="${event.module}">${h.shorten_module(event.module)}</a></td>
			<td><a href="${event.url}">${h.shorten_url(event.url)}</a></td>
			<td>${h.username_plus_ip(event.username, event.address)|n}</td>
			<td>${event.message}</td>
		</tr>
	% endfor
	</table>
</html>
