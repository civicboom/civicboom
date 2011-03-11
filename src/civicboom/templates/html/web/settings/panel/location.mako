<%inherit file="/html/web/common/frag_container.mako"/>

<%namespace name="frag" file="/frag/common/frag.mako"/>
<%namespace name="location_settings" file="/frag/settings/panel/location.mako" import="body,title"/>

<%def name="title()">General Settings</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <%
        self.attr.frags = [menu, location, help]
        self.attr.frag_col_sizes = [1,2,1]
    %>
</%def>

<%def name="menu()">
  <%include file="/frag/settings/menu.mako"/>
</%def>

<%def name="location()">
  ${frag.frag_basic(title=location_settings.title, icon='group', frag_content=location_settings.body)}
</%def>

<%def name="help()">
  <!--#include file="/help/settings"-->
</%def>