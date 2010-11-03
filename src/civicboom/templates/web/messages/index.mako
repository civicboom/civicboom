<%inherit file="/web/common/html_base.mako"/>

<%def name="col_left()">
	<div class="avatar">
		<img class="avatar" src="${c.logged_in_persona.avatar_url}">
		<br>${c.logged_in_persona.name}
		<br>(${c.logged_in_persona.username})
	</div>

	<h2>${_("Tools")}</h2>
	    <a href="${url(controller='profile', action='index')}">${_("My Profile")}</a>
	<br><a href="${url(controller='settings', action='general')}">${_("Edit Settings")}</a>
	<br><a href="${url(controller='settings', action='messages')}">${_("Edit Notifications")}</a>
	<br><a href="${url('messages')}">${_("My Messages")}</a>
</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">

    <% frag_url_messages = url('messages', format='frag') %>
    ${h.frag_div( "messages", frag_url_messages)}
    ${h.frag_link("messages", frag_url_messages, "refresh messages")}

</%def>
