<%inherit file="/rss/rss_base.mako"/>

<%def name="title()">${_("_site_name _content search results")}</%def>

<%def name="body()">
    % for content in d['list']['items']:
        ${self.rss_content_item(content)}
    % endfor
</%def>