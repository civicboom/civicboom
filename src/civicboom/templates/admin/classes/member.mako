<%namespace name="common" file="/admin/classes/common.mako" />

${common.errors(fieldset)}

<table class="outer">
	<tr>
		<td>
<table>
	<tr><th colspan="2">${_("Information")}</th></tr>
	${common.render_short_field(fieldset.id)|n}
</table>
		</td>
		<td>
<table>
	<tr><th colspan="2">${_("Description")}</th></tr>
	${common.render_short_field(fieldset.name)|n}
	${common.render_short_field(fieldset.join_date)|n}
</table>
<table>
    <tr><th colspan="2">${_("Payment Account")}</th></tr>
    ${common.render_short_field(fieldset.payment_account)|n}
</table>
		</td>
	</tr>
</table>
