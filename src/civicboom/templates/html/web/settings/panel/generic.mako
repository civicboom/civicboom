<%inherit file="/html/web/common/frag_container.mako"/>

<%namespace name="frag" file="/frag/common/frag.mako"/>
<%namespace name="generic_settings" file="/frag/settings/panel/generic.mako" import="body"/>

<%def name="title()">Settings</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <%
        self.attr.frags = [menu, generic]
        self.attr.frag_col_sizes = [1,2]
    %>
</%def>

<%def name="menu()">
  <%include file="/frag/settings/menu.mako"/>
</%def>

<%def name="generic()">
  ${frag.frag_basic( frag_content=generic_settings.body)}
</%def>

<%def name="help()">
  <!--#include file="/help/settings"-->
</%def>
