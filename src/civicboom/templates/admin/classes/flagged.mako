<%namespace name="common" file="/admin/classes/common.mako" />

${common.errors(fieldset)}

<table class="outer">
	<tr>
		<td>
<table>
	<tr><th colspan="2">${_("Article")}</th></tr>
	<tr class="input_row"><td>Content</td><td><a href="/admin/Content/models/${fieldset.content_id.render()}/edit">${(fieldset.content.render())|n}</a></td></tr>
	${common.render_short_field(fieldset.timestamp)|n}
</table>
		</td>
		<td>
<table>
	<tr><th colspan="2">${_("Report")}</th></tr>
	${common.render_short_field(fieldset.member)|n}
	${common.render_short_field(fieldset.type)|n}
	${common.render_short_field(fieldset.comment)|n}
</table>
		</td>
	</tr>
</table>
