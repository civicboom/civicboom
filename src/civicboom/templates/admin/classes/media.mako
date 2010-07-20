<%namespace name="common" file="/admin/classes/common.mako" />

${common.style()}
${common.errors(fieldset)}

<table class="outer">
	<tr>
		<td>
<table>
	<tr><th colspan="2">${_("Content")}</th></tr>
	${common.render_short_field(fieldset.name)|n}
	${common.render_short_field(fieldset.type)|n}
	${common.render_short_field(fieldset.subtype)|n}
	${common.render_short_field(fieldset.caption)|n}
	${common.render_short_field(fieldset.credit)|n}
	${common.render_short_field(fieldset.attached_to)|n}
</table>
		</td>
		<td>
<table>
	<tr><th>${_("Media")}</th></tr>
	<tr><td>FIXME: preview goes here</td></tr>
</table>
		</td>
	</tr>
</table>
