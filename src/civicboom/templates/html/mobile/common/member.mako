##------------------------------------------------------------------------------
## Member Avatar - display a member as text/image + link to profile
##------------------------------------------------------------------------------
<%def name="avatar(member, class_='', js_link_to_frag=True, new_window=False, img_class='', as_link=True, **kwargs)">
    % if member:
        <%
            if hasattr(member,'to_dict'):
                member = member.to_dict()
        %>
        % if as_link:
            <a href="${h.url('member', id=member['username'])}" title="${member['name']}" rel="external">
        % endif
            <img src="${member['avatar_url']}" alt="${member['username']}'s avatar" class="${img_class}" onerror='this.onerror=null;this.src="/images/default/avatar_user.png"'/>
        % if as_link:
        </a>
        % endif
    % endif
</%def>

##------------------------------------------------------------------------------
## List member thumbnails
##------------------------------------------------------------------------------
<%def name="member_thumbnail_list(member_list)">
    % for member in member_list['items']:
        ${avatar(member, img_class="thumbnail_small")}
    % endfor
</%def>

##------------------------------------------------------------------------------
## Short member details - Username, real name and user type + avatar
##------------------------------------------------------------------------------
<%def name="member_details_short(member, as_link=True, li_only=False)">
    % if member:
        <%
            if hasattr(member,'to_dict'):
                member = member.to_dict()
        %>
        % if not li_only:
        <div class="member_details">
            <ul data-role="listview">
        % endif
                <li>
                    % if as_link:
                    <a href="${h.url('member', id=member['username'])}" title="${member['name']}" rel="external">
                    % endif
                        ${avatar(member, as_link=0, img_class="thumbnail")}
                        <h3>${member['name']}</h3>
                        <p>Username: <b>${member['username']}</b></p>
                        <p>Type: <b>${member['type'].capitalize()}</b></p>
                    % if as_link:
                    </a>
                    % endif
                </li>
        % if not li_only:
            </ul>
        </div>
        % endif
    % endif
</%def>
