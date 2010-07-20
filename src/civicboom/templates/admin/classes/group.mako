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
	<tr><th colspan="2">Information</th></tr>
	${common.render_short_field(fieldset.username)|n}
	${common.render_short_field(fieldset.status.dropdown(options=["pending", "active", "removed"]))|n}
	${common.render_short_field(fieldset.members)|n}
</table>
		</td>
		<td>
<table>
	<tr><th colspan="2">Description</th></tr>
	${common.render_short_field(fieldset.name)|n}
	${common.render_short_field(fieldset.join_date)|n}
	${common.render_short_field(fieldset.avatar)|n}
	${common.render_short_field(fieldset.home_location)|n}
	${common.render_short_field(fieldset.webpage)|n}
	${common.render_short_field(fieldset.description)|n}
</table>
		</td>
	</tr>
</table>
