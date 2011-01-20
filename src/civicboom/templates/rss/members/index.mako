<%inherit file="/rss/rss_base.mako"/>

<%def name="title()">${_('_site_name _member search results')}</%def>

<%def name="body()">
    % for member in d['list']:
        ${self.rss_member_item(member)}
    % endfor
</%def>