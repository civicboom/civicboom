<%inherit file="/email/base_email_content.mako"/>

## AllanC - ***ING mako wont render without a body, it complains about undefined c. .. wtf!
<%def name="body()"></%def>

<%def name="content_after()">
    <p>${_('To alter your email notifications visit your ')}<a href="${h.url('setting_action', id=kwargs.get('target_username','me'), action='notifications', protocol='https', sub_domain='www', qualified=True)}">${_('notification settings')}</a></p>
</%def>
