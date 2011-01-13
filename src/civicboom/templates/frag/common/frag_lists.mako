<%inherit file="/frag/common/frag.mako"/>

<%namespace name="member_includes" file="/web/common/member.mako" />

##------------------------------------------------------------------------------
## Frag List Template
##------------------------------------------------------------------------------
## For frag_containers that only display a list (lists bridge they are sometimes refererd too)
## Consistant title bar and styling for list fragments

<%def name="init_vars()">
    <%
        self.attr.share_url        = url.current() #format='html'
        self.attr.auto_georss_link = True
    %>
</%def>
<%def name="body()">
    <div class="frag_col">
    ${next.body()}
    </div>
</%def>



##------------------------------------------------------------------------------
## Public Methods - Content and Memeber lists
##------------------------------------------------------------------------------
## When imported, these are the main methods of use
<%def name="member_list_thumbnails(*args, **kwargs)">
    <%
        if 'max' not in kwargs:
            kwargs['max'] = 24
    %>
    ${frag_list(render_item_function=render_item_member_thumbnail, type=('ul','li'), list_class='member'        , *args, **kwargs)}
</%def>

<%def name="member_list(*args, **kwargs)">
    <%
        if 'max' not in kwargs:
            kwargs['max'] = 24
    %>
    ${frag_list(render_item_function=render_item_member       , type=('table','tr'), list_class='member'        , *args, **kwargs)}
</%def>

<%def name="content_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_content      , type=('table','tr'), list_class='content'       , *args, **kwargs)}
</%def>

<%def name="group_members_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_group_members, type=('table','tr'), list_class='group_members' , *args, **kwargs)}
</%def>

<%def name="message_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_message      , type=('ul','li')   , list_class='messages'      , *args, **kwargs)}
</%def>



##------------------------------------------------------------------------------
## Private Rendering Structure
##------------------------------------------------------------------------------

<%def name="frag_list(items, title, href=None, max=3, show_count=True, hide_if_empty=True, type=('ul','li'), list_class='', icon='', render_item_function=None, *args, **kwargs)">
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
            href_kwargs['private'] = True # AllanC - short term hack - infuture this will only be needed on private profile pages, it may help caching if it's not included every time, future investigation needed as private=true may disabled the public cache
            href      = url(*href_args, **href_kwargs)
            href_kwargs['format'] = 'frag'
            href_frag = url(*href_args, **href_kwargs)
            js_link_to_frag_bridge = h.literal("""onclick="cb_frag($(this), '%s', 'bridge'); return false;" """ % href_frag)
    %>
    % if hide_if_empty and len(items)==0:
        
    % else:
        <div class='frag_list'>
            <h2>
                % if icon:
                <span class="icon icon_${icon}"><span>${icon}</span></span>
                % endif
                % if href:
                <a href="${href}" ${js_link_to_frag_bridge}>${title}</a>
                % else:
                ${title}
                % endif
                % if show_count:
                <span class="count">${show_count}</span>
                % endif
            </h2>
            <div class="frag_list_contents">
            <${type[0]} class="${list_class}">
                % for item in items[0:max]:
                ##<${type[1]}>
                    ${render_item_function(item, *args, **kwargs)}
                ##</${type[1]}>
                % endfor
            </${type[0]}>
            % if href and max > 0 and len(items) > max:
            <a href="${href}" ${js_link_to_frag_bridge} class="link_more">${len(items)-max} more</a>
            % endif
            </div>
            ##<div style="clear: both;"></div>
        </div>
    %endif
</%def>



##------------------------------------------------------------------------------
## Member Item Thumbnail
##------------------------------------------------------------------------------

<%def name="render_item_member_thumbnail(member)">
<li>
    ${member_includes.avatar(member, class_="thumbnail_small")}
</li>
</%def>

##------------------------------------------------------------------------------
## Member Item
##------------------------------------------------------------------------------

<%def name="render_item_member(member)">
<tr>
    <td>
        ${member_includes.avatar(member, class_="thumbnail_small")}
    </td>
    <td>
        ${member.get('name')}
    </td>
</tr>
</%def>



##------------------------------------------------------------------------------
## Group Members Item
##------------------------------------------------------------------------------

