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
<%def name="generate_list(list, method, title=None, more=None)">
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
            % if more != None and list.get('count') > list.get('limit'):
                <li>
                    <a href="${more_link(list)}">See all ${list.get('count')} ${title.lower()}</a>
                </li>
            % endif
        </ul>
    % endif
</%def>

<%def name="more_link(list)">
    <%
        href = None
        count = list.get('count')
        limit = list.get('limit')
    
        if not href and isinstance(list, dict) and list.get('kwargs'):
            href_args   = [list.get('type')] 
            href_kwargs = list.get('kwargs')
        
        if href_args or href_kwargs:
            href_kwargs['private'] = True
            href      = h.url(*href_args, **href_kwargs)
    %>
    
    ${href}
</%def>

##------------------------------------------------------------------------------
## Generate li elements for a list of contents
##------------------------------------------------------------------------------
<%def name="list_contents(list, title='Content', more=None)">
    ${generate_list(list, content_li, title, more)}
</%def>

##------------------------------------------------------------------------------
## Generate li elements for a list of members
##------------------------------------------------------------------------------
<%def name="list_members(list, title='Members', more=None)">
    ${generate_list(list, member_li, title, more)}
</%def>

##------------------------------------------------------------------------------
## Generate li elements for a list of messages
##------------------------------------------------------------------------------
<%def name="list_messages(list, title='Message', more=None)">
    ${generate_list(list, message_li, title, more)}
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
            <p>${timestamp(item)} by ${item.get('creator').get('username')}</p>
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
            % if item.get('username'):
                <p>${item['username']}</p>
            % endif
            % if item.get('num_followers') != None:
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
        <a href="${url('message', id=item['id'])}" data-ajax="true" data-rel="dialog" data-transition="fade">
            <h3>${item['subject']}</h3>
            % if item.get('source'):
                <p><b>From ${item['source']['username']}</b></p>
            % endif
            <p>${item['content']}</p>
            <p>${item['timestamp']}</p>
        </a>
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