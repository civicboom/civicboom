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
        <img src="${member['avatar_url']}" alt="${member['username']}'s avatar" class="${img_class}" onerror='this.onerror=null;this.src="/images/default/avatar.png"'/>
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