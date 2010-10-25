${h.form(url('messages', format='redirect'))}
	<table class="message_composer">
		<tr>
			<td>To&nbsp;</td>
			<td><input type="text" name="targetx" value="${request.GET.get("to", "")}"></td>
		</tr>
		<tr>
			<td>Subject&nbsp;</td>
			<td><input type="text" name="subject" value="${request.GET.get("subject", "")}"></td>
		</tr>
		<tr>
			<td colspan="2"><textarea name="content"></textarea></td>
		</tr>
		<tr>
			<td colspan="2"><input type="submit" value="Send"></td>
		</tr>
	</table>
${h.end_form()}
