<ul class="right">
	<li class="settings"><a href="${url('settings')}"><!--${_("settings")}-->&nbsp;</a></li>
</ul>

<ul>
	<li class="name"><a href="${url(controller='profile', action='view', id=c.logged_in_user.username)}">${c.logged_in_user.name}</a></li>
	<li class="time"><a>[Clock]</a></li>
	<li class="role"><a>[Role]</a></li>
</ul>

<ul>
	<li class=""><a href="${url(controller='profile', action='index')}">${_("profile")}</a></li>
	<li class=""><a href="${url(controller='profile', action='index')}">${_("groups")}</a></li>
	<li class=""><a href="${url(controller='profile', action='index')}">${_("assignments")}</a></li>
</ul>

<ul>
	<li class=""><a href="${url('messages')}">${_("messages")}</a></li>
</ul>
