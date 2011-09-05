<%namespace name="common" file="/admin/classes/common.mako" />

${common.errors(fieldset)}

<table class="outer">
	<tr>
		<td>
<table>
	<tr><th colspan="2">${_("Status")}</th></tr>
	${common.render_short_field(fieldset.type)|n}
	${common.render_short_field(fieldset.billing_status)|n}
	${common.render_short_field(fieldset.start_date)|n}
	${common.render_short_field(fieldset.frequency)|n}
	${common.render_short_field(fieldset.currency)|n}
	${common.render_short_field(fieldset.taxable)|n}
	${common.render_short_field(fieldset.tax_rate_code)|n}
</table>
		</td>
		<td>
<table>
	<tr><th colspan="2">${_("Users & _Groups")}</th></tr>
	${common.render_short_field(fieldset.members)|n}
</table>
<table>
    <tr><th colspan="2">${_("Billing Accounts")}</th></tr>
    ${common.render_short_field(fieldset.billing_accounts)|n}
    ${type(fieldset.billing_accounts)}
</table>
		</td>
	</tr>
</table>
