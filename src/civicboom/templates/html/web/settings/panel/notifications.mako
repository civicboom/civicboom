<%inherit file="/html/web/common/frag_container.mako"/>

<%namespace name="frag" file="/frag/common/frag.mako"/>
<%namespace name="message_settings" file="/frag/settings/panel/notifications.mako" import="body"/>
<%namespace name="settings_menu" file="/frag/settings/menu.mako" import="body"/>

<%def name="title()">General Settings</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <%
        self.attr.frags = [menu, messages]
        self.attr.frag_col_sizes = [1,2]
    %>
</%def>

<%def name="menu()">
  ${frag.frag_basic(title=_('Settings menu'), icon='group', frag_content=settings_menu.body)}
</%def>

<%def name="messages()">
  ${frag.frag_basic(title=_('Notification Settings'), icon='group', frag_content=message_settings.body)}
</%def>

<%def name="help()">
  <!--#include file="/help/settings_panel_messages"-->
</%def>
