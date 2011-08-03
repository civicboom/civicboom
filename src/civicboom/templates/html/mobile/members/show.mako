<%inherit file="/html/mobile/common/mobile_base.mako"/>

## includes
<%namespace name="member_includes" file="/html/mobile/common/member.mako" />
<%namespace name="list_includes"   file="/html/mobile/common/lists.mako" />
<%namespace name="frag_list"       file="/frag/common/frag_lists.mako" />

## page structure defs
<%def name="body()">
    <%
        self.member    = d['member']
        self.id        = self.member['username']
        self.name      = self.member.get('name')
    %>
    
    ## Main member detail page (username/description/etc)
    <div data-role="page" data-title="${page_title()}" data-theme="b" id="member-details-${self.id}" class="member_details_page">
        <div data-role="header" data-position="inline">
            <h1>${self.name}</h1>
            <a href="#member-extra-${self.id}" alt="more" class="ui-btn-right" data-role="button" data-icon="arrow-r" data-iconpos="right">More</a>
        </div>
        
        <div data-role="content">
            ${member_details_full(self.member)}
        </div>
        
        ${control_bar()}
    </div>
    
    ## Extra info (content/boomed/etc)
    <div data-role="page" data-title="${page_title()}" data-theme="b" id="member-extra-${self.id}" class="member_extra_page">
        <div data-role="header" data-position="inline">
            <a href="#member-details-${self.id}" data-role="button" data-icon="arrow-l" data-direction="reverse">Back</a>
            <h1>${self.name} - extra</h1>
        </div>
        
        <div data-role="content">
            ${member_content_list(d)}
        </div>
    </div>
</%def>

<%def name="control_bar()">
    % if c.logged_in_user:
        <div data-role="footer" data-position="fixed">
            <div data-role="navbar" class="ui-navbar">
                <ul>
                    <li>
                        <a href="${h.url(controller='profile', action='index')}" rel="external">My profile</a>
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

<%def name="page_title()">
    ${_("_site_name Mobile - " + self.name)}
</%def>

## Short member details - Username, real name and user type + avatar
<%def name="member_details_short(member, as_link=True)">
    % if member:
        <%
            if hasattr(member,'to_dict'):
                member = member.to_dict()
        %>
        <div class="member_details">
            <ul data-role="listview" data-inset="true">
                <li>
                    % if as_link:
                    <a href="${h.url('member', id=member['username'])}" title="${member['name']}" rel="external">
                    % endif
                        ${member_includes.avatar(member, as_link=0, img_class="thumbnail")}
                        <h3>${member['name']}</h3>
                        <p>Username: <b>${member['username']}</b></p>
                        <p>Type: <b>${member['type'].capitalize()}</b></p>
                    % if as_link:
                    </a>
                    % endif
                </li>
            </ul>
        </div>
    % endif
</%def>

## Full user details for member/profile pages
## Includes username/etc, description, followers/etc
<%def name="member_details_full(member)">
    % if member:
        <%
            if hasattr(member,'to_dict'):
                member = member.to_dict()
            username = member['username']
            website = member['website']
        %>
        <div class="member_details">
            ## Avatar/name
            ${member_includes.avatar(member, as_link=0, img_class="avatar")}
            <h3>${member['name']}</h3>
            <p>Username: <b>${username}</b></p>
            <p>Type: <b>${member['type'].capitalize()}</b></p>
                
            <ul data-role="listview" data-inset="true">
                ## User website
                % if member['website']:
                    <li data-role="list-divider" role="heading">
                        ${username}'s website
                    </li>
                    <li>
                        <a href="${website}" alt="${member['id']}'s website">
                            ${website}
                        </a>
                    </li>
                % endif
                
                ## User description
                <li data-role="list-divider" role="heading">
                    ${username}'s description
                </li>
                <li>
                    ${member['description']}
                </li>
            </ul>
                
                ${member_list("following")}
                ${member_list("followers")}
                ${member_list("members")}
            </ul>
        </div>
    % endif
</%def>

<%def name="member_list(list_title)">
    <% count = d[list_title]['count'] %>
    % if count:
        <ul data-role="listview" data-inset="true">
            <li data-role="list-divider" role="heading">
                ${list_title.capitalize()}
                <span class="ui-li-count">${count}</span>
            </li>
            <li class="ui-li ui-li-static ui-body-c">
                ${member_includes.member_thumbnail_list(d[list_title])}
            </li>
        </ul>
    % endif
</%def>

## List the content relating to this user
## Includes assignments, articles, responses, etc
<%def name="member_content_list(data)">
    % if data:
        <%
            member = data['member']
            if hasattr(member,'to_dict'):
                member = member.to_dict()
            requests = data['assignments_active']
            responses = data['responses']
            articles = data['articles']
        %>
        <div class="member_content">
            ${list_includes.list_contents(requests, "Active requests")}
            ${list_includes.list_contents(responses, "Responses")}
            ${list_includes.list_contents(articles, "Stories")}
        </div>
    % endif
</%def>