<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="title()">General Settings</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <%
        self.attr.frags = [menu, generic, help]
        self.attr.frag_col_sizes = [1,2,1]
    %>
</%def>

<%def name="menu()">
  <%include file="/frag/settings/menu.mako"/>
</%def>

<%def name="generic()">
  <%include file="/frag/settings/panel/generic.mako"/>
</%def>

<%def name="help()">
  <!--#include file="/help/settings"-->
</%def>