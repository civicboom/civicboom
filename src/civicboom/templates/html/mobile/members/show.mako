<%inherit file="/html/mobile/common/mobile_base.mako"/>

##-----------------------------------------------------------------------------
## includes
##-----------------------------------------------------------------------------
<%namespace name="components"      file="/html/mobile/common/components.mako" />
<%namespace name="member_includes" file="/html/mobile/common/member.mako" />
<%namespace name="list_includes"   file="/html/mobile/common/lists.mako" />
<%namespace name="frag_list"       file="/frag/common/frag_lists.mako" />

<%def name="body()">
    <%
        self.member    = d['member']
        self.id        = self.member['username']
        self.name      = self.member.get('name')
    %>
    
    ## Main member detail page (username/description/etc)
    <div data-role="page" data-title="${page_title()}" data-theme="b" id="member-details-${self.id}" class="member_details_page">
        ${components.header(title=self.name, next_link="#member-extra-"+self.id)}
        
        <div data-role="content">
            ${member_details_full(self.member)}
        </div>
        
        ${signout_navbar()}
    </div>
    
    ## Extra info (content/boomed/etc)
    <div data-role="page" data-title="${page_title()}" data-theme="b" id="member-extra-${self.id}" class="member_extra_page">
        ${components.header(title=self.name, back_link="#member-details-"+self.id)}
        
        <div data-role="content">
            ${member_content_list(d)}
        </div>
    </div>
</%def>

<%def name="page_title()">
    ${_(self.name)}
</%def>

##-----------------------------------------------------------------------------
## Signout nav bar link
##-----------------------------------------------------------------------------
<%def name="signout_navbar()">
    % if c.logged_in_user and c.logged_in_user.username == self.id:
        <div data-role="footer" data-position="inline" data-id="page_footer" data-theme="a">
            <div data-role="navbar" class="ui-navbar">
                <ul>
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
## Short member details - Username, real name and user type + avatar
##-----------------------------------------------------------------------------
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

##-----------------------------------------------------------------------------
## Full user details for member/profile pages
## Includes username/etc, description, followers/etc
##-----------------------------------------------------------------------------
<%def name="member_details_full(member)">
    % if member:
        <%
            if hasattr(member,'to_dict'):
                member = member.to_dict()
            username = member['username']
            description = member['description']
            website = member['website']
        %>
        <div class="member_details">
            ## Avatar/name
            ${member_includes.avatar(member, as_link=0, img_class="avatar")}
            <h3>${member['name']}</h3>
            <p>Username: <b>${username}</b></p>
            <p>Type: <b>${member['type'].capitalize()}</b></p>
            
            <div class="messages ui-grid-b" data-theme="b">
                <div class="ui-block-a">
                    <a href="${h.url('messages', list='to', format='html' )}" rel="external">Messages</a>
                </div>
                <div class="ui-block-b">
                    <a href="${h.url('messages', list='sent', format='html' )}" rel="external">Sent</a>
                </div>
                <div class="ui-block-c">
                    <a href="${h.url('messages', list='notification', format='html' )}" rel="external">Notifications</a>
                </div>
            </div>
            
            <ul data-role="listview" data-inset="true">
                ## User website
                % if website:
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
                % if description:
                    <li data-role="list-divider" role="heading">
                        ${username}'s description
                    </li>
                    <li>
                        ${description}
                    </li>
                % endif
            </ul>
                
            ${member_list("following")}
            ${member_list("followers")}
            ${member_list("members")}
        </div>
    % endif
</%def>

##-----------------------------------------------------------------------------
## 
##-----------------------------------------------------------------------------
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

##-----------------------------------------------------------------------------
## List the content relating to this user
## Includes assignments, articles, responses, etc
##-----------------------------------------------------------------------------
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
                <li>
                    ${h.secure_link(
                        h.url(controller='account', action='signout'),
                        _('Sign out')
                    )}
                </li>
            </ul>
        </div>
    % endif
</%def>