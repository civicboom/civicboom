<%inherit file="/frag/common/frag.mako"/>

<%!
    import copy
    import types
    import datetime
    import civicboom.lib.constants as constants
    
    rss_url = True
%>

<%namespace name="member_includes" file="/html/web/common/member.mako" />

##------------------------------------------------------------------------------
## Frag List Template
##------------------------------------------------------------------------------
## For frag_containers that only display a list (frag_col_1)
## Consistant title bar and styling for list fragments

<%def name="init_vars()">
    <%
        self.attr.share_url        = h.url('current') #format='html'
        #self.attr.auto_georss_link = True
        
        args, kwargs = c.web_params_to_kwargs
        icon, description = constants.get_list_titles(kwargs.get('list'))
        self.attr.title     = "%s (%s)" % (description, d['list']['count'] )
        self.attr.icon_type = icon
    %>
</%def>
<%def name="body()">
    <div class="frag_col">
    ${next.body()}
    </div>
</%def>
<%def name="actions_common()">
    ${self.georss_link()}
</%def>
<%def name="actions_specific()">
    ## Pagination
    <%
        args, kwargs = c.web_params_to_kwargs
        kwargs = copy.copy(kwargs)
        if 'format' in kwargs:
            del kwargs['format']
        offset = d['list']['offset']
        limit  = d['list']['limit']
        count  = d['list']['count']
        items  = len(d['list']['items'])
    %>
    % if offset > 0:
        <% kwargs['offset'] = offset - limit %>
        <a href="${h.url('current', format='html', **kwargs)}" onclick="cb_frag_load($(this), '${h.url('current', format='frag', **kwargs)}'); return false;">prev</a>
    % endif
    % if offset + items < count:
        <% kwargs['offset'] = offset + limit %>
        <a href="${h.url('current', format='html', **kwargs)}" onclick="cb_frag_load($(this), '${h.url('current', format='frag', **kwargs)}'); return false;">next</a>
    % endif
</%def>


##------------------------------------------------------------------------------
## Public Methods - Content and Memeber lists
##------------------------------------------------------------------------------
## When imported, these are the main methods of use
<%def name="member_list_thumbnails(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_member_thumbnail, type_=('ul','li'), list_class='member'        , *args, **kwargs)}
</%def>

<%def name="member_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_member       , type_=('table','tr'), list_class='member'        , *args, **kwargs)}
</%def>

<%def name="content_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_content      , type_=('table','tr'), list_class='content'       , *args, **kwargs)}
</%def>

<%def name="group_members_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_group_members, type_=('table','tr'), list_class='group_members' , *args, **kwargs)}
</%def>

<%def name="message_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_message      , type_=('ul','li')   , list_class='messages', empty_message=_('You have no messages')      , *args, **kwargs)}
</%def>

<%def name="sponsored_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_sponsored, type_=('table','tr'),   content_class='sponsored_content',  list_class='content',   *args,  **kwargs)}
</%def>


##------------------------------------------------------------------------------
## Private Rendering Structure
##------------------------------------------------------------------------------

