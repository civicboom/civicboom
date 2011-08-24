<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%def name="page_title()">
    % if hasattr(next, 'page_title'):
        ${next.page_title()}
    % endif
</%def>

<%def name="body()">
    ${next.body()}
</%def>

##------------------------------------------------------------------------------
## Display parent content of content (with list divider) if it exists
##------------------------------------------------------------------------------
<%def name="parent_content(item)">
    % if item.get('parent'):
        <% parent = item['parent'] %>
        <li data-role="list-divider" role="heading">
            Parent ${parent['type']}
        </li>
        ${content_li(parent)}
    % endif
</%def>

##------------------------------------------------------------------------------
## Generate li elements for a list
##------------------------------------------------------------------------------
<%def name="generate_list(list, method, title=None)">
    % if method and list.get('count') and list['count']:
        <ul data-role="listview" data-inset="true" data-split-icon="delete" data-split-theme="d">
            % if title:
                <li data-role="list-divider" role="heading">
                    ${title}
                    <span class="ui-li-count">${list['count']}</span>    
                </li>
            % endif
            % for item in list['items']:
                ${method(item)}
            % endfor
        </ul>
    % endif
</%def>

##------------------------------------------------------------------------------
## Generate li elements for a list of contents
##------------------------------------------------------------------------------
<%def name="list_contents(list, title=None)">
    ${generate_list(list, content_li, title)}
</%def>

##------------------------------------------------------------------------------
## Generate li elements for a list of members
##------------------------------------------------------------------------------
<%def name="list_members(list, title=None)">
    ${generate_list(list, member_li, title)}
</%def>

##------------------------------------------------------------------------------
## Generate li elements for a list of messages
##------------------------------------------------------------------------------
<%def name="list_messages(list, title=None)">
    ${generate_list(list, message_li, title)}
</%def>

##------------------------------------------------------------------------------
## Generate a single li element for the given content item
##------------------------------------------------------------------------------
<%def name="content_li(item)">
    <li>
        <a href="${h.url(controller='contents', action='show', id=item['id'], title=h.make_username(item['title']))}" rel="external">
            <img src="${item['thumbnail_url']}" class="thumbnail" />
            <h3>${item['title']}</h3>
            <p>${item['content_short']}</p>
        </a>
    </li>
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
            % if item.get('num_followers'):
                <p><b>${item['num_followers']}</b> followers</p>
            % endif
        </a>
    </li>
</%def>

##------------------------------------------------------------------------------
## Generate a single li element for the given message
##------------------------------------------------------------------------------
<%def name="message_li(item)">
    <%
        item_read = 1 if item['read'] else 0
    %>
    <li 
    % if not item_read:
        data-theme="b"
    % endif    
    >
        <a href="${url('message', id=item['id'])}" data-rel="dialog" data-transition="fade">
            <h3>${item['subject']}</h3>
            % if item.get('source'):
                <p><b>From ${item['source']['username']}</b></p>
            % endif
            <p>${item['content']}</p>
            <p>${item['timestamp']}</p>
        </a>
        
        ${h.secure_link(
            h.args_to_tuple('message', id=item['id'], format='redirect'),
            method="DELETE",
            title=_("Delete"),
            rel="external",
            value=h.literal("<a>smoosh</a>"),
        )}
    </li>
</%def>

##-----------------------------------------------------------------------------
## Render a navbar containing next/previous links for index lists
##-----------------------------------------------------------------------------
<%def name="pagination()">
    <%
        import copy
        
        args, kwargs = c.web_params_to_kwargs
        kwargs = copy.copy(kwargs)
        if 'format' in kwargs:
            del kwargs['format']
        list   = d['list']
        offset = list['offset']
        limit  = list['limit']
        count  = list['count']
        items  = len(list['items'])
    %>
    
    % if offset > 0 or offset + items < count:
        <div data-role="footer" data-position="fixed" data-fullscreen="true">
            <div data-role="navbar" class="ui-navbar">
                <ul>
                % if offset > 0:
                    <li>
                        <% kwargs['offset'] = offset - limit %>
                        <a href="${h.url('current', format='html', **kwargs)}" class="prev" data-direction="reverse">${_("Previous")}</a>
                    </li>
                % endif
                % if offset + items < count:
                    <li>
                        <% kwargs['offset'] = offset + limit %>
                        <a href="${h.url('current', format='html', **kwargs)}" class="next">${_("Next")}</a>
                    </li>
                % endif
                </ul>
            </div>
        </div>
    % endif
</%def>