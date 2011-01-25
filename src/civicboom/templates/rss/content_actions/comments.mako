<%inherit file="/rss/rss_base.mako"/>

<%def name="body()">
    % for content in d['list']['items']:
        ${self.rss_comment_item(content)}
    % endfor
</%def>