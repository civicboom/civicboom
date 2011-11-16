<%inherit file="/email/base_email_content.mako"/>

<%def name="body()"></%def>

<%def name="content()">
    <h1>${_('Notification Summary')}</h1>
    % for message in messages:
        ${message}
    % endfor
</%def>