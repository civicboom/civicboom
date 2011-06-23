##<%inherit file="/frag/common/frag.mako"/>

<%!
    from urllib import quote_plus, unquote_plus
    from civicboom.lib.web import current_referer
%>

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------
## depricated! - this returns just the frag form
<%def name="init_vars()">
    <%
        self.attr.title     = _('Feedback')
        self.attr.icon_type = 'dialog'
    %>
</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
    ${feedback_form()}
</%def>

##------------------------------------------------------------------------------
## Feedback form
##------------------------------------------------------------------------------
<%def name="feedback_form()">
<style>
TABLE.feedback INPUT,
TABLE.feedback SELECT {
	width: 100%;
}
</style>
    ${h.form(h.args_to_tuple(controller='misc', action='feedback', format='redirect'), method='POST', json_form_complete_actions="cb_frag_remove(current_element);")}
        % if current_referer():
        <input type="hidden" name="referer" value="${quote_plus(current_referer())}"/>
        % endif
        
        <table class="feedback">
            <tr>
                <td>${_('Category')}</td>
                <td style="padding: 3px 0 0 3px">
                    <select name="category">
                      <option value="bug"    >${_('Report a bug')}</option>
                      <option value="feature">${_('Feature request')}</option>
                      <option value="opinion">${_('Opinion')}</option>
                      <option value="other"  >${_('Other')}</option>
                    </select>
                </td>
            </tr>
            
            <tr>
                <td>${_('Message')}</td>
                <td style="padding: 3px 0 0 3px">
                    <p>${_('Tell us about your experience/problems to help us improve _site_name.')}</p>
                    <p>${_('Please provide as much detail as possible')}</p>
                    <textarea name="message" style="width: 450px; height: 200px;" placeholder="">
${_('What were you previously doing:')}

${_('What were you trying to do:')}

${_('What did you expect to happen:')}

                    </textarea>
                </td>
            </tr>
            
            % if not c.logged_in_user:
            <tr>
                <td>${_('Contact email')}</td>
                <td style="padding: 3px 0 0 3px">
                    <input type="text" name="from" />
                </td>
            </tr>
            <tr>
                <td>${_('Prove you are human:')}</td>
                <td>
                    <input type="text" name="simple_captcha" />
                    <p>${_('type "xyz" into this box')}</p>
                </td>
            </tr>
            % endif

			<tr>
		        <td style="padding: 3px 0 0 3px" colspan="2"><input type="submit" name="submit" value="Send message"/></td>
			</tr>
        </table>
    </form>
    <br />
    <a href="mailto:feedback@civicboom.com">${_("Alternatively, email us your feedback")}</a>
    
</%def>
