
<%namespace name="member_includes"  file="/web/common/member.mako"       />

##------------------------------------------------------------------------------
## Public Methods - Content and Memeber lists
##------------------------------------------------------------------------------

<%def name="member_list(*args, **kwargs)">
    <% kwargs['max'] = 20 %>
    ${frag_list(render_item_function=render_item_member , type=('ul','li')   , *args, **kwargs)}
</%def>

<%def name="content_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_content, type=('table','tr'), *args, **kwargs)}
</%def>

<%def name="group_members_list(*args, **kwargs)">
    ##${frag_list(render_item_function=render_item_group_members, *args, **kwargs)}
</%def>


##------------------------------------------------------------------------------
## Private Rendering Structure
##------------------------------------------------------------------------------


<%def name="frag_list(items, title, url_more=None, max=3, show_count=True, type=('ul','li'), render_item_function=None, *args, **kwargs)">
    <div class='frag_list'>
    <%
        if not isinstance(items, list):
            items=[items]
            show_count=False
        if max==None:
            max=-1
        if isinstance(show_count, bool) and show_count:
            show_count = len(items)
    %>
    <h2>
        % if url_more:
        <a href="${url_more}">${title}</a>
        % else:
        ${title}
        % endif
        % if show_count:
        <span class="count">${show_count}</span>
        % endif
    </h2>
    <${type[0]}>
        % for item in items[0:max]:
        <${type[1]}>
            ${render_item_function(item, *args, **kwargs)}
        </${type[1]}>
        % endfor
    </${type[0]}>
    % if url_more and max > 0 and len(items) > max:
    <a href="${url_more}" class="link_more">more</a>
    % endif
    </div>
</%def>



##------------------------------------------------------------------------------
## Member Item
##------------------------------------------------------------------------------

<%def name="render_item_member(member)">   
    ${member_includes.avatar(member, class_="thumbnail_small")}
</%def>


##------------------------------------------------------------------------------
## Group Members Item
##------------------------------------------------------------------------------

<%def name="render_item_group_members(members)">
</%def>


##------------------------------------------------------------------------------
## Content Item
##------------------------------------------------------------------------------

<%def name="render_item_content(content, location=False, stats=False, creator=False)">

    <%
        id = content['id']
    
        js_link_to_frag = True
        if js_link_to_frag:
            js_link_to_frag = h.literal(""" onclick="cb_frag($(this), '%s'); return false;" """ % h.url('content', id=id, format='frag'))
        else:
            js_link_to_frag = ''
    %>

    <td class="thumbnail">
        <a href="${h.url('content', id=id)}" ${js_link_to_frag}>
            ${content_thumbnail_icons(content)}
            <img src="${content['thumbnail_url']}" alt="${content['title']}" class="img" />
        </a>
    </td>
    
    <td class="title">
        <a href="${h.url('content', id=id)}" ${js_link_to_frag}>
            <p class="content_title">${content['title']}</p>
        </a>
    </td>
    % if location:
    <td>
        flag
    </td>
    % endif
    % if stats:
    <td>
        rating <br/> comments
    </td>
    % endif
    % if creator:
    <td class="creator">
        ${member_includes.avatar(content['creator'], class_="thumbnail_small")}
    </td>
    % endif
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