<%def name="frag_list(cb_list, title, href=None, show_heading=True, hide_if_empty=True, type_=('ul','li'), content_class=None, list_class='', icon='', render_item_function=None, empty_message=None, actions=None, *args, **kwargs)">
    <%
        count = None
        if isinstance(cb_list, dict) and 'items' in cb_list:
            items = cb_list.get('items')
            count = cb_list.get('count')
        else:
            items = cb_list

        if not isinstance(items, list):
            items      = [items]
            show_count = False
        
        if not title:
            show_count = False
        if not count:
            count = len(items)
        
        # If HREF is a dict then generate two URL's from it
        #  1.) the original compatable call
        #  2.) a json formatted version for the AJAX call
        js_link_to_frag_list = ''
        if isinstance(href, tuple):
            href_args   = href[0]
            href_kwargs = href[1]
            href_kwargs['private'] = True # AllanC - short term hack - infuture this will only be needed on private profile pages, it may help caching if it's not included every time, future investigation needed as private=true may disabled the public cache
            href      = h.url(*href_args, **href_kwargs)
            href_kwargs['format'] = 'frag'
            href_frag = h.url(*href_args, **href_kwargs)
            js_link_to_frag_list = h.literal("""onclick="cb_frag($(this), '%s', 'frag_col_1'); return false;" """ % href_frag)
    %>
    % if hide_if_empty and not count:
      % if empty_message:
        ${empty_message}
      % endif
    % else:
        % if show_heading:
        <div class='frag_list'>
            <h2>
                % if icon:
                <span class="icon16 i_${icon}"><span>${icon}</span></span>
                % endif
                % if href:
                <a href="${href}" ${js_link_to_frag_list}>${title}</a>
                % else:
                ${title}
                % endif
                ##% if show_count:
                <span class="count">${count}</span>
                ##% endif
                % if actions:
                    <div class="list_actions">
                    % if type(actions) == types.FunctionType:
                        ${actions()}
                    % else:
                        ${actions}
                    % endif
                    </div>
                % endif
            </h2>
        % endif
            % if content_class:
                <div class=${content_class}>
            % else:
                <div class="frag_list_contents">
            % endif
            <${type_[0]} class="${list_class}">
                ##% for item in items[0:limit]:
                % if count:
                  % for item in items:
                  ##<${type_[1]}>
                    ${render_item_function(item, *args, **kwargs)}
                  ##</${type_[1]}>
                  % endfor
                % elif empty_message:
                  <tr><td>${empty_message}</td></tr>
                % endif
            </${type_[0]}>
            % if href and show_heading and len(items) < count:
            <a href="${href}" ${js_link_to_frag_list} class="link_more">${count-len(items)} more</a>
            % endif
            </div>
            ##<div style="clear: both;"></div>
        % if show_heading:
        </div>
        % endif
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
    <td style="padding-top: 3px;">
        ${member_includes.avatar(member, class_="thumbnail_small")}
    </td>
    <td style="padding-left: 3px">
        ## AllanC - short term botch to add follow option to member list
        ${h.secure_link(
            h.args_to_tuple('member_action', action='follow'    , id=member['username'], format='redirect') ,
            value           = _('Follow') ,
            value_formatted = h.literal("<span class='icon16 i_follow' style='float:right;'></span>%s") % '',#_('Follow'),
            title           = _("Follow %s" % member['name'] or member['username']) ,
            json_form_complete_actions = "cb_frag_reload('members/%s');" % member['username'] ,
        )}
        
        <a href="${h.url('member', id=member['username'])}" onclick="cb_frag($(this), '${h.url('member', id=member['username'], format='frag')}'); return false;">
        ${member.get('name')}
        </a>
		<br/><small>
			<!-- Following ${member['num_following']}; -->
			% if member['type'] == 'group' and member['num_members']:
				${member['num_followers']} followers; ${member['num_members']} members
			% else:
				${member['num_followers']} followers
			% endif
		</small>
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

    <% from civicboom.model.member import group_member_roles %>
    ##, group_join_mode, group_member_visibility, group_content_visibility

    ## Remove
    <%def name="remove_member(member)">
        % if c.logged_in_persona and ((c.logged_in_persona.username == member['username'] and permission_remove_self) or (c.logged_in_persona.username != member['username'] and permission_remove)):
            ${h.form(h.args_to_tuple('group_action', id=id, action='remove_member', format='redirect'), method='post', json_form_complete_actions="cb_frag_reload(current_element); cb_frag_reload('members/%s');" % id)}
                <input type="hidden" name="member" value="${member['username']}"/>
                <input type="submit" name="submit" value="${_('Remove')}"/>
            ${h.end_form()}
        % endif
    </%def>

    ## Set Role
    <%def name="set_role(member)">
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
    </%def>
    
    % if not permission_set_role:
    <td>${member['role']}</td>
    % else:
    <td>${set_role(member)}</td>
    % endif
    
    % if permission_remove or permission_remove_self:
    <td>${remove_member(member)}</td>
    % else:
    <td></td>
    % endif
</tr>
</%def>


##------------------------------------------------------------------------------
## Content Item
##------------------------------------------------------------------------------

