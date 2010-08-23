<%inherit file="/web/layout_3cols.mako"/>
<%namespace name="loc"             file="/web/design09/includes/location.mako"/>
<%namespace name="member_includes" file="/web/design09/includes/member.mako"  />
<%namespace name="sl"              file="/web/design09/includes/secure_link.mako"  />


##------------------------------------------------------------------------------
## Left Col
##------------------------------------------------------------------------------

<%def name="col_left()">
	<style>
	.avatar     {width: 100%; text-align: center;}
	.avatar IMG {border: 1px solid gray;}
	.message_empty {color: #AAA; display: block; width: 100%; text-align: center;}
	.read_more {                 display: block; width: 100%; text-align: right; }
	.notification {border-bottom: 1px solid gray; margin-bottom: 4px; padding-bottom: 4px;}
	.notification FORM {float: right;}
	</style>

	<div class="avatar">
		##<img src="${c.viewing_user.avatar_url}">
		##<br>${c.viewing_user.name}
		##<br>(${c.viewing_user.username})
        ${member_includes.avatar(c.viewing_user, show_name=True)}
	</div>

	<h2>${_("Following")}</h2>
	% if c.viewing_user.following:
        ${member_includes.member_list(c.viewing_user.following, show_avatar=True, class_="avatar_thumbnail_list")}
	% else:
		<span class="message_empty">Not following anyone</span>
	% endif

	<h2>${_("Followers")}</h2>
	% if c.viewing_user.followers:
		${member_includes.member_list(c.viewing_user.followers, show_avatar=True, class_="avatar_thumbnail_list")}
	% else:
		<span class="message_empty">No followers</span>
	% endif

	<h2>${_("Tools")}</h2>
	    <a href="${url(controller='profile', action='index')}">My Profile</a>
	<br><a href="${url(controller='settings', action='general')}">Edit Settings</a>
	<br><a href="${url(controller='settings', action='messages')}">Edit Notifications</a>
	<br><a href="${url(controller='messages', action='index')}">My Messages</a>
</%def>


##------------------------------------------------------------------------------
## Right Col
##------------------------------------------------------------------------------
<%def name="col_right()">
	<h2>${_("Notifications")}</h2>
	% if c.viewing_user.messages_notification:
		% for msg in c.viewing_user.messages_notification:
			<div class="notification">
				${sl.secure_link(url.current(controller='messages', action='delete'), "X", [("msg_id", msg.id), ("type", "notification")])}
				${msg.subject|n}
			</div>
		% endfor
	% else:
		<span class="message_empty">No notifications</span>
	% endif

	<h2>${_("Recent Messages")}</h2>
	% if c.viewing_user.messages_to[0:5]:
		% for msg in c.viewing_user.messages_to[0:5]:
			<div class="message_short">
				<a class="subject" href="${url(controller='messages', action='read', id=msg.id)}">${msg.subject}</a>
				<span class="source">${str(msg.source)}</span>
			</div>
		% endfor
		<a class="read_more" href="${url(controller='messages', action='index')}">View All Messages &rarr;</a>
	% else:
		<span class="message_empty">No messages</span>
	% endif

	<h2>${_("Where I Am Now")}</h2>
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
	<h2>${_("Articles I'm Working On")}</h2>

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
