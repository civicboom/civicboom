##-----------------------------------------------------------------------------
## Title logo image
##-----------------------------------------------------------------------------
<%def name="title_logo()">
    <div class="title_logo">
        <a href="${h.url(controller='misc', action='titlepage')}" rel='external'>
            <img class='logo_img' src='${h.wh_url("public", "images/logo-v3-684x150.png")}' alt='${_("_site_name")}' />
        </a>
    </div>
</%def>

##-----------------------------------------------------------------------------
## Creates the control bar/footer
##-----------------------------------------------------------------------------
<%def name="control_bar()">
    % if c.logged_in_user:
        <div data-role="navbar" class="ui-navbar">
            <ul>
                <li>
                    <a href="${h.url(controller='profile', action='index')}" rel="external">Profile</a>
                </li>
                <li>
                    <a href="${h.url(controller='contents', action='index')}" rel="external">Explore</a>
                </li>
            </ul>
        </div>
    % endif
</%def>

##-----------------------------------------------------------------------------
## Standard search for for content and member index pages
##-----------------------------------------------------------------------------
<%def name="search_form()">
    <div data-role="collapsible" data-collapsed="true" class="search_form">
        <h3>Search</h3>
        <p>
            <form action="${url(controller='misc', action='search_redirector')}" data-ajax="false">
                <input type="search" name="term" placeholder="${_("Find _assignments, _articles and _members")}">
                <select name="type">
                    <option value="All">All content</option>
                    <option value="${_("_Assignments")}">${_("_Assignments")}</option>
                    <option value="${_("_Articles")}">${_("_Articles")}</option>
                    <option value="${_("_Members")}">${_("_Users / _Groups")}</option>
                </select>
                <input type="submit" value="${_("Search")}">
            </form>
        </p>
    </div>
</%def>

##-----------------------------------------------------------------------------
## Render header bar incl. control panel + extra links
##-----------------------------------------------------------------------------
<%def name="header(title=None, back_link=None, next_link=None, control_override=None)">
    <div data-role="header" data-position="inline" data-id="page_header" data-theme="b">
        <div class="header">
            % if back_link:
                <a href="${back_link}" class="back_link" data-direction="reverse">
                    <span><</span>
                </a>
            % endif
            <a href="/" rel="external">
                <img class='logo_img' src='${h.wh_url("public", "images/logo-v3-128x28.png")}' alt='${_("_site_name")}' />
            </a>
            % if next_link:
                <a href="${next_link}" class="next_link">
                    <span>></span>
                </a>
            % endif
            <div class="separator"></div>
        </div>
        ${control_override() if control_override else control_bar()}
    </div>
</%def>