<%def name="render_item_content(content, extra_info=False, creator=False)">
<tr>
    <%
        id = content['id']
    
        item_url = h.url(controller='contents', action='show', id=id, title=h.make_username(content['title']))
    
        js_link_to_frag = True
        if js_link_to_frag:
            js_link_to_frag = h.literal(""" onclick="cb_frag($(this), '%s'); return false;" """ % h.url('content', id=id, format='frag'))
        else:
            js_link_to_frag = ''
    %>

    <td>
        <a class="thumbnail" href="${item_url}" ${js_link_to_frag}>
            ${content_thumbnail_icons(content)}
            <img src="${content['thumbnail_url']}" alt="${content['title']}" class="img" />
        </a>
    </td>
    
    <td class="content_details">
        <a href="${item_url}" ${js_link_to_frag}>
            <p class="content_title">${h.truncate(content['title']  , length=45, indicator='...', whole_word=True)}</p>
        </a>
        
        % if extra_info:
            % if   content['type']=='article' and (content.get('parent_id') or content.get('parent')):
                <%
                    (parent_url_static, parent_url_frag) = h.url_pair('content', id=content.get('parent_id') or content['parent']['id'], gen_format='frag')
                %>
                <p>${_('In response to:')}
                    <a href="${parent_url_static}" onclick="cb_frag($(this), '${parent_url_frag}'); return false;">
                        % if content.get('parent'):
                        ${h.truncate(content['parent']['title'], length=30, indicator='...', whole_word=True)}
                        % else:
                        content
                        % endif
                    </a>
                </p>
            % elif content['type']=='article'   :
                <p>
                ${_('Views')}:${content['views']}
                % if content.get('tags'):
                , ${_('Tags')}:${content['tags'][:3]}
                % endif
                </p>
            % elif content['type']=='assignment':
                <%
                    (response_url_static, response_url_frag) = h.url_pair('contents', response_to=id, include_fields='creator,parent', gen_format='frag')
                %>
                <p><a href="${response_url_static}" onclick="cb_frag($(this), '${response_url_frag}', 'frag_col_1'); return false;">${_('Responses')}: ${content['num_responses']}</a></p>
            % endif
        % endif
        
        <p class="timestamp">
            ${timestamp(content)}
        </p>
    </td>

    <%doc>
        % if creator and 'creator' in content:
          <p><small class="content_by">By: ${content['creator']['name']}</small>
        % endif
    </%doc>

    <td class="creator">
        ## Creator avatar
        % if creator and 'creator' in content:
            ${member_includes.avatar(content['creator'], class_="thumbnail_small")}
        % endif
        ## Responses show parent Creator
        ##% if content.get('parent') and content['parent'].get('creator'):
        ##    ${member_includes.avatar(content['parent']['creator'], class_="thumbnail_small")}
        ##% endif
    </td>
    
</tr>
% if request.GET.get('term', '') and 'content_short' in content:
<tr><td colspan="5">
	## content_short is stripped of html tags, so any that are in here are search highlights
	<small class="content_short">${content['content_short']|n}</small>
</td></tr>
% endif
</%def>

## Content Thumbnail Icons
<%def name="content_thumbnail_icons(content)">
    <div class="icons">
        ## AllanC - HACK!! please remove type==draft after issue #515 is fixed
        % if content.get('private') or content.get('type')=='draft':
            ${h.icon('private')}
        % endif
        % if content.get('edit_lock'):
            ${h.icon('edit_lock')}
        % endif
        % if content.get('approval') and content.get('approval') != 'none':
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
            css_class="icon16 i_delete",
            json_form_complete_actions = "cb_frag_reload(current_element);" ,
        )}
    % endif
    
    % if message.get('source') and list!='sent':
        ${member_includes.avatar(message['source'], class_="thumbnail_small source")}
    % elif list=='notification':
        <div class="icon16 i_notification" style="float: left; margin: 3px 0 0 3px;"><span>Notification</span></div>
    % endif
    
    % if message.get('target') and list=='sent':
        ${member_includes.avatar(message['target'], class_="thumbnail_small target")}
    % endif
    <div style="margin-left: 22px;">
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
             onclick = "cb_frag($(this), '${url('message', id=message['id'], format='frag')}', 'frag_col_1'); return false;"
          >
              <p class="subject">${message['subject']}</p>
          </a>
      % endif
      <p class="timestamp">
        % if message.get('source') and list!='sent':
            From: ${message['source']['name']}
        % endif
        % if message.get('target') and list=='sent':
            To: ${message['target']['name']}
        % endif
      </p>
      <p class="timestamp">${_('%s ago') % h.time_ago(message['timestamp'])}</p>
    </div>
    
