<%inherit file="/ics/ics_base.mako"/>

<%def name="body()">\
% for list in d['featured'].values():
    % for content in list['items']:
${self.ics_content_item(content)}\
    % endfor
% endfor
</%def>