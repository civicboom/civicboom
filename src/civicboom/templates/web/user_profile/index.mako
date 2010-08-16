<%inherit file="/web/layout_3cols.mako"/>
<%namespace name="loc" file="/web/design09/includes/location.mako"/>

##------------------------------------------------------------------------------
## Left Col
##------------------------------------------------------------------------------

<%def name="col_left()">
	<style>
	DIV.avatar {width: 100%; text-align: center;}
	IMG.avatar {border: 1px solid gray;}
	.message_empty {color: #AAA; display: block; width: 100%; text-align: center;}
	.read_more {                 display: block; width: 100%; text-align: right; }
	</style>

	<div class="avatar">
		<img class="avatar" src="${c.viewing_user.avatar_url}">
		<br>${c.viewing_user.name}
		<br>(${c.viewing_user.username})
	</div>

	<h2>Following</h2>
	% if c.viewing_user.following:
		% for f in c.viewing_user.following:
			<br>${f.name}
		% endfor
	% else:
		<span class="message_empty">Not following anyone</span>
	% endif

	<h2>Followers</h2>
	% if c.viewing_user.followers:
		% for f in c.viewing_user.followers:
			<br>${f.name}
		% endfor
	% else:
		<span class="message_empty">No followers</span>
	% endif

	<h2>Tools</h2>
	    <a href="${url(controller='user_profile', action='index')}">My Profile</a>
	<br><a href="${url(controller='settings', action='general')}">Edit Settings</a>
	<br><a href="${url(controller='settings', action='messages')}">Edit Notifications</a>
	<br><a href="${url(controller='messages', action='index')}">My Messages</a>
</%def>


##------------------------------------------------------------------------------
## Right Col
##------------------------------------------------------------------------------
<%def name="col_right()">
	<h2>Notifications</h2>
	% if c.viewing_user.messages_notification:
		% for msg in c.viewing_user.messages_notification:
			<div class="notification">
				${msg.subject}
			<form action="${url.current(controller='messages', action='delete')}" method="POST">
				<input type="hidden" name="_authentication_token" value="${h.authentication_token()}">
				<input type="hidden" name="msg_id" value="${msg.id}">
				<input type="hidden" name="type" value="notification">
				<input type="submit" value="X">
			</form>
			</div>
		% endfor
	% else:
		<span class="message_empty">No notifications</span>
	% endif

	<h2>Recent Messages</h2>
	% if c.viewing_user.messages_to[0:5]:
		% for msg in c.viewing_user.messages_to[0:5]:
			<div class="message_short">
				<a class="subject" href="${url(controller='messages', action='read', id=msg.id)}">${msg.subject}</a>
				<span class="source">${str(msg.source)}</span>
			</div>
		% endfor
	% else:
		<span class="message_empty">No messages</span>
	% endif
	<a class="read_more" href="${url(controller='messages', action='index')}">View All Messages &rarr;</a>

	<h2>Where I Am Now</h2>
<%
# we need to pass the session to GeoAlchemy functions
from civicboom.model.meta import Session
%>
	% if c.viewing_user.location:
	<p>${loc.minimap(
		width="100%", height="200px",
		lon=c.viewing_user.location.coords(Session)[0],
		lat=c.viewing_user.location.coords(Session)[1]
	)}
	% else:
		<span class="message_empty">No location specified</span>
	% endif
	<a class="read_more" href="${url(controller='settings', action='location')}">Set Location &rarr;</a>
</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
	<h2>Articles I'm Working On</h2>

	% if c.viewing_user.content:
		% for content in c.viewing_user.content:
			<div class="content_summary">
    			<a href="${h.url(controller='content', action="view", id=content.id)}">${content.title}:${content.__type__}</a>
			</div>
		% endfor
	% else:
		<span class="message_empty">No Drafts</span>
	% endif

</%def>
