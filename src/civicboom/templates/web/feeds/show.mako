<h1>${c.result['data']['name']}</h1>
<hr>
% for r in c.result['data']['results']:
	<p><a href="${url('content', id=r.id)}">${r.title}</a>
% endfor
