<%namespace name="member_includes" file="/web/design09/includes/member.mako"  />

<%def name="sidebar()">
	<div class="avatar">
        ${member_includes.avatar(c.viewing_user, show_name=True)}
	</div>

	<h2>Tools</h2>
	    <a href="${url(controller='profile', action='')}">My Profile</a>
	<br><a href="${url(controller='settings', action='general')}">Edit Settings</a>
	<br><a href="${url(controller='settings', action='messages')}">Edit Notifications</a>
	<br><a href="${url(controller='settings', action='location')}">Edit Location</a>
	<br><a href="${url(controller='messages', action='index')}">My Messages</a>
</%def>
