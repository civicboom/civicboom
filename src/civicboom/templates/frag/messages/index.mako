<%inherit file="/frag/common/frag_lists.mako"/>

<%def name="body()">
    <%
        args, kwargs = c.web_params_to_kwargs
        list = _('Message ')
        if 'list' in kwargs:
            list += kwargs.get('list')
    %>
    ${parent.message_list(d['list'], list, max=None, list=kwargs.get('list'))}
</%def>


<%doc>
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
					${h.form(url('message', id=message['id'], format='redirect'), method="DELETE")}
						<input type="submit" value="Delete">
					${h.end_form()}
				</td>
			</tr>
% endfor
		</tbody>
    </table>
</%def>
</%doc>