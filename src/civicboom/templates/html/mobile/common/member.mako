##------------------------------------------------------------------------------
## Member Avatar - display a member as text/image + link to profile
##------------------------------------------------------------------------------
<%def name="avatar(member, class_='', js_link_to_frag=True, new_window=False, img_class='', as_link=True, **kwargs)">
    % if member:
        <%
            if hasattr(member,'to_dict'):
                member = member.to_dict()
        %>
        <img src="${member['avatar_url']}" alt="${member['username']}'s avatar" onerror='this.onerror=null;this.src="/images/default/avatar.png"'/>
    % endif
</%def>

<%def name="member_details(member)">
    <% creator = d['content']['creator'] %>
    <div class="member_details">
        <ul data-role="listview">
            <li>
                <a href="${h.url('member', id=member['username'])}" title="${member['name']}" rel="external">
                    ${avatar(member)}
                    <h3>By ${creator['name']}</h3>
                    <p>Username: <b>${creator['username']}</b></p>
                    <p>Type: <b>${creator['type'].capitalize()}</b></p>
                </a>
            </li>
        </ul>
    </div>
</%def>