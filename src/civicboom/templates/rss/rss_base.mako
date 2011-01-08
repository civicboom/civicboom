<?xml version="1.0" encoding="utf-8"?>
<rss
	version="2.0"
	xmlns:media="http://search.yahoo.com/mrss/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:creativeCommons="http://cyber.law.harvard.edu/rss/creativeCommonsRssModule.html"
	## Reference http://www.georss.org/Main_Page
	xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#"
	xmlns:georss="http://www.georss.org/georss"
	xmlns:gml="http://www.opengis.net/gml"
	xmlns:woe="http://where.yahooapis.com/v1/schema.rng"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
>
<%
from datetime import datetime
%>
<channel>
	<title        >${next.title()}</title>
	<link         >${url.current(host=app_globals.site_host)}</link>
	<description  >${_("News and articles from _site_name")}</description>
	<pubDate      >${datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate>
	<lastBuildDate>${datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")}</lastBuildDate>
	<generator    >http://www.civicboom.com/</generator>
	<image url  ="/images/rss_large.png"
		   link ="${url.current(host=app_globals.site_host)}"
		   title="${_('_site_name')}"
	/>
	
	${next.body()}
        
	</channel>
</rss>
