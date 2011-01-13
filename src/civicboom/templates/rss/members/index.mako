<%inherit file="/rss/rss_base.mako"/>
<%def name="title()">Member Search Results</%def>

% for member in d['list']:
<item> 
	<title>${member['name'] or member['username']}</title> 
	<link>${url('member', id=member['id']}</link> 
	<description>${member['description']}</description> 
	##<pubDate>${h.datetime_to_rss(h.api_datestr_to_datetime(content['creation_date']))}</pubDate> 
	<guid isPermaLink="false">Civicboom Member #${member['id']}</guid>
    
    ## locaiton?
</item>
% endfor