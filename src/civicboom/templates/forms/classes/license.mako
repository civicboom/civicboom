<%namespace name="common" file="/forms/classes/common.mako" />

${common.style()}
${common.errors(fieldset)}

<table>
	<tr><th colspan="2">Content</th></tr>
	${common.render_short_field(fieldset.code)|n}
	${common.render_short_field(fieldset.name)|n}
	${common.render_short_field(fieldset.url)|n}
	${common.render_short_field(fieldset.description)|n}
</table>
