<%inherit file="/rss/rss_base.mako"/>
<%
from datetime import datetime
%>
% for content in d['list']:
<item> 
	<description>${content['content']}</description> 
	<pubDate>${datetime.strptime(content['creation_date'][0:19], "%Y-%m-%d %H:%M:%S").strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate> 
	<dc:creator>${content['creator']['name']} (${content['creator']['username']})</dc:creator>
</item>
% endfor
