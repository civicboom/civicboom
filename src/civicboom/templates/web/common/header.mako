<div id="search">
	<form action="${h.url('contents')}" method='GET'>
		<input type="search" class="search_input" name="query" placeholder=" ${_("Search")}" />
		<input type="submit" class="button gradient" value="GO">
	</form>
</div>

<div class="menuh-container">
<div class="menuh">
    <ul>
        <li><a href="#" class="top_parent">${_("Create")}</a>
        <ul>
            <li>${h.secure_link(h.url('new_content', target_type='assignment'), _("_assignment").capitalize(), css_class="sub_option")}</li>
            <li>${h.secure_link(h.url('new_content', target_type='article'   ), _("_article").capitalize()   , css_class="sub_option")}</li>
            <li><a href="${h.url('new_group')}" class="sub_option">${_("Group")}</a></li>
        </ul>
        </li>
    </ul>

    <ul>
        <li><a href="#" class="top_parent">${_("Explore")}</a>
        <ul>
            <!--<li><form action="${h.url('contents')}" method='GET'><input type="search" name="query" placeholder="${_("Quick Search")}"></form></li>-->
% if c.logged_in_persona:
            <li><a href="/feeds" class="parent">${_("News Feeds")}</a>
				<ul>
					% for f in c.logged_in_persona.feeds:
					<li><a href="/feeds/${f.id}" class="sub_option">${f.name}</a></li>
					% endfor
					<li><a href="/feeds/new" class="sub_option">${_("Create New Feed")}</a></li>
				</ul>
			</li>
% endif
            <li><a href="/contents?list=assignments_active" class="sub_option">${_("_Assignments")}</a></li>
            <li><a href="/contents?list=articles" class="sub_option">${_("_Articles")}</a></li>
            <li><a href="/members" class="sub_option">${_("People")}</a></li>
            <li><a href="/groups" class="sub_option">${_("Groups")}</a></li>
        </ul>
        </li>
    </ul>

    <ul>
        <li><a href="#" class="top_parent">${_("Manage")}</a>
        <ul>
            <li><a href="/profile" class="sub_option">${_("Profile")}</a></li>
            <li><a href="/settings" class="sub_option">${_("Settings")}</a></li>
            <li><a href="/profile" class="sub_option">${_("Content")}</a></li>
            <li><a href="/profile" class="sub_option">${_("Assignments")}</a></li>
            <li><a href="/profile" class="sub_option">${_("Groups")}</a></li>
        </ul>
        </li>
    </ul>

</div>
</div>

<h1 id="logo">
	<a href='/'>
		<img src='/styles/web/logo.png' alt='${_("_site_name")}' height="32" width="128" />
		<span>${_("_site_name")}</span>
	</a>
</h1>
