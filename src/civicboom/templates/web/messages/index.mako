<%inherit file="/web/common/layout_2cols.mako"/>

<%def name="col_side()">
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
<%
from civicboom.controllers.messages import MessagesController
%>
<div id="message_table">
${h.call_action(MessagesController().index)}
</div>
<script>
function refresh_messages() {
	$("#message_table").load("${url('messages', format='frag')}");
	flash_message('messages updated');
}
</script>
<a href="#" onclick="refresh_messages(); return false;">refresh</a>
</%def>
