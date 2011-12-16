<%inherit file="/html/web/common/html_base.mako"/>
<%def name="title()">${_("Feeds")}</%def>

<p><a href="${url('new_feed')}">${_("new")}</a>

<hr>

${h.form(url('feeds', format='redirect'), method="post")}
	${_("Name:")} <input type="text" name="name" placeholder="e.g. Sport in Whitstable">
	<p><input type="submit">
${h.end_form()}

<hr>

<ul>
% for f in c.result['data']['feeds']:
	<li>
		<a href="${url('feed', id=f['id'])}">${f['name']}</a>
		(<a href="${url('edit_feed', id=f['id'])}">${_("edit")}</a>)
	</li>
% endfor
</ul>
