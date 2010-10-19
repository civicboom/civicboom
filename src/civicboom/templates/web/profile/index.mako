<%inherit file="/web/common/html_base.mako"/>

<%namespace name="public_profile"   file="/web/members/show.mako"        />
<%namespace name="loc"              file="/web/common/location.mako"     />
<%namespace name="member_includes"  file="/web/common/member.mako"       />
<%namespace name="content_includes" file="/web/common/content_list.mako" />


##------------------------------------------------------------------------------
## Left Col
##------------------------------------------------------------------------------


<%def name="col_left()">

    ${public_profile.col_left()}

	<h2>${_("Tools")}</h2>
	    <a href="${url(controller='profile', action='index')}">${_("My Profile")}</a>
	<br><a href="${url('settings')}">${_("Edit Settings")}</a>
	<br><a href="${url(controller='settings', action='messages')}">${_("Edit Notifications")}</a>
	<br><a href="${url('messages')}">${_("My Messages")}</a>
    <br><a href="${url(controller='account', action='link_janrain')}">${_("Manage Login Accounts")}</a>

</%def>



##------------------------------------------------------------------------------
## Right Col
##------------------------------------------------------------------------------

<%def name="col_right()">
	<h2>${_("Notifications")}</h2>
	% if 'notifications' in d['messages'] and len(d['messages']['notifications']) > 0:
		% for message in d['messages']['notifications']:
			<div class="notification">
				${h.secure_link(url('message', id=message['id'], format='redirect'), "X", [("_method", "DELETE"), ])}
				${message['subject']|n}
			</div>
		% endfor
	% else:
		<span class="message_empty">${_("No notifications")}</span>
	% endif

	<h2>${_("Recent Messages")}</h2>
	% if 'to' in d['messages'] and len(d['messages']['to']) > 0:
		% for message in d['messages']['to']:
			<div class="message_short">
				<a class="subject" href="${url('message', id=message['id'])}">${message['subject']}</a>
				<span class="source">${str(message['source'])}</span>
			</div>
		% endfor
		<a class="read_more" href="${url('messages')}">${_("View All Messages")} &rarr;</a>
	% else:
		<span class="message_empty">${_("No messages")}</span>
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
		<span class="message_empty">${_("No location specified")}</span>
	% endif
	<a class="read_more" href="${url(controller='settings', action='location')}">${_("Set Location")} &rarr;</a>
</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    ## reminder that new relationships have been setup as -
    ##   content_assignments_active and content_assignments_previous
    ${public_profile.content_list(d['content'], type_filters=["draft", "article", "assignment", "syndicate"], show_actions=True)}
    ${public_profile.content_list_group(d['member']['assignments_accepted'], "assignments accepted")}
</%def>
