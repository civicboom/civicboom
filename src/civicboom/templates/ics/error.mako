<%inherit file="/rss/rss_base.mako"/>

<%def name="title()">
    Error
    % if c.result:
        ${c.result.get('code')}
    % endif
</%def>
<%def name="description()">
    % if c.result:
        ${c.result.get('message')}
    % endif
</%def>

<%def name="body()">
</%def>
