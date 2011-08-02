## Display parent content of content (with list divider) if it exists 
<%def name="parent_content(item)">
    % if item.get('parent'):
        <% parent = item['parent'] %>
        <li data-role="list-divider" role="heading">
            Parent ${parent['type']}
        </li>
        ${content_li(parent)}
    % endif
</%def>

## Generate li elements for a list of contents
<%def name="list_contents(list, title=None)">
    % if list.get('count') and list['count']:
        % if title:
            <li data-role="list-divider" role="heading">
                ${title}
                <span class="ui-li-count">${list['count']}</span>    
            </li>
        % endif
        % for item in list['items']:
            ${content_li(item)}
        % endfor
    % endif
</%def>

## Generate a single li element for the given content item
<%def name="content_li(item)">
    <li>
        <a href="${h.url(controller='contents', action='show', id=item['id'], title=h.make_username(item['title']))}" rel="external">
            <img src="${item['thumbnail_url']}" class="thumbnail" />
            <h3>${item['title']}</h3>
            <p>${item['content_short']}</p>
        </a>
    </li>
</%def>