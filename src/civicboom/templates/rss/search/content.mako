<%
# we need to pass the session to GeoAlchemy functions
from civicboom.model.meta import Session
%>
<rss version="2.0"
		xmlns:media="http://search.yahoo.com/mrss/"
		xmlns:dc="http://purl.org/dc/elements/1.1/"
		xmlns:creativeCommons="http://cyber.law.harvard.edu/rss/creativeCommonsRssModule.html"
		xmlns:georss="http://www.georss.org/georss">
	<channel> 
		<title>Civicboom Search Results</title> 
		<link>http://www.civicboom.com/search/</link> 
 		<description>Search Results</description> 
		<pubDate>Thu, 22 Mar 2007 19:08:17 -0700</pubDate> 
		<lastBuildDate>Thu, 22 Mar 2007 19:08:17 -0700</lastBuildDate> 
		<generator>http://www.civicboom.com/</generator> 
 
		% for r in results:
		<item> 
			<title>${r.title}</title> 
			<link>${url(controller='content', action='view', id=r.id)}</link> 
			<description>${r.content}</description> 
			<pubDate>Tue, 25 Oct 2005 15:42:32 -0700</pubDate> 
			<guid isPermaLink="false">tag:flickr.com,2004:/grouppool/322338@N20/photo/56104498</guid> 
			% if r.location:
			<georss:point>${r.location.coords(Session)[0]} ${r.location.coords(Session)[1]}</georss:point> 
			<!--
			<geo:lat>${r.location.coords(Session)[1]}</geo:lat>
			<geo:long>${r.location.coords(Session)[0]}</geo:long>
			-->
			% endif
		</item>
		% endfor
	</channel>
</rss>
