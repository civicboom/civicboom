<%inherit file="/rss/rss_base.mako"/>

<%def name="body()">
    % for content in d['list']['items']:
    <item> 
        <description>${content['content']}</description>
        <pubDate>${h.date_to_rss(content.get('creation_date'))}</pubDate>
        ## ${datetime.strptime(content['creation_date'][0:19], "%Y-%m-%d %H:%M:%S").strftime("%a, %d %b %Y %H:%M:%S +0000")}
        <dc:creator>${content.get('creator', dict()).get('name')} (${content.get('creator',dict()).get('username')})</dc:creator>
    </item>
    % endfor
</%def>