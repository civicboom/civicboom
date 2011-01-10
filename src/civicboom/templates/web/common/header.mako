##------------------------------------------------------------------------------
## Persona Switching
##------------------------------------------------------------------------------
% if c.logged_in_persona:
<div id="persona_select" class="menuh">
    <ul><li>
        <a class="name" href="${url(controller='profile', action='index')}">
            <img src="${c.logged_in_persona.avatar_url}" alt="${c.logged_in_persona.name}" onerror='this.onerror=null;this.src="/images/default_avatar.png"'/>
            <span class="role">${c.logged_in_persona_role}</span>
        </a>
        <ul>
            <li>
                <img src="${c.logged_in_user.avatar_url}"/>
                ${h.secure_link(url(controller='account', action='set_persona', id=c.logged_in_user.username, format='redirect'), "%s" % (c.logged_in_user.username))}
            </li>
            % for membership in [membership for membership in c.logged_in_user.groups_roles if membership.status=="active"]:
            <li>
                <img src="${membership.group.avatar_url}" alt="${membership.group.name}" onerror='this.onerror=null;this.src="/images/default_avatar.png"'/>
                ${h.secure_link(url(controller='account', action='set_persona', id=membership.group.username, format='redirect'), "%s:%s" % (membership.group.name, membership.role))}
            </li>
            % endfor
        </ul>
    </li><ul>
</div>


% endif

##------------------------------------------------------------------------------
## Logo
##------------------------------------------------------------------------------
<h1 id="logo">
	<a href='/'>
		<img src='/styles/web/logo.png' alt='${_("_site_name")}' height="32" width="128" />
		<span>${_("_site_name")}</span>
	</a>
</h1>



##------------------------------------------------------------------------------
## Menu
##------------------------------------------------------------------------------
<nav class="menuh-container">
    % if c.logged_in_persona:
    <a id="home_link" href="${url(controller='profile', action='index')}">
    % else:
    <a id="home_link" href="/">
    % endif
        <img src="/styles/common/icons32/home-icon.png" alt="${_('Home')}" width="32" height="24" />
    </a>
    
<div class="menuh">
    <ul>
        <li><a href="#" class="top_parent button">${_("Create")}</a>
        <ul>
            <li>${h.secure_link(h.url('new_content', target_type='assignment'), _("_assignment").capitalize(), css_class="sub_option")}</li>
            <li>${h.secure_link(h.url('new_content', target_type='article'   ), _("_article").capitalize()   , css_class="sub_option")}</li>
            <li><a href="${h.url('new_group')}" class="sub_option">${_("Group")}</a></li>
        </ul>
        </li>
    </ul>

    <ul>
        <li><a href="#" class="top_parent button">${_("Explore")}</a>
        <ul>
            <!--<li><form action="${h.url('contents')}" method='GET'><input type="search" name="query" placeholder="${_("Quick Search")}"></form></li>-->
% if c.logged_in_persona:
<!--
            <li><a href="/feeds" class="parent">${_("News Feeds")}</a>
				<ul>
					% for f in c.logged_in_persona.feeds:
					<li><a href="/feeds/${f.id}" class="sub_option">${f.name}</a></li>
					% endfor
					<li><a href="/feeds/new" class="sub_option">${_("Create New Feed")}</a></li>
				</ul>
			</li>
-->
% endif
            <li><a href="/contents?list=assignments_active" class="sub_option">${_("_Assignments")}</a></li>
            <li><a href="/contents?list=articles" class="sub_option">${_("_Articles")}</a></li>
            <li><a href="/members?list=users" class="sub_option">${_("People")}</a></li>
            <li><a href="/members?list=groups" class="sub_option">${_("Groups")}</a></li>
        </ul>
        </li>
    </ul>

    <ul>
        <li><a href="#" class="top_parent button">${_("Manage")}</a>
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
</nav>

##------------------------------------------------------------------------------
## Search
##------------------------------------------------------------------------------
<div id="search">
	<form action="${h.url('contents')}" method='GET'>
		<input type="search" class="search_input" name="query" placeholder=" ${_("Search")}" />
		<input type="submit" class="button" value="GO">
	</form>
</div>


##------------------------------------------------------------------------------
## Logout
##------------------------------------------------------------------------------
<div id="login">
% if c.logged_in_persona:
    ${h.secure_link(
        url(controller='account', action='signout'),
        _('Log out'),
        css_class="logout"
    )}
% else:
    <a class="login" href="${url(controller='account', action='signin')}">
        ##<img src="/styles/web/login.png" alt="${_("Log in")}" width="68" height="17">
        ${_('Log in')}
    </a>
% endif
</div>
