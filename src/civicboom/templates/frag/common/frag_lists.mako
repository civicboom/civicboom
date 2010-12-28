<%namespace name="member_includes"  file="/web/common/member.mako"       />

##------------------------------------------------------------------------------
## Frag List Template
##------------------------------------------------------------------------------
## For frag_containers that only display a list (lists bridge they are sometimes refererd too)
## Consistant title bar and styling for list fragments

<%def name="body()">
    <div class="title_bar">
        <div class="title">
            <span class="icon icon_list"></span><span class="title_text">
                ##${next.title()}
                ${_('List')}
            </span>
        </div>
        <div class="common_actions">
            <% args, kwargs = c.web_params_to_kwargs; kwargs['format']='rss' %>
            <a href='${url.current(**kwargs)}' title='RSS' class="icon icon_rss"  ><span>RSS</span></a>
            <a href='' onclick="cb_frag_remove($(this)); return false;" title='${_('Close')}' class="icon icon_close"><span>${_('Close')}</span></a>
        </div>
    </div>

    <div class="action_bar">

    </div>

    <div class="frag_data">
        <div class="frag_col">
        ${next.frag_list_call()}
        </div>
    </div>
</%def>



##------------------------------------------------------------------------------
## Public Methods - Content and Memeber lists
##------------------------------------------------------------------------------
## When imported, these are the main methods of use
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

<%def name="frag_list(items, title, href=None, max=3, show_count=True, type=('ul','li'), render_item_function=None, *args, **kwargs)">
    <%
        if not isinstance(items, list):
            items      = [items]
            show_count = False
        if isinstance(show_count, bool) and show_count:
            show_count = len(items)
        if not title:
            show_count = False
        
        # If HREF is a dict then generate two URL's from it
        #  1.) the original compatable call
        #  2.) a json formatted version for the AJAX call
        js_link_to_frag_bridge = ''
        if isinstance(href, tuple):
            href_args   = href[0]
            href_kwargs = href[1]
            href      = url(*href_args, **href_kwargs)
            href_kwargs['format'] = 'frag'
            href_frag = url(*href_args, **href_kwargs)
            js_link_to_frag_bridge = h.literal("""onclick="cb_frag($(this), '%s', 'bridge'); return false;" """ % href_frag)
    %>
    <div class='frag_list'>
    <h2>
        % if href:
        <a href="${href}" ${js_link_to_frag_bridge}>${title}</a>
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
    % if href and max > 0 and len(items) > max:
    <a href="${href}" ${js_link_to_frag_bridge} class="link_more">more</a>
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
        % if content.get('private'):
            ${h.icon('private')}
        % endif
        % if content.get('edit_lock'):
            ${h.icon('edit_lock')}
        % endif
        % if content.get('response_type'):
            ${h.icon(content.get('response_type'))}
        % endif
    </div>
</%def>