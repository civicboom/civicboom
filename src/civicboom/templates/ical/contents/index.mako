<%inherit file="/ical/ical_base.mako"/>

<%def name="body()">
    % for content in d['list']['items']:
        ${self.ical_content_item(content)}
    % endfor
</%def>