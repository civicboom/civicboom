<%inherit file="/frag/common/frag.mako"/>
##<%inherit file="/html/web/common/html_base.mako"/>
<%!
    import webhelpers.constants
%>

<%namespace name="upgrade_plans" file="/html/web/misc/about/upgrade_plans.mako"/>
<%namespace name="edit_frag"     file="/frag/payments/edit.mako"/>
<%def name="body()">
    <%
        if d:
            self.account = d.get('payment', {})
            self.invalid = d.get('invalid', {})
        else:
            self.account = {'name_type': c.logged_in_user.extra_fields.get('help_type', 'ind')}
            self.invalid = {}
    %>
    <div class="frag_whitewrap">
        ${h.form('/payments')}
        <h1>${_('Just a few details before we can upgrade your account')}</h1>
        ${edit_frag.form_content(self)}
        <p>
            ${_('By clicking Create below you confirm you agree to our Terms and Conditions.')}
        </p>
        <div class="terms-75">
            ${upgrade_plans.upgrade_details('create_account')}
        </div>
        ${h.end_form()}
    </div>
</%def>