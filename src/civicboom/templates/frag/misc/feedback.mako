<%inherit file="/frag/common/frag.mako"/>

<%!
    from urllib import quote_plus, unquote_plus
%>

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%def name="init_vars()">
    <%
        self.attr.title     = _('Feedback')
        self.attr.icon_type = 'dialog'
    %>
</%def>


##------------------------------------------------------------------------------
## Feedback form
##------------------------------------------------------------------------------
<%def name="body()">
    <form action="" method="post">
        <textarea name="message" placeholder="${_('Please tell us about your experience/problems to help us improve _site_name')}"></textarea>
        % if not c.logged_in_user:
        <input type="text" name="from" value=""/>
        % endif
        <%
            env = ''
            for key,value in request.environ.iteritems():
                env += "%s:%s\n" % (key,value)
        %>
        <input type="hidden" name="env" value="${env}"/>
        <input type="submit" name="submit" value="submit"/>
    </form>
</%def>