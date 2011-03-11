<%inherit file="/html/web/common/frag_container.mako"/>

<%namespace name="frag" file="/frag/common/frag.mako"/>
<%namespace name="link_janrain" file="/frag/settings/panel/link_janrain.mako" import="body,title"/>

<%def name="title()">Settings</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <%
        self.attr.frags = [menu, janrain, help]
        self.attr.frag_col_sizes = [1,2,1]
    %>
</%def>

<%def name="menu()">
  <%include file="/frag/settings/menu.mako"/>
</%def>

<%def name="janrain()">
  ${frag.frag_basic(title=link_janrain.title, icon='group', frag_content=link_janrain.body)}
</%def>

<%def name="help()">
  <!--#include file="/help/link_accounts"-->
</%def>