##------------------------------------------------------------------------------
## Public Methods - Content and Memeber lists
##------------------------------------------------------------------------------

<%def name="member_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_member, *args, **kwargs)}
</%def>

<%def name="content_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_content, *args, **kwargs)}
</%def>

<%def name="group_members_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_group_members, *args, **kwargs)}
</%def>


##------------------------------------------------------------------------------
## Private Rendering Structure
##------------------------------------------------------------------------------

<%def name="frag_list(items, title, url_more, max=3, show_count=True, render_item_function=None)">
    <% if not isinstance(items, list): items=[items]; show_count=False %>
    <% if max==None: max=-1 %>
    <h2><a href="${url_more}">${title}</a></h2>
    <table>
        % for item in items[0:max]:
        <tr>
            ${render_item_function(item)}
        </tr>
        % endfor
    </table>
    % if max > 0 and len(items) > max:
    <a href="${url_more}">more</a>
    % endif
</%def>


##------------------------------------------------------------------------------
## Member Item
##------------------------------------------------------------------------------

<%def name="render_item_member(member)">
    <td>
        <a href="${h.url('member', id=member['id'])}" onclick="cb_frag($(this), '${h.url('member', id=member['id'], format='frag')}'); return false;">
            ${member['username']}
        </a>
    </td>
</%def>


##------------------------------------------------------------------------------
## Group Members Item
##------------------------------------------------------------------------------

<%def name="render_item_group_members(members)">
</%def>


##------------------------------------------------------------------------------
## Content Item
##------------------------------------------------------------------------------

<%def name="render_item_content(content, location=False)">
    <td class="thumbnail small">
        <div class="clipper">
            ${content_thumbnail_icons(content)}
            <img src="${content['thumbnail_url']}" alt="${content['title']}" class="img"/>
        </div>
    </td>
    <td>
        <a href="${h.url('content', id=content['id'])}" onclick="cb_frag($(this), '${h.url('content', id=content['id'], format='frag')}'); return false;">
            <p class="content_title">${content['title']}</p>
        </a>
    </td>
    % if location:
    <td>
        flag
    </td>
    % endif
    <td>
        rating <br/> comments
    </td>
    <td>
        ##${member_includes.avatar(content['creator'], show_name=False, class_="content_creator_thumbnail")}
    </td>
</%def>

## Content Thumbnail Icons
<%def name="content_thumbnail_icons(content)">
    <div class="icons">
        % if content['private']:
            ${h.icon('private')}
        % endif
        % if content['edit_lock']:
            ${h.icon('edit_lock')}
        % endif
        % if 'response_type' in content:
            ${h.icon(content['response_type'])}
        % endif
    </div>
</%def>