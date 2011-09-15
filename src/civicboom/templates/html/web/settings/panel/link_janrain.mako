<%inherit file="/html/web/common/frag_container.mako"/>

<%namespace name="frag" file="/frag/common/frag.mako"/>
<%namespace name="link_janrain" file="/frag/settings/panel/link_janrain.mako" import="body,title"/>
<%namespace name="settings_menu" file="/frag/settings/menu.mako" import="body"/>

<%def name="title()">Settings</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <%
        self.attr.frags = [menu, janrain]
        self.attr.frag_col_sizes = [1,2]
    %>
</%def>

<%def name="menu()">
  ${frag.frag_basic(title=_('Settings menu'), icon='group', frag_content=settings_menu.body)}
</%def>

<%def name="janrain()">
  ${frag.frag_basic(title=link_janrain.title, icon='group', frag_content=link_janrain.body)}
</%def>

<%def name="help()">
  <!--#include virtual="/help/link_accounts"-->
</%def>
