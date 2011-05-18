<%inherit file="base_email_from_plaintext.mako"/>

<%def name="plaintext_after()">
    ${_('To alter your notificaiton settings click ')}<a href="${h.url('settings', id='me', action='notifications')}">${_('here')}</a>
</%def>