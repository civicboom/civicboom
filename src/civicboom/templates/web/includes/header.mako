<h1>
	<a href='/'>
		<img src='/styles/design09/logo_beta_overlay.png' alt='beta' style="position: absolute; max-width: 20px; margin-left: 120px;"/>
		<img src='/styles/design09/logo.png'              alt='${_("_site_name")}'/>
		<span>${_("_site_name")}</span>
	</a>
</h1>

<ul>
% if not c.logged_in_user:
	<li><a href="${url(controller='account', action='signin')}">${_("Sign in or Sign up")}</a></li>
% else:
	<li><a href="${url(controller='profile', action='view', id=c.logged_in_user.username)}">${c.logged_in_user.name} (${c.logged_in_user.username})</a></li>
	<li><a href="${url(controller='profile', action='index')}">${_("Controls")}</a></li>
	<li>${h.secure_link(url(controller='account', action='signout'), _("Sign out"))}</li>
% endif
</ul>

<ul>
	<li>
		${h.secure_link(url('new_content'), _("Create _content"))}
		<div class="tooltip tooltip_icon"><span>${_("Uploading an _article allows you express your ideas, opinions and news to a wider community")}</span></div>
	</li>
	<li>
		<a href="${h.url(controller='search', action='content', type='assignment')}">${_("Find _assignments")}</a>
		<div class="tooltip tooltip_icon"><span>${_("Find open _assignments to respond to")}</span></div>
	</li>
</ul>

<form action="${h.url(controller='search', action='content')}" method='GET'>
	${_("Find")}:
	<input type="search" class="search_input" name="query" placeholder="News, opinions" />
	<input type="submit" class="search_submit" value="" />
</form>
