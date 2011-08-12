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
        <ul data-role="listview" data-inset="true">
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
## Generate li elements for a list of contents
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
            <h3>${item['name']}</h3>
            <p>Username: <b>${item['username']}</b></p>
            <p>Type: <b>${item['type'].capitalize()}</b></p>
        </a>
    </li>
</%def>

##------------------------------------------------------------------------------
## Generate a single li element for the given member
##------------------------------------------------------------------------------
<%def name="message_li(item)">
    <li>
        ## <a href="${h.url('member', id=item['username'])}" title="${item['name']}" rel="external">
            <h3>${item['content']}</h3>
            <p>${item['subject']}</p>
            <p>${item['timestamp']}</p>
        ## </a>
    </li>
</%def>