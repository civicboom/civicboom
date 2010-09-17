<h1>Feeds</h1>
<p><a href="${url('new_feed')}">new</a>
% for f in c.result['data']['feeds']:
	<p><a href="${url('feed', id=f['id'])}">${f['name']}</a>
	(<a href="${url('edit_feed', id=f['id'])}">edit</a>)
% endfor
