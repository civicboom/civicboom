# -*- coding: utf-8 -*-
<!--
vim:ft=html
-->
<%namespace name="common" file="/forms/classes/common.mako" />

${common.style()}
${common.errors(fieldset)}

<table class="outer">
	<tr>
		<td>
<table>
	<tr><th colspan="2">General</th></tr>
	${common.render_short_field(fieldset.creator)|n}
	${common.render_short_field(fieldset.parent)|n}
	${common.render_short_field(fieldset.creation_date)|n}
	${common.render_short_field(fieldset.responses)|n}
</table>
		</td>
		<td>
<table>
	<tr><th colspan="2">Content</th></tr>
	${common.render_short_field(fieldset.title)|n}
	${common.render_short_field(fieldset.content)|n}
	${common.render_short_field(fieldset.attachments)|n}
</table>
		</td>
	</tr>
</table>
