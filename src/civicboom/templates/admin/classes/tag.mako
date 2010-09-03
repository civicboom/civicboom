<%namespace name="common" file="/admin/classes/common.mako" />

${common.errors(fieldset)}

<table>
	<tr><th colspan="2">${_("Content")}</th></tr>
	${common.render_short_field(fieldset.name)|n}
	${common.render_short_field(fieldset.parent)|n}
</table>