</li>
</%def>

##------------------------------------------------------------------------------
## Sponsored Content Item
##------------------------------------------------------------------------------
<%def name="render_item_sponsored(content, location=False, stats=False, creator=False)">
<tr style="width: 100%;">
    <%
        id = content['id']
    
        js_link_to_frag = True
        if js_link_to_frag:
            js_link_to_frag = h.literal(""" onclick="cb_frag($(this), '%s'); return false;" """ % h.url('content', id=id, format='frag'))
        else:
            js_link_to_frag = ''
    %>

    <td colspan="2" class="content_title">
        <a href="${h.url(controller='contents', action='show', id=id, title=h.make_username(content['title']))}" ${js_link_to_frag}>
            <p>${h.truncate(content['title']  , length=45, indicator='...', whole_word=True)}</p>
        </a>
        % if content and 'creator' in content:
            <div class="creator-avatar">
                ${member_includes.avatar(content['creator'], class_="thumbnail_small")}
            </div>
        % endif
    </td>
</tr>
<tr>
    <td class="thumbnail" >
        <a href="${h.url(controller='contents', action='show', id=id, title=h.make_username(content['title']))}" ${js_link_to_frag}>
            ${content_thumbnail_icons(content)}
            <img src="${content['thumbnail_url']}" alt="${content['title']}" class="img"/>
        </a>
    </td>
    
    <td class="content">
        % if content and 'content_short' in content:
            <p>"${content['content_short']}"</p>
        % endif
    </td>
    
</tr>
<tr>
    <td colspan="2" class="content-info">
        % if content and 'creator' in content:
            <div class="creator">
                <small class="content_by">By: ${content['creator']['name']}</small>
            </div>
        % endif
        
        <div class="timestamp">
            <small>${timestamp(content)}</small>
        </div>
        
        % if content and 'views' in content:
            <div class="views">
                <small>${content['views']} views</small>
            </div>
        % endif
        
        % if content and 'num_responses' in content:
            <div class="responses">
                <small>${content['num_responses']} responses</small>
            </div>
        % endif
        
        % if content and 'num_comments' in content:
            <div class="comments">
                <small>${content['num_comments']} comments</small>
            </div>
        % endif
    </td>
</tr>
<tr>
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
    % if creator and 'creator' in content:
    <td class="creator">
        ${member_includes.avatar(content['creator'], class_="thumbnail_small")}
    </td>
    % endif
</tr>
% if request.GET.get('term', '') and 'content_short' in content:
<tr><td colspan="5">
	## content_short is stripped of html tags, so any that are in here are search highlights
	<small class="content_short">${content['content_short']|n}</small>
</td></tr>
% endif
</%def>

##------------------------------------------------------------------------------
## Timestamp
##------------------------------------------------------------------------------
<%def name="timestamp(content)">
    % if content['type']=='assignment':
        <% publish = h.time_ago(content['publish_date']) %>
        % if   content['event_date'] and content['event_date'] > h.now():
            ${_('Set %s ago, Event in %s time') % (publish, h.time_ago(content['event_date']) )}
        % elif content['due_date'  ] and content['due_date'  ] > h.now():
            ${_('Set %s ago, Due in %s time'  ) % (publish, h.time_ago(content['due_date']  ) )}
        % else:
            ${_('Set %s ago'                  ) % (publish                                    )}
        % endif
    % elif content['type']=='draft':
        % if content.get('parent'):
            % if   content['parent']['event_date'] and content['parent']['event_date'] > h.now():
                ${_('Event in %s time'  ) % h.time_ago(content['parent']['event_date'])}
            % elif content['parent']['due_date'  ] and content['parent']['due_date'  ] > h.now():
                ${_('Due in %s time'  ) % h.time_ago(content['parent']['event_date'])}
            % endif
        % endif
        % if content.get('sceduled_publish_date'):
            ${_('Will be published in %s time'  ) % h.time_ago(content['sceduled_publish_date'])}
        % endif
    % else:
        ${_('%s ago') % h.time_ago(content['update_date'])}
    % endif
</%def>