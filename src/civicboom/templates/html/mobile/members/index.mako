<%inherit file="/html/mobile/common/lists.mako"/>

<%namespace name="member_includes" file="/html/mobile/common/member.mako" />


<%def name="title()"       >${_("Explore _users and _groups")}</%def>

<%def name="page_id()"     >explore_member</%def>
<%def name="page_content()">
    ${parent.generate_list(d['list'], member_li, title=_('Members'), more=None)}
</%def>

##------------------------------------------------------------------------------
## 
##------------------------------------------------------------------------------

<%def name="list_members_avatars(members, title=None)">
    <%
        title = title if title else _('Members')
        if isinstance(members, dict):
            count   = members['count']
            members = members['items']
        else:
            count   = len(members)
    %>
    % if members:
        ## AllanC - TODO - Can this be unified with generate_list?
        <ul data-role="listview" data-inset="true">
            <li data-role="list-divider" role="heading">
                ## AllanC - TODO - member avatar lists need to open up full members_index page of followers etc
                ${title.capitalize()}
                <span class="ui-li-count">${count}</span>
            </li>
            <li class="ui-li ui-li-static ui-body-c">
                % for member in members:
                    <span class="member_avatar_small">${member_includes.avatar(member, img_class="thumbnail_small")}</span>
                % endfor
            </li>
        </ul>
    % endif
</%def>

##------------------------------------------------------------------------------
## Generate a single li element for the given member
##------------------------------------------------------------------------------
<%def name="member_li(item)">
    <li>
        <a href="${h.url('member', id=item['username'])}" title="${item['name']}" rel="external">
            <img src="${item['avatar_url']}" class="thumbnail" />
            <h3>
                ${item['name']}
                % if item.get('type') == "group":
                    <small><b> [${_("_Group")}]</b></small>
                % endif
            </h3>
            % if item.get('username'):
                <p>${item['username']}</p>
            % endif
            % if item.get('num_followers') != None:
                <p><b>${item['num_followers']}</b> followers</p>
            % endif
        </a>
    </li>
</%def>


