<%inherit file="/rss/rss_base.mako"/>

<%def name="title()">${_("_site_name Search Results")}</%def>

<%def name="body()">
    % for content in d['list']:
        ${self.rss_content_item(content)}
    % endfor
</%def>