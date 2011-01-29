<%inherit file="/html/web/common/frag_container.mako"/>

<%!
    from civicboom.lib.web import cookie_get
%>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------

<%def name="title()">${_('Signin or Signup')}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <%        
        self.attr.frags = [signin]
        
        self.attr.action_object_url = None
        args, kwargs = h.get_object_from_action_url( cookie_get('login_redirect') )
        if args and kwargs:
            kwargs['format'] = 'frag'
            self.attr.action_object_url = url(*args, **kwargs)
        
        if action_object_url:
            self.attr.frags.append(action_object_frag)
    %>
</%def>

<%def name="signin()">
    <%include file="/frag/account/signin.mako"/>
</%def>

<%def name="action_object_frag()">
    <!--#include file="${action_object_url}"-->
</%def>