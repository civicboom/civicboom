<%namespace name="common" file="/admin/classes/common.mako" />

${common.style()}
${common.errors(fieldset)}

<table>
	<tr><th colspan="2">Content</th></tr>
	${common.render_short_field(fieldset.source)|n}
	${common.render_short_field(fieldset.target)|n}
	${common.render_short_field(fieldset.timestamp)|n}
	${common.render_short_field(fieldset.text)|n}
</table>
