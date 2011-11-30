<%inherit file="/ics/ics_base.mako"/>

<%def name="body()">\
    % for content in d['list']['items']:
${self.ics_content_item(content)}\
    % endfor
</%def>