<%def name="content_list(results)">
<table id="content_list">
% for r in results:
	<tr>
		<td class="avatar">
			<a href="${url(controller='user', action='view', id=r.creator.username)}">
				<img class='avatar' src="${r.creator.avatar_url}"><br>
				${r.creator.name}
			</a>
		</td>
		<td>
			<b style="float: right; text-align: right;">
				${str(r.update_date)[0:16]}
				<br>${ungettext("%d response", "%d responses", len(r.responses)) % len(r.responses)}
			</b>
			<b>
				<a href="${url(controller='content', action='view', id=r.id)}">${r.title}</a>
			</b>
			<br>${r.content[0:75]}... <!-- FIXME: truncate function -->
			<p>&nbsp;<br><b style="float: right; text-align: right;">
				<a href="${url(controller='content', action='view', id=r.id)}">${_("Read More")} &rarr;</a>
			</b>
		</td>
		
	</tr>
% endfor
</table>
</%def>
