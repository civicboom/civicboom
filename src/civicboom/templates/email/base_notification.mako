<%inherit file="base_email_from_plaintext.mako"/>

<%def name="body()"></%def>

<%def name="plaintext_after()">
    <%
        username = 'me'
    %>
    <p>${_('To alter your notificaitons visit your ')}<a href="${h.url('setting_action', id=username, action='messages', sub_domain='www', qualified=True)}">${_('notification settings')}</a></p>
</%def>
