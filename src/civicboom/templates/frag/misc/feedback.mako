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
    
    ${h.form(h.url(controller='misc', action='feedback', format='redirect'), method='POST')}
        % if current_referer():
        <input type="hidden" name="referer" value="${quote_plus(current_referer())}"/>
        % endif
        
        <table>
            <tr>
                <td>${_('Category')}</td>
                <td>
                    <select name="category">
                      <option value="bug"    >${_('Reoort a bug')}</option>
                      <option value="feature">${_('Feature request')}</option>
                      <option value="opinion">${_('Opinion')}</option>
                      <option value="other"  >${_('Other')}</option>
                    </select>
                </td>
            </tr>
            
            <tr>
                <td>${_('Message')}</td>
                <td>
                    <textarea name="message" placeholder="${_('Please tell us about your experience/problems to help us improve _site_name')}"></textarea>
                </td>
            </tr>
            
            % if not c.logged_in_user:
            <tr>
                <td>${_('Contact email')}</td>
                <td>
                    <input type="text" name="from" />
                </td>
            </tr>
            % endif
        </table>
        
        <input type="submit" name="submit" value="submit"/>
    </form>
    
</%def>