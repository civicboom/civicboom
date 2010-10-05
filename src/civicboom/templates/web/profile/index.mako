<%inherit file="/web/common/layout_3cols.mako"/>

<%namespace name="public_profile"   file="view.mako"     />
<%namespace name="loc"              file="/web/design09/includes/location.mako"     />
<%namespace name="member_includes"  file="/web/design09/includes/member.mako"       />
<%namespace name="content_includes" file="/web/design09/includes/content_list.mako" />


##------------------------------------------------------------------------------
## Left Col
##------------------------------------------------------------------------------


<%def name="col_left()">

    ${public_profile.col_left()}

	<h2>${_("Tools")}</h2>
	    <a href="${url(controller='profile', action='index')}">My Profile</a>
	<br><a href="${url('settings')}">Edit Settings</a>
	<br><a href="${url(controller='settings', action='messages')}">Edit Notifications</a>
	<br><a href="${url('messages')}">My Messages</a>
    <br><a href="${url(controller='account', action='link_janrain')}">Manage Login Accounts</a>

</%def>



##------------------------------------------------------------------------------
## Right Col
##------------------------------------------------------------------------------

<%def name="col_right()">
	<h2>${_("Notifications")}</h2>
	% if 'notifications' in d['messages']:
		% for message in d['messages']['notifications']:
			<div class="notification">
				${h.secure_link(url('message', id=message['id']), "X", [("_method", "DELETE"), ])}
				${message['subject']|n}
			</div>
		% endfor
	% else:
		<span class="message_empty">No notifications</span>
	% endif

	<h2>${_("Recent Messages")}</h2>
	% if 'messages_to' in d['messages']:
		% for message in d['messages']['to']:
			<div class="message_short">
				<a class="subject" href="${url('message', id=messgae['id'])}">${message['subject']}</a>
				<span class="source">${str(message['source'])}</span>
			</div>
		% endfor
		<a class="read_more" href="${url('messages')}">View All Messages &rarr;</a>
	% else:
		<span class="message_empty">No messages</span>
	% endif

	<h2>${_("Where I Am Now")}</h2>
<%
# we need to pass the session to GeoAlchemy functions
from civicboom.model.meta import Session
%>
	% if d['member']['location_home']:
    <p>
	${loc.minimap(
		width="100%", height="200px",
		lon=d['member']['location_home'].split[0],
		lat=d['member']['location_home'].split[1]
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



<%doc>
    % for content in c.viewing_user.content:
        <div class="content_summary">
            <a href="${h.url(controller='content', action="view", id=content.id)}">${content.title}:${content.__type__}</a>
        </div>
</%doc>

    ## reminder that new relationships have been setup as -
    ##   content_assignments_active and content_assignments_previous

    ${public_profile.content_list(d['content'], ["draft", "article", "assignment", "syndicate"])}

    
</%def>