<%def name="render_item_group_members(member)">
<tr>
    <td>${member_includes.avatar(member, class_="thumbnail_small")}</td>
    <td>${member['name']}</td>
    
    ## AllanC - FIXME!
    ##          a lame botch for meet the KM deadline - could be much cleaner!
    ##          importing on every item!? inefficent
    ##          forcing group and actions to be in d[] (see /frag/member_actions/member_list.mako for the sibbling hack to go along with this)
    <%
        id = d['group']['id']
        permission_set_role    = 'set_role'    in d['actions']
        permission_remove      = 'remove'      in d['actions']
        permission_remove_self = 'remove_self' in d['actions']
    %>
    
    % if not permission_set_role:
    <td>${member['role']}</td>
    % else:
    <td>
        <% from civicboom.model.member import group_member_roles, group_join_mode, group_member_visibility, group_content_visibility %>
        ## Set Role
        ${h.form(h.args_to_tuple('group_action', id=id, action='set_role', format='redirect'), method='post')}
            <input type="hidden" name="member" value="${member['username']}"/>
            % if member['status']=='active':
                    ${h.html.select('role', member['role'], group_member_roles.enums)}
                    <input type="submit" name="submit" value="${_('Set role')}"/>
            % elif member['status']=='request':
                    <input type="hidden" name="role"   value=""/>
                    <input type="submit" name="submit" value="${_('Accept join request')}"/>
            % endif
        ${h.end_form()}
        
        ## Remove
        % if c.logged_in_persona and ((c.logged_in_persona.username == member['username'] and permission_remove_self) or (c.logged_in_persona.username != member['username'] and permission_remove)):
            ${h.form(h.args_to_tuple('group_action', id=id, action='remove_member', format='redirect'), method='post')}
                <input type="hidden" name="member" value="${member['username']}"/>
                <input type="submit" name="submit" value="${_('Remove')}"/>
            ${h.end_form()}
        % endif
    </td>
    % endif
</tr>
</%def>


##------------------------------------------------------------------------------
## Content Item
##------------------------------------------------------------------------------

<%def name="render_item_content(content, location=False, stats=False, creator=False)">
<tr>
    <%
        id = content['id']
    
        js_link_to_frag = True
        if js_link_to_frag:
            js_link_to_frag = h.literal(""" onclick="cb_frag($(this), '%s'); return false;" """ % h.url('content', id=id, format='frag'))
        else:
            js_link_to_frag = ''
    %>

    <td>
        <a class="thumbnail" href="${h.url('content', id=id)}" ${js_link_to_frag}>
            ${content_thumbnail_icons(content)}
            <img src="${content['thumbnail_url']}" alt="${content['title']}" class="img" />
        </a>
    </td>
    
    <td style="width:100%;">
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
</tr>
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
        % if content.get('approval'):
            ${h.icon(content.get('approval'))}
        % endif
    </div>
</%def>


##------------------------------------------------------------------------------
## Message Item
##------------------------------------------------------------------------------

<%def name="render_item_message(message, list='to')">
<%
    read_status = ''
    if 'read' in message:
        if not message['read']:
            read_status = 'unread'
%>
<li class="${read_status}">
    ##<a href="${url('message', id=message['id'])}">
    
    % if list!='sent':
        ${h.secure_link(
            h.args_to_tuple('message', id=message['id'], format='redirect') ,
            method="DELETE",
            value="",
            title=_("Delete"),
            css_class="icon icon_delete",
            json_form_complete_actions = "cb_frag_reload(current_element);" ,
        )}
    % endif
    
    % if message.get('source') and list!='sent':
        ${member_includes.avatar(message['source'], class_="thumbnail_small source")}
    % endif
    
    % if message.get('target') and list=='sent':
        ${member_includes.avatar(message['target'], class_="thumbnail_small target")}
    % endif
    
    % if 'content' in message:

        <p class="subject">${message['subject']}</p>
        % if list=='notification':
        ## It is safe to use literal here as notifications only come from the system
        <p class="content">${h.literal(h.links_to_frag_links(message['content']))}</p>
        % else:
        <p class="content">${message['content']}</p>
        % endif

    % else:
        
        <a href    = "${url('message', id=message['id'])}"
           onclick = "cb_frag($(this), '${url('message', id=message['id'], format='frag')}', 'bridge'); return false;"
        >
            <p class="subject">${message['subject']}</p>
        </a>
    % endif
    
    <p class="timestamp">${message["timestamp"][0:16]}</p>
    
    
</li>
</%def>