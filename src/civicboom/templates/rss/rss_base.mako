<%! from datetime import datetime %>

<%def name="title()"      >${_('_site_name RSS')}</%def>
<%def name="description()">${_("News and articles from _site_name")}</%def>

##------------------------------------------------------------------------------
## RSS Base
##------------------------------------------------------------------------------

<%def name="body()"><?xml version="1.0" encoding="utf-8"?>
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
    <channel>
        <title        >${self.title()}</title>
        <link         >${h.url('current', subdomain='www')}</link>
        <description  >${self.description()}</description>
        <pubDate      >${datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate>
        <lastBuildDate>${datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")}</lastBuildDate>
        <generator    >http://www.civicboom.com/</generator>
        <image url  ="/images/rss_large.png"
               link ="${h.url('current', subdomain='www')}"
               title="${_('_site_name')}"
        />
        
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
        <link>${url('content', id=content['id'], subdomain='www')}</link> 
        <description>${content['content_short']}</description> 
        <pubDate>${h.date_to_rss(content.get('update_date'))}</pubDate>
        <guid isPermaLink="false">Civicboom Content #${content['id']}</guid>
        % if 'tags' in content:
        <category>
            % for tag in content['tags']:
            ${tag}, 
            % endfor
        </category>
        % endif
        <dc:creator>${content.get('creator',dict()).get('name')} (${content.get('creator',dict()).get('username')})</dc:creator>
        ## Comments - http://wellformedweb.org/news/wfw_namespace_elements/
        ##<wfw:comment   >${url('contents', parent_id=content['id'], type='comment', format='rss', host=app_globals.site_host)}</wfw:comment>
        <wfw:commentRss>${url('content_actions', action='comments', id=content['id'], format='rss', subdomain='www')}</wfw:commentRss>
        <!-- <creativeCommons:license>license url here</creativeCommons:license> -->
        
        ##% if 'thumbnail_url' in content:
            ## AllanC :( Broken  .. WHY!!! WHY!!!
            ## With this line enabled ... it wont show up in firefox .. the entire entry is not displayed
            ##<enclosure url="${content['thumbnail_url']}" length="0" type="image/png"/>
            ## cant guaranete that it's a jpeg because placeholders are pngs :(
        ##% endif
        
        % if 'attachments' in content:
            % for media in content['attachments']:
            <%doc>
            <!-- having both types of attachment means that it shows up twice in RSS readers; do we need both? -->
            <!--
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
            -->
            </%doc>
            ##
            ## Standard RSS 2.0 Media enclosure
            <enclosure url="${media['media_url']}" length="${media['filesize']}" type="${media['type']}/${media['subtype']}" />
            % endfor
        % endif
        
        % if content['location']:
        <% lat, lon = content['location'].split(' ') %>
        <georss:point>${lat} ${lon}</georss:point>
        <geo:lat>${lat}</geo:lat><geo:long>${lon}</geo:long>
        % endif
    
    </item>
</%def>

##------------------------------------------------------------------------------
## RSS Member Item
##------------------------------------------------------------------------------

<%def name="rss_comment_item(comment)">
<item>
    ##% if content['type'] == 'comment':
    <% name = comment.get('creator', dict()).get('name') or comment.get('creator', dict()).get('username') %>
    <title>${_('Comment by')}: ${name} - ${h.truncate(comment['content'], length=50, whole_word=True, indicator='...')}</title>
    <description>${comment['content']}</description>
    <pubDate>${h.date_to_rss(comment.get('creation_date'))}</pubDate>
    ## ${datetime.strptime(content['creation_date'][0:19], "%Y-%m-%d %H:%M:%S").strftime("%a, %d %b %Y %H:%M:%S +0000")}
    <dc:creator>${name}</dc:creator>
</item>
</%def>


##------------------------------------------------------------------------------
## RSS Member Item
##------------------------------------------------------------------------------

<%def name="rss_member_item(member)">
    <item> 
        <title>${member['name'] or member['username']}</title> 
        <link>${url('member', id=member['username'], subdomain='www')}</link>
        <category>${member['type']}</category>
        % if 'description' in member:
        <description>${member['description']}</description>
        % endif
        ##<pubDate>${h.datetime_to_rss(h.api_datestr_to_datetime(content['creation_date']))}</pubDate> 
        <guid isPermaLink="false">Civicboom Member #${member['id']}</guid>

    ##% if 'thumbnail_url' in member:
    ##    <enclosure url="${member['thumbnail_url']}" type="image/jpeg" />
    ##% endif
        
        ## locaiton?
    </item>
</%def>