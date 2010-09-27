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
