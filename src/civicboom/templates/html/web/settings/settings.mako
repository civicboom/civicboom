<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="title()">${_("Settings")}</%def>

<%def name="body()">
	<% self.attr.frags = settings %>
</%def>

<%def name="settings()">
	<%include file="/frag/settings/settings.mako"/>
</%def>
