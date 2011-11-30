<%inherit file="/ics/ics_base.mako"/>

<%! import pprint %>

<%def name="body()">\
% for l in d.values():
    % if isinstance(l, dict) and l.get('type')=='contents':
        % for content in l['items']:
${self.ics_content_item(content)}\
        % endfor
    % endif
% endfor
</%def>
