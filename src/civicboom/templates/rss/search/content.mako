<%inherit file="/rss/rss_base.mako"/>
<%
from datetime import datetime
%>
% for content in d['list']:
<item> 
	<title>${content['title']}</title> 
	<link>${content['url']}</link> 
	<description>${content['content_short']}</description> 
	<pubDate>${datetime.strptime(content['creation_date'][0:19], "%Y-%m-%d %H:%M:%S").strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate> 
	<guid isPermaLink="false">Civicboom Content #${content['id']}</guid>
	<category>${content['tags']}</category>
	<dc:creator>${content['creator']['name']} (${content['creator']['username']})</dc:creator>
##
% if 'attachments' in content:
	% for media in content['attachments']:
	## http://video.search.yahoo.com/mrss
	<media:content url="${media['media_url']}" fileSize="${media['filesize']}" type="${media['type']}/${media['subtype']}" expression="full">
		<media:thumbnail url="${media['thumbnail_url']}" />
		<media:title     type="plain"                 >${media['caption']}</media:title>
		<media:credit    role="owner" scheme="urn:yvs">${media['credit'] }</media:credit>
		<media:community>
			% if 'rating' in content:
			<media:starRating average="${content['rating']}" />
			% endif
			% if 'views' in content:
			<media:statistics views="${content.get('rating')}" favorites="${content.get('boom_count')}" />
			% endif
			##<media:tags>news: 5, abc:3, reuters </media:tags>
		</media:community>
	% if content['location']:
		<media:location>
			<georss:where>
				<gml:Point>
					<gml:pos>${content['location']}</gml:pos>
				</gml:Point>
			</georss:where>
		</media:location>
	% endif
	</media:content>
	##
	## Standard RSS 2.0 Media enclosure
	<enclosure url="${media['media_url']}" length="${media['filesize']}" type="${media['type']}/${media['subtype']}" />
	% endfor
% endif
##
% if content['location']:
<%
lat, lon = content['location'].split(' ')
%>
	<georss:point>${lat} ${lon}</georss:point>
	<geo:lat>${lat}</geo:lat><geo:long>${lon}</geo:long>
% endif
</item>
% endfor
