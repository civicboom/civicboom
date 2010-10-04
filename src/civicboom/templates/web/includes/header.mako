% if c.logged_in_user:
<div id="logout">
	${h.secure_link(url(controller='account', action='signout'), h.literal('<img src="/styles/web/login.png" alt="${_("Log out")}">'))}
</div>
% else:
<div id="login">
	<a href="${url(controller='account', action='signin')}"><img src="/styles/web/login.png" alt="${_("Log in")}"></a>
</div>
% endif

<div id="search">
	<form action="${h.url(controller='search', action='content')}" method='GET'>
		<input type="search" class="search_input" name="query" placeholder="${_("Search")}" />
		<input type="image" class="search_button" src="/styles/web/go.png" alt="Search">
	</form>
</div>

<h1 id="logo">
	<a href='/'>
		<img src='/styles/web/logo.png' alt='${_("_site_name")}'/>
		<span>${_("_site_name")}</span>
	</a>
</h1>
