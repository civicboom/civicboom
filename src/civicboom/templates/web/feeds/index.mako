<h1>Feeds</h1>
<p><a href="${url('new_feed')}">new</a>
<hr>
${h.form(url('feeds', format='redirect'), method="POST")}
Name: <input type="text" name="name">
<p><input type="submit">
${h.end_form()}
<hr>
% for f in c.result['data']['feeds']:
	<p><a href="${url('feed', id=f['id'])}">${f['name']}</a>
	(<a href="${url('edit_feed', id=f['id'])}">edit</a>)
% endfor
