<%inherit file="/ics/ics_base.mako"/>

<%def name="body()">\
    % for message in d['list']['items']:
${self.ics_message_item(message)}\
    % endfor
</%def>