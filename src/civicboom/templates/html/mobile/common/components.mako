##-----------------------------------------------------------------------------
## Creates the control bar/footer
##-----------------------------------------------------------------------------
<%def name="control_bar()">
    % if c.logged_in_user:
        <div data-role="footer" data-position="fixed" data-theme="b">
            <div data-role="navbar" class="ui-navbar">
                <ul>
                    <li>
                        <a href="${h.url(controller='profile', action='index')}" rel="external">My profile</a>
                    </li>
                    <li>
                        <a href="${h.url(controller='contents', action='index')}" rel="external">Explore</a>
                    </li>
                    <li>
                        ${h.secure_link(
                            h.url(controller='account', action='signout'),
                            _('Sign out')
                        )}
                    </li>
                </ul>
            </div>
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
                    <option value="${_("_Members")}">${_("_Members")}</option>
                </select>
                <input type="submit" value="${_("Search")}">
            </form>
        </p>
    </div>
</%def>