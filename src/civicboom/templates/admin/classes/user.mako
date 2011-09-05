<%namespace name="common" file="/admin/classes/common.mako" />

${common.errors(fieldset)}

<table class="outer">
	<tr>
		<td>
<table>
	<tr><th colspan="2">${_("Information")}</th></tr>
	${common.render_short_field(fieldset.id)|n}
	${common.render_short_field(fieldset.email)|n}
	${common.render_short_field(fieldset.email_unverified)|n}
	${common.render_short_field(fieldset.status.dropdown(options=["pending", "active", "removed"]))|n}
</table>
		</td>
		<td>
<table>
	<tr><th colspan="2">${_("Description")}</th></tr>
	${common.render_short_field(fieldset.name)|n}
	${common.render_short_field(fieldset.join_date)|n}
</table>

<table>
	<tr><th colspan="2">${_("Location")}</th></tr>
	<tr class="input_row"><td>Location Updated</td><td>${fieldset.location_updated.render_readonly()|n}</td></tr>
</table>
		</td>
	</tr>
</table>
