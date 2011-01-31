<%inherit file="/rss/rss_base.mako"/>
<%def name="title()">${_("Responses to %s") % d.get('content',dict()).get('title')}</%def>

<%def name="body()">
    % for content in d['responses']['items']:
        ${self.rss_content_item(content)}
    % endfor
    % for content in d['comments']['items']:
        ${self.rss_comment_item(content)}
    % endfor
</%def>