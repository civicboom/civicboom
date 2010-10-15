<div id="search">
	<form action="${h.url(controller='search', action='content')}" method='GET'>
		<input type="search" class="search_input" name="query" placeholder="${_("Search")}" />
		<input type="image" class="search_button" src="/styles/web/go.png" alt="${_("Search")}">
	</form>
</div>

<h1 id="logo">
	<a href='/'>
		<img src='/styles/web/logo.png' alt='${_("_site_name")}'/>
		<span>${_("_site_name")}</span>
	</a>
</h1>
