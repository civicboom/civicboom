<%inherit file="/ics/ics_base.mako"/>

<%def name="body()">\
${self.ics_content_item(d['content'])}\
</%def>