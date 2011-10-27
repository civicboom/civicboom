<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="title()">${_("New _article")}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <% self.attr.frags = new_content %>
</%def>

<%def name="new_content()">
    ##<!--#include virtual="${h.url(controller='misc', action='new_content', format='frag')}"-->
    <%include file="/frag/misc/new_content.mako"/>
</%def>
