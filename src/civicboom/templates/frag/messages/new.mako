<% args, kwargs = c.web_params_to_kwargs %>

${h.form(h.args_to_tuple('messages', format='redirect'), data=dict(json_complete="[['modal_close']]"))}
	<table class="message_composer">
        
        % if kwargs.get("target"):
        <input type="hidden" name="target" value="${kwargs.get("target")}"/>
        % else:
		<tr>
			<td>${_("To")}&nbsp;</td>
            <td><input type="text"   name="target" value=""/></td>
		</tr>
        % endif
		<tr>
			<td>${_("Subject")}&nbsp;</td>
			<td><input type="text" name="subject" value="${kwargs.get("subject", "")}"></td>
		</tr>
		<tr>
			<td colspan="2"><textarea name="content"></textarea></td>
		</tr>
		<tr>
			<td colspan="2"><input type="submit" value="${_("Send")}"></td>
		</tr>
	</table>
${h.end_form()}
