<%inherit file="/html/mobile/common/mobile_base.mako"/>

## includes
<%namespace name="member_includes" file="/html/mobile/common/member.mako" />
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
        
        ${member_details_full(self.member)}
    </div>
    
    ## Extra info (content/boomed/etc)
    <div data-role="page" data-title="${page_title()}" data-theme="b" id="member-extra-${self.id}" class="member_extra_page">
        <div data-role="header" data-position="inline">
            <a href="#member-details-${self.id}" data-role="button" data-icon="arrow-l" data-direction="reverse">Back</a>
            <h1>${self.name} - extra</h1>
        </div>
        
        ${member_content_list(d)}
    </div>
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
            <ul data-role="listview">
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
            website = member['website']
        %>
        <div class="member_details">
            <ul data-role="listview">
                ## Avatar/name
                <li>
                    ${member_includes.avatar(member, as_link=0, img_class="thumbnail")}
                    <h3>${member['name']}</h3>
                    <p>Username: <b>${member['username']}</b></p>
                    <p>Type: <b>${member['type'].capitalize()}</b></p>
                </li>
                
                ## User website
                % if member['website']:
                    <li data-role="list-divider" role="heading">
                        User's website
                    </li>
                    <li>
                        <a href="${website}" alt="${member['id']}'s website">
                            ${website}
                        </a>
                    </li>
                % endif
                
                ## User description
                <li data-role="list-divider" role="heading">
                    User's description
                </li>
                <li>
                    ${member['description']}
                </li>
                
                ## User description
                <li data-role="list-divider" role="heading">
                    Following
                    <span class="ui-li-count">${d['following']['count']}</span>
                </li>
                <li class="ui-li ui-li-static ui-body-c">
                    ${member_includes.member_thumbnail_list(d['following'])}
                </li>
                
                ## User description
                <li data-role="list-divider" role="heading">
                    Followers
                    <span class="ui-li-count">${d['followers']['count']}</span>
                </li>
                <li class="ui-li ui-li-static ui-body-c">
                    ${member_includes.member_thumbnail_list(d['followers'])}
                </li>
            </ul>
        </div>
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
            <ul data-role="listview">
                ${list_contents(requests, "Active requests")}
                ${list_contents(responses, "Responses")}
                ${list_contents(articles, "Stories")}
            </ul>
        </div>
    % endif
</%def>

## Create li elements for each item in the given list
<%def name="list_contents(content, title)">
    % if content:
        <%
            items = content['items']
            count = content['count']
        %>
        
        % if items and count:
            <li data-role="list-divider" role="heading">
                ${title}
                <span class="ui-li-count">${count}</span>
            </li>
            
            % for item in items:
                <li>
                    <a href="${h.url(controller='contents', action='show', id=item['id'], title=h.make_username(item['title']))}">
                        <img src="${item['thumbnail_url']}" class="thumbnail" />
                        <h3>${item['title']}</h3>
                        <p>${item['content_short']}</p>
                    </a>
                </li>
            % endfor
        % endif
    % endif
</%def>