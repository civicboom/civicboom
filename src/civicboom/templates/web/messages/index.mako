<%inherit file="/web/common/html_base.mako"/>

<%def name="col_left()">
	<div class="avatar">
		<img class="avatar" src="${c.viewing_user.avatar_url}">
		<br>${c.viewing_user.name}
		<br>(${c.viewing_user.username})
	</div>

	<h2>Tools</h2>
	    <a href="${url(controller='profile', action='index')}">My Profile</a>
	<br><a href="${url(controller='settings', action='general')}">Edit Settings</a>
	<br><a href="${url(controller='settings', action='messages')}">Edit Notifications</a>
	<br><a href="${url('messages')}">My Messages</a>
</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">

    <% frag_url_messages = url('messages', format='frag') %>
    ${h.frag_div( "messages", frag_url_messages)}
    ${h.frag_link("messages", frag_url_messages, "refresh messages")}

</%def>
