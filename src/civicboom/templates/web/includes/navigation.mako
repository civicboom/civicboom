<a class="settings" href="${url('settings')}"><span>${_("settings")}</span></a>

<a class="name" href="${url(controller='profile', action='view', id=c.logged_in_user.username)}">${c.logged_in_user.name}</a>
<a class="clock">[Clock]</a>
<a class="role">[Role]</a>

<a class="profile" href="${url(controller='profile', action='index')}">${_("profile")}</a>
<a class="groups"  href="${url(controller='profile', action='index')}">${_("groups")}</a>
<a class="assignments"  href="${url(controller='profile', action='index')}">${_("assignments")}</a>

<a class="messages" href="${url('messages')}">${_("messages")}</a>
