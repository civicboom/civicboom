<%inherit file="base_email_from_plaintext.mako"/>

<%def name="body()"></%def>

<%def name="plaintext_after()">
    ${_('To alter your notificaiton settings click ')}<a href="${h.url('setting_action', id='me', action='notifications', absolute=True)}">${_('here')}</a>
</%def>