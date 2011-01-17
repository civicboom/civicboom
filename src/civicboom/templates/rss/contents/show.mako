<%inherit file="/rss/rss_base.mako"/>
<%def name="title()">${_("Responses to %s") % d.get('content',dict()).get('title')}</%def>

<%def name="body()">
    % for content in d['responses']:
        ${self.rss_content_item(content)}
    % endfor
</%def>