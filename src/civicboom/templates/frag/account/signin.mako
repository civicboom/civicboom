<%inherit file="/frag/common/frag.mako"/>

<%namespace name="signin" file="/html/web/account/signin.mako"/>

##------------------------------------------------------------------------------
##
##------------------------------------------------------------------------------
<%def name="init_vars()">
    <%
        self.attr.title     = _('Signin or Signup ')
        self.attr.icon_type = 'boom'
    %>
</%def>  

##------------------------------------------------------------------------------
## Signin Fragment
##------------------------------------------------------------------------------
<%def name="body()">
    % if hasattr(c, 'action_objects'):
        ${c.action_objects['description']}
        ##${c.action_objects['action_object']}
    % endif
    ${signin.signin()}
    ${signin.signup()}
    ${signin.janrain()}
    ${signin.forgot()}
</%def>