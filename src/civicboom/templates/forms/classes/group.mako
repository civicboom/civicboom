# -*- coding: utf-8 -*-
<!--
vim:ft=html
-->
<%namespace name="common" file="/forms/classes/common.mako" />

${common.style()}
${common.errors(fieldset)}

<table>
	<tr>
		<td>
<table>
	${common.render_short_field(fieldset.username)|n}
	${common.render_short_field(fieldset.name)|n}
	${common.render_short_field(fieldset.join_date)|n}
	${common.render_short_field(fieldset.status.dropdown(options=["pending", "active", "removed"]))|n}
</table>
		</td>
		<td>
<table>
	${common.render_short_field(fieldset.avatar)|n}
	${common.render_short_field(fieldset.home_location)|n}
	${common.render_short_field(fieldset.webpage)|n}
	<tr>
		<td colspan="2">
			${fieldset.description.render()|n}
		</td>
	</tr>
</table>
		</td>
	</tr>
	<tr>
		<td colspan="2">
			Members:
			<br>${fieldset.members.render()|n}
		</td>
	</tr>
</table>
