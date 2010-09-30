${show_messages(d['messages'])}

<%def name="show_messages(messages)">
    <table>
        <tr>
            <th>From</th>
            <th>Subject</th>
            <th>Date</th>
            <th>Action</th>
        </tr>
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
    </table>
</%def>