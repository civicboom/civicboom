<%inherit file="/web/common/html_base.mako"/>
<%def name="title()">${_("Feeds: ")+d['name']}</%def>

% for r in d['results']:
	<p><a href="${url('content', id=r['id'])}">${r['title']}</a>
% endfor
