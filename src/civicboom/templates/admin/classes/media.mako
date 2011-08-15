<%namespace name="common" file="/admin/classes/common.mako" />

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
	<tr><td style="text-align: center">
		## FIXME: hack because we don't have access to Media.media_url or the like
		<% base = config['warehouse.url'] %>
		<p><img src="${base}/media-thumbnail/${fieldset.hash.value}">
		<p><a href="${base}/media-original/${fieldset.hash.value}">Original</a>,
		<a href="${base}/media/${fieldset.hash.value}">Processed</a>,
		<a href="${base}/media-thumbnail/${fieldset.hash.value}">Thumbnail</a>
	</td></tr>
</table>
		</td>
	</tr>
</table>
