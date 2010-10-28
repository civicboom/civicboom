<div id="search">
	<form action="${h.url(controller='search', action='content')}" method='GET'>
		<input type="search" class="search_input" name="query" placeholder="${_("Search")}" />
		<input type="image" class="search_button" src="/styles/web/go.png" alt="${_("Search")}">
	</form>
</div>

<div id="menuh-container">
<div id="menuh">
    <ul>
        <li><a href="#" class="top_parent">Create</a>
        <ul>
            <li><a href="/contents/new?target_type=assignment" class="sub_option">Assignment</a></li>
            <li><a href="/contents/new?target_type=article" class="sub_option">Article</a></li>
            <li><a href="/groups/new" class="sub_option">Group</a></li>
        </ul>
        </li>
    </ul>

    <ul>
        <li><a href="#" class="top_parent">Explore</a>
        <ul>
            <li><input type="text" placeholder="Quick Search"></li>
            <li><a href="/search" class="sub_option">Advanced Search</a></li>
% if c.logged_in_persona:
            <li><a href="/feeds" class="parent">News Feeds</a>
				<ul>
					% for f in c.logged_in_persona.feeds:
					<li><a href="/feeds/${f.id}" class="sub_option">${f.name}</a></li>
					% endfor
					<li><a href="/feeds/new" class="sub_option">Create New Feed</a></li>
				</ul>
			</li>
% endif
            <li><a href="/groups" class="sub_option">Find Groups</a></li>
        </ul>
        </li>
    </ul>

    <ul>
        <li><a href="#" class="top_parent">Manage</a>
        <ul>
            <li><a href="/profile" class="sub_option">My Profile</a></li>
            <li><a href="/profile" class="sub_option">My Content</a></li>
            <li><a href="/profile" class="sub_option">My Groups</a></li>
        </ul>
        </li>
    </ul>

</div>
</div>

<h1 id="logo">
	<a href='/'>
		<img src='/styles/web/logo.png' alt='${_("_site_name")}'/>
		<span>${_("_site_name")}</span>
	</a>
</h1>
