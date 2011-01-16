<%inherit file="/web/common/frag_container.mako"/>

<%def name="title()">${_("Messages")}</%def>

<%def name="body()">
	<% self.attr.frags = settings %>
</%def>

<%def name="settings()">
	<%include file="/frag/settings/messages.mako"/>
</%def>



