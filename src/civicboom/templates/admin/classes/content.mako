<%namespace name="common" file="/admin/classes/common.mako" />

${common.errors(fieldset)}

<table class="outer">
	<tr>
		<td>
<table>
	<tr><th colspan="2">${_("General")}</th></tr>
	${common.render_short_field(fieldset.creator)|n}
	##${common.render_short_field(fieldset.status.dropdown(options=["pending", "show", "locked"]))|n}
    ${common.render_short_field(fieldset.edit_lock.dropdown(options=["none", "parent_owner", "group", "system"]))|n} ##AllanC this can be set to None and "none" is not needed - see model
    ${common.render_short_field(fieldset.visable)|n}
	${common.render_short_field(fieldset.private)|n}
	${common.render_short_field(fieldset.parent)|n}
</table>
<table>
	<tr><th colspan="2">${_("Content")}</th></tr>
	${common.render_short_field(fieldset.title)|n}
	${common.render_short_field(fieldset.content)|n}
	${common.render_short_field(fieldset.attachments)|n}
	${common.render_short_field(fieldset.tags)|n}
</table>
		</td>
		<td>
<table>
	<tr><th colspan="2">${_("Timeline")}</th></tr>
	${common.render_short_field(fieldset.creation_date)|n}
	${common.render_short_field(fieldset.update_date)|n}
	${common.render_short_field(fieldset.edits)|n}
</table>
<table>
	<tr><th colspan="2">${_("Other")}</th></tr>
	${common.render_short_field(fieldset.responses)|n}
	${common.render_short_field(fieldset.location)|n}
	${common.render_short_field(fieldset.flags)|n}
</table>
		</td>
	</tr>
</table>
