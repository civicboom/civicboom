<%! from datetime import datetime %>

<%def name="title()"      >${_('_site_name RSS')}</%def>
<%def name="description()">${_("News and articles from _site_name")}</%def>

##------------------------------------------------------------------------------
## RSS Base
##------------------------------------------------------------------------------

<%def name="body()"><?xml version="1.0" encoding="utf-8"?>
<rss
	version="2.0"
	xmlns:media  = "http://search.yahoo.com/mrss/"
	xmlns:dc     = "http://purl.org/dc/elements/1.1/"
    ## w3c rss validator recommends the latter
	##xmlns:creativeCommons="http://cyber.law.harvard.edu/rss/creativeCommonsRssModule.html"
	xmlns:creativeCommons="http://backend.userland.com/creativeCommonsRssModule"
	## Reference http://www.georss.org/Main_Page
	xmlns:geo    = "http://www.w3.org/2003/01/geo/wgs84_pos#"
	xmlns:georss = "http://www.georss.org/georss"
	xmlns:gml    = "http://www.opengis.net/gml"
	xmlns:woe    = "http://where.yahooapis.com/v1/schema.rng"
	xmlns:wfw    = "http://wellformedweb.org/CommentAPI/"
>
    <channel>
        <title        >${self.title()}</title>
        <link         >${h.url('current', qualified=True)}</link>
        <description  >${self.description()}</description>
        <pubDate      >${datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate>
        <lastBuildDate>${datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")}</lastBuildDate>
        <generator    >${h.url(controller='misc', action='titlepage', sub_domain='www', qualified=True)}</generator>
        <image>
            <url>${h.wh_url('public', 'images/rss_large.png')}</url>
            <title>${self.title()}</title>
            <link>${h.url('current', qualified=True)}</link>
        </image>
        
        ${next.body()}
        
    </channel>
</rss>
</%def>

##------------------------------------------------------------------------------
## RSS Content Item
##------------------------------------------------------------------------------

<%def name="rss_content_item(content)">
    <item>
        <title>${content['title']}</title>
        <link>${h.url('content', id=content['id'], qualified=True)}</link> 
        <description>${content.get('content', content.get('content_short'))}</description> 
        <pubDate>${h.date_to_rss(content.get('update_date'))}</pubDate>
        <guid isPermaLink="false">Content #${content['id']}</guid>
        % for tag in content.get('tags', []):
        <category>${tag}</category>
        % endfor
        <dc:creator>${content.get('creator',dict()).get('name')} (${content.get('creator',dict()).get('username')})</dc:creator>
        ## Comments - http://wellformedweb.org/news/wfw_namespace_elements/
        <wfw:commentRss>${h.url('content_action', action='comments', id=content['id'], format='rss', qualified=True)}</wfw:commentRss>
        ##<!-- <creativeCommons:license>license url here</creativeCommons:license> -->
        % if 'thumbnail_url' in content:
        <media:thumbnail url="${content['thumbnail_url']}" />
        ##width="80" height="60"
        % endif
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
            ## <!-- having both types of attachment means that it shows up twice in RSS readers; do we need both? -->
            ## Standard RSS 2.0 Media enclosure
            ##<enclosure url="${media['media_url']}" length="${media['filesize']}" type="${media['type']}/${media['subtype']}" />
            % endfor
        % endif
		##
        % if content['location']:
        <% lon, lat = content['location'].split(' ') %>
        <georss:point>${lat} ${lon}</georss:point>
        <geo:lat>${lat}</geo:lat><geo:long>${lon}</geo:long>
        % endif
    </item>\
</%def>

##------------------------------------------------------------------------------
## RSS Member Item
##------------------------------------------------------------------------------

<%def name="rss_comment_item(comment)">
<item>
    ##% if content['type'] == 'comment':
    <% name = comment.get('creator', dict()).get('name') %>
    <title>${_('Comment by')}: ${name} - ${h.truncate(comment['content'], length=50, whole_word=True, indicator='...')}</title>
    <description>${comment.get('content')}</description>
    <pubDate>${h.date_to_rss(comment.get('creation_date'))}</pubDate>
    <dc:creator>${name}</dc:creator>
</item>
</%def>


##------------------------------------------------------------------------------
## RSS Member Item
##------------------------------------------------------------------------------

<%def name="rss_member_item(member)">
    <item> 
        <title>${member['name']}</title> 
        <link>${h.url('member', id=member['username'], qualified=True)}</link>
        <category>${member['type']}</category>
        <guid isPermaLink="false">Member #${member['id']}</guid>
        % if 'description' in member:
        <description>${member['description']}</description>
        % endif
        % if 'join_date' in member:
        <pubDate>${member['join_date']}</pubDate>
        % endif
        % if 'avatar_url' in member:
        <media:thumbnail url="${member['avatar_url']}" />
        ##<enclosure url="${member['avatar_url']}" type="image/jpeg" />
        % endif
        ## locaiton?
    </item>
</%def>
