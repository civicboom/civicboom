<%inherit file="/html/web/common/frag_container.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------

<%def name="title()">${_('Sign in or Sign up')}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <%        
        self.attr.frags = [signin]
        
        if hasattr(c,'action_objects'):
            if c.action_objects.get('frag_url'):
                self.attr.frags.append(action_object_frag)
                self.attr.action_object_frag_url = c.action_objects['frag_url'] + '?exclude_actions=all'
                
    %>
</%def>

<%def name="signin()">
    <%include file="/frag/account/signin.mako"/>
</%def>

<%def name="action_object_frag()">
    <!--#include file="${self.attr.action_object_frag_url}"-->
</%def>
