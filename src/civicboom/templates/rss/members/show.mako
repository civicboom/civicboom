<%inherit file="/rss/rss_base.mako"/>
<%def name="title()">${d['member']['name']}</%def>

<%def name="body()">
    % for content in d['content']:
        ${self.rss_content_item(content)}
    % endfor
</%def>