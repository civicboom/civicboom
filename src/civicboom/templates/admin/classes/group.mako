<%namespace name="common" file="/admin/classes/common.mako" />

${common.errors(fieldset)}

<table class="outer">
	<tr>
		<td>
<table>
	<tr><th colspan="2">${_("Information")}</th></tr>
	${common.render_short_field(fieldset.id)|n}
	${common.render_short_field(fieldset.status.dropdown(options=["pending", "active", "removed"]))|n}
</table>

<table>
	<tr><th colspan="2">${_("Mode")}</th></tr>
	${common.render_short_field(fieldset.join_mode)|n}
	${common.render_short_field(fieldset.member_visibility)|n}
	${common.render_short_field(fieldset.default_content_visibility)|n}
	${common.render_short_field(fieldset.default_role)|n}
</table>
		</td>
		<td>
<table>
	<tr><th colspan="2">${_("Description")}</th></tr>
	${common.render_short_field(fieldset.name)|n}
	${common.render_short_field(fieldset.join_date)|n}
	${common.render_short_field(fieldset.avatar)|n}
</table>
		</td>
	</tr>
</table>
