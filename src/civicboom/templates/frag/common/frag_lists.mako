##------------------------------------------------------------------------------
## Public Methods - Content and Memeber lists
##------------------------------------------------------------------------------

<%def name="member_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_member, *args, **kwargs)}
</%def>

<%def name="content_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_content, *args, **kwargs)}
</%def>


##------------------------------------------------------------------------------
## Private Rendering Structure
##------------------------------------------------------------------------------

<%def name="frag_list(items, title, max=3, show_count=True, render_item_function=None)">
    <% if not isinstance(items, list): items=[items]; show_count=False %>
    <% if max==None: max=-1 %>
    <h2>${title}</h2>
    <ul>
        % for item in items[0:max]:
        <li>
            ${render_item_function(item)}
        </li>
        % endfor
    </ul>
</%def>


##------------------------------------------------------------------------------
## Member Item
##------------------------------------------------------------------------------

<%def name="render_item_member(member)">
    ${member}
</%def>


##------------------------------------------------------------------------------
## Content Item
##------------------------------------------------------------------------------

<%def name="render_item_content(content)">
    ${content}
</%def>
