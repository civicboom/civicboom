<%inherit file="/rss/rss_base.mako"/>

${d}


<%doc>
% for content in d['list']:
<item> 
    <title>${content['title']}</title> 
    <link>${content['url']}</link> 
    <description>${content['content_short']}</description> 
    <pubDate>Tue, 25 Oct 2005 15:42:32 -0700</pubDate> 
    <guid isPermaLink="false">Civicboom Content #${content['id']}</guid> 
    % if content['location']:
        <%
        lat, lon = content['location'].split(' ')
        %>
        <georss:point>${lat} ${lon}</georss:point> 
        <geo:lat>${lat}</geo:lat><geo:long>${lon}</geo:long>
    % endif
</item>
% endfor
</%doc>