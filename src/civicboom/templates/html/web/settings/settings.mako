<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="title()">${_("Settings")}</%def>

<%def name="body()">
	<%
        self.attr.frags = [settings]
        self.attr.frag_col_sizes = [2]
    %>
</%def>

<%def name="settings()">
	<%include file="/frag/settings/settings.mako"/>
</%def>

<%def name="help()">
##	<!--#include virtual="/help/settings"-->
</%def>