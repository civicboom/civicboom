<%inherit file="/html/mobile/common/lists.mako"/>

<%def name="title()">${_("Explore _content")}</%def>

<%def name="list_id()"     >explore_content</%def>
<%def name="list_class()"  ></%def>
<%def name="list_content()">
    ${self.search_form()}
    ##${parent.generate_list(d['list'], content_li, title=_('Content'))}
    ${list_contents(d['list'])}
</%def>

##------------------------------------------------------------------------------
## 
##------------------------------------------------------------------------------
<%def name="list_contents(contents, title=None)">
    <%
        title = title if title else _('Content')
    %>
    ${parent.generate_list(contents, content_li, title)}
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
            <p>${timestamp(item)} by ${item.get('creator_id')}</p>
        </a>
    </li>
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
## Timestamp
##------------------------------------------------------------------------------
<%def name="timestamp(content)">
    % if content['type']=='assignment':
        <%
            publish    = h.time_ago(content['publish_date'])
            event_date = h.api_datestr_to_datetime(content['event_date'])
            due_date   = h.api_datestr_to_datetime(content['due_date']  )
        %>
        % if   event_date and event_date > h.now():
            ${_('Set %s ago, Event in %s time') % (publish, h.time_ago(event_date))}
        % elif due_date   and due_date   > h.now():
            ${_('Set %s ago, Due in %s time'  ) % (publish, h.time_ago(due_date  ))}
        % else:
            ${_('Set %s ago'                  ) % (publish                        )}
        % endif
    % elif content['type']=='draft':
        % if content.get('parent'):
            <%
                event_date = h.api_datestr_to_datetime(content['parent']['event_date'])
                due_date   = h.api_datestr_to_datetime(content['parent']['due_date']  )
            %>
            % if   event_date and event_date > h.now():
                ${_('Event in %s time'  ) % h.time_ago(event_date)}
            % elif due_date   and due_date > h.now():
                ${_('Due in %s time'    ) % h.time_ago(due_date  )}
            % endif
        % endif
        % if content.get('sceduled_publish_date'):
            ${_('Will be published in %s time'  ) % h.time_ago(content['sceduled_publish_date'])}
        % endif
    % else:
        ${_('%s ago') % h.time_ago(content['update_date'])}
    % endif
</%def>