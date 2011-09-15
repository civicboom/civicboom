<%inherit file="/html/web/common/frag_container.mako"/>

<%namespace name="frag" file="/frag/common/frag.mako"/>
<%namespace name="group_settings" file="/frag/settings/panel/general_group.mako" import="body"/>
<%namespace name="settings_menu" file="/frag/settings/menu.mako" import="body"/>

<%def name="title()">Group Settings</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <%
        self.attr.frags = [menu, general_group]
        self.attr.frag_col_sizes = [1,2]
    %>
</%def>

<%def name="menu()">
  ${frag.frag_basic(title=_('Settings menu'), icon='group', frag_content=settings_menu.body)}
</%def>

<%def name="general_group()">
	${frag.frag_basic(title=_('_Group Settings'), icon='group', frag_content=group_settings.body)}
</%def>


<%def name="help()">
  <!--#include virtual="/help/settings"-->
</%def>
