# -*- coding: utf-8 -*-
<!--
vim:ft=html
-->
<%namespace name="common" file="/admin/classes/common.mako" />

${common.style()}
${common.errors(fieldset)}

<table class="outer">
	<tr>
		<td>
<table>
	<tr><th colspan="2">General</th></tr>
	${common.render_short_field(fieldset.creator)|n}
	${common.render_short_field(fieldset.status.dropdown(options=["pending", "show", "locked"]))|n}
	${common.render_short_field(fieldset.private)|n}
	${common.render_short_field(fieldset.parent)|n}
</table>
<table>
	<tr><th colspan="2">Content</th></tr>
	${common.render_short_field(fieldset.title)|n}
	${common.render_short_field(fieldset.content)|n}
	${common.render_short_field(fieldset.attachments)|n}
	${common.render_short_field(fieldset.tags)|n}
</table>
		</td>
		<td>
<table>
	<tr><th colspan="2">Timeline</th></tr>
	${common.render_short_field(fieldset.creation_date)|n}
	${common.render_short_field(fieldset.update_date)|n}
	${common.render_short_field(fieldset.edits)|n}
</table>
<table>
	<tr><th colspan="2">Other</th></tr>
	${common.render_short_field(fieldset.responses)|n}
	${common.render_short_field(fieldset.location)|n}
</table>
		</td>
	</tr>
</table>
