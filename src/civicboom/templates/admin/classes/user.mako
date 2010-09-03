<%namespace name="common" file="/admin/classes/common.mako" />

${common.errors(fieldset)}

<table class="outer">
	<tr>
		<td>
<table>
	<tr><th colspan="2">${_("Information")}</th></tr>
	${common.render_short_field(fieldset.username)|n}
	${common.render_short_field(fieldset.email)|n}
	${common.render_short_field(fieldset.status.dropdown(options=["pending", "active", "removed"]))|n}
	${common.render_short_field(fieldset.location)|n}
	<tr class="input_row"><td>Updated</td><td>${fieldset.location_updated.render_readonly()|n}</td></tr>
</table>
		</td>
		<td>
<table>
	<tr><th colspan="2">${_("Description")}</th></tr>
	${common.render_short_field(fieldset.name)|n}
	${common.render_short_field(fieldset.join_date)|n}
</table>
		</td>
	</tr>
</table>
