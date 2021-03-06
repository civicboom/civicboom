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
</%def>
    
<%def name="pagination()">
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
    <div class="pagination">
        % if offset > 0:
            <% kwargs['offset'] = offset - limit %>
            <a href="${h.url('current', format='html', **kwargs)}" data-frag="${h.url('current', format='frag', **kwargs)}" class="link_update_frag prev">${_("Previous")}</a>
        % endif
        % if offset + items < count:
            <% kwargs['offset'] = offset + limit %>
            <a href="${h.url('current', format='html', **kwargs)}" data-frag="${h.url('current', format='frag', **kwargs)}" class="link_update_frag next">${_("Next")}</a>
        % endif
        <div style="clear: both;"></div>
    </div>
</%def>


##------------------------------------------------------------------------------
## Public Methods - Content and Memeber lists
##------------------------------------------------------------------------------
## When imported, these are the main methods of use
<%def name="member_list_thumbnails(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_member_thumbnail, type_=('ul', 'li'), list_class='member_thumbnail'        , *args, **kwargs)}
</%def>

<%def name="member_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_member       , type_=('ul', 'li'), list_class='member'        , *args, **kwargs)}
</%def>

<%def name="content_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_content      , type_=('ul', 'li'), list_class='content'       , *args, **kwargs)}
</%def>

<%def name="group_members_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_group_members, type_=('table','tr'), list_class='group_members' , *args, **kwargs)}
</%def>

<%def name="message_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_message      , type_=('ul','li')   , list_class='messages', empty_message=_('You have no messages')      , *args, **kwargs)}
</%def>

<%def name="sponsored_list(*args, **kwargs)">
    ${frag_list(render_item_function=render_item_sponsored, type_=('table','tr'),   show_count=False, content_class='sponsored_content',  list_class='content',   *args,  **kwargs)}
</%def>


##------------------------------------------------------------------------------
## Private Rendering Structure
##------------------------------------------------------------------------------

<%def name="frag_list(cb_list, title, href=None, show_heading=True, show_count=True, paginate=False, hide_if_empty=True, type_=('ul','li'), content_class=None, list_class='', icon='', render_item_function=None, empty_message=None, actions=None, *args, **kwargs)">
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
        
        # If HREF is a tuple of *args **kwargs then generate two URL's from it
        #  1.) the original compatable call
        #  2.) a json formatted version for the AJAX call
        js_link_to_frag_list = ''
        href_args   = []
        href_kwargs = {}
        data_frag = ''
        if isinstance(href, tuple):
            href_args   = href[0]
            href_kwargs = href[1]
            
        # If CB list is an API list, it could have kwargs as to how the list is generated, we can recreate the url automatically with these kwargs
        if not href and isinstance(cb_list, dict) and cb_list.get('kwargs'):
            href_args   = [cb_list.get('type')] # AllanC - hack - we know the list type 'content' or 'member' we need to put this string in an arg list but also the controllers are called 'contents' and 'members' .. the propper way would be to use the singular pluran data in the url_routing stuff, but this works for now. It may even be worth changing the name on the list from 'content' to 'contents' to match
            href_kwargs = cb_list.get('kwargs')
        
        if href_args or href_kwargs:
            href_kwargs['private'] = True # AllanC - short term hack - infuture this will only be needed on private profile pages, it may help caching if it's not included every time, future investigation needed as private=true may disabled the public cache
            href      = h.url(*href_args, **href_kwargs)
            href_kwargs['format'] = 'frag'
            href_frag = h.url(*href_args, **href_kwargs)
            data_frag = href_frag
    %>
    % if hide_if_empty and not count:
      % if empty_message:
        ${empty_message}
      % endif
    % else:
        % if show_heading:
        <div class='frag_list'>
            <h2>
                ##% if icon:
                ##<span class="icon16 i_${icon}"><span>${icon}</span></span>
                ##% endif
                % if href:
                    <a class="link_new_frag" href="${href}" data-frag="${data_frag}">
                    ##<a href="${href}" ${js_link_to_frag_list}>
                        ${title}
                    </a>
                % else:
                ${title}
                % endif
                % if show_count:
                <span class="count">${count}</span>
                % endif
                % if actions:
                    <div class="list_actions">
                    % if type(actions) == types.FunctionType:
                        <span class="action_pad">${actions()}</span>
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
            </div>
            % if href and show_heading and len(items) < count:
            <div class="link_more">
                <a class="link_new_frag" href="${href}" data-frag="${data_frag}">
                ##<a href="${href}" ${js_link_to_frag_list} class="link_more">
                    % if show_count:
                        ${_("%d more") % (count-len(items))}
                    % else:
                        ${_("more")}
                    % endif
                </a>
            </div>
            % endif
            % if paginate:
                ${pagination()}
            % endif
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
    <li class="member_item">
        ${member_includes.avatar(member, class_="thumbnail_small")}
        
        <div class="member_details">  
            <% show_type = "[H]" if member.get('type') == "group" else "" %>
            
            <a class="link_new_frag" href="${h.url('member', id=member['username'])}" data-frag="${h.url('member', id=member['username'], format='frag')}">
                ${member.get('name')}
            </a>
    		<br/>
    		<small>
    			<!-- Following ${member['num_following']}; -->
    			% if member['type'] == 'group' and member['num_members']:
    				${member['num_followers']} followers; ${member['num_members']} members
    			% else:
    				${member['num_followers']} followers
    			% endif
    		</small>
        </div>
        
        <span class="follow">
            ${show_type}
            ## AllanC - short term botch to add follow option to member list
            ${h.secure_link(
                h.args_to_tuple('member_action', action='follow'    , id=member['username'], format='redirect') ,
                value           = _('Follow') ,
                value_formatted = "<span class='icon16 i_follow'></span>",
                title           = _("Follow") + " " + (member['name'] or member['username']),

            )}
        </span>
    </li>
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
            ${h.form(h.args_to_tuple('group_action', id=id, action='remove_member', format='redirect'), method='post', data=dict(json_complete="[ ['update'],['update', ['/profile', '%s']]]" % h.url('members', id=id)))}
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
    
    </tr><tr>
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
    <%
        id = content['id']
    
        item_url = h.url(controller='contents', action='show', id=id, title=h.make_username(content['title']))
        data_frag = h.url(controller='contents', action='show', id=id, format='frag')
    %>

    <li class="content_item">
        <a class="link_new_frag" href="${item_url}" data-frag="${data_frag}">
            <div class="thumbnail content_thumbnail event_load">
                ${content_thumbnail_icons(content)}
                <img src="${content['thumbnail_url']}" alt="${content['title']}" />
            </div>
        </a>
        
        <div class="content_details">
            <a class="link_new_frag" href="${item_url}" data-frag="${data_frag}">
                <p class="content_title">${h.truncate(content['title']  , length=45, indicator='...', whole_word=True)}</p>
            </a>
            % if request.GET.get('term', '') and 'content_short' in content:
            <p class="content_short">
                ${content['content_short']|n}
            </p>
            % endif
            <p class="timestamp">
                ${timestamp(content)}
                % if content['type']=='article' and (content.get('parent_id') or content.get('parent')):
                    <%
                        (parent_url_static, parent_url_frag) = h.url_pair('content', id=content.get('parent_id') or content['parent']['id'], gen_format='frag')
                    %>
                    ${_('in response to')}
                    <a class="link_new_frag" href="${parent_url_static}" data-frag="${parent_url_frag}">
                        % if content.get('parent'):
                            ${h.truncate(content['parent']['title'], length=30, indicator='...', whole_word=True)}
                        % else:
                            ${_('a _assignment')}
                        % endif
                    </a>
                % endif
            </p>
            % if extra_info:
                % if content['type']=='article':
                    <p class="extra">
                        % if content.get('tags'):
                            ${_('Tags')}: ${", ".join(content['tags'][:4])}<br />
                        % endif
                        ${_('Views')}: ${content['views']}
                    </p>
                % elif content['type']=='assignment':
                    <%
                        (response_url_static, response_url_frag) = h.url_pair('contents', response_to=id, include_fields='creator,parent', gen_format='frag')
                    %>
                    <p class="extra"><a class="link_new_frag" href="${response_url_static}" data-frag="${response_url_frag}">${_('Responses')}: ${content['num_responses']}</a></p>
                % endif
            % endif
            
            ## Creator avatar
            % if creator and 'creator' in content:
                ## AllanC - Not happy with this. We are having to include an additional link with the members name in, but as the thumbnail itself is positioned absolutely, it's just aararar
                <%doc>
                <%
                    member_url_static, member_url_frag = h.url_pair('member', id=content['creator']['username'], gen_format="frag")
                %>
                % if extra_info:
                <a class="link_new_frag" href="${member_url_static}" data-frag="${member_url_frag}" style="float: right;">
                    ${content['creator']['name']}
                </a>
                % endif
                </%doc>
                ${member_includes.avatar(content['creator'], class_="thumbnail_small", show_name=True)}
            % endif
            ## Responses show parent Creator
            ##% if content.get('parent') and content['parent'].get('creator'):
            ##    ${member_includes.avatar(content['parent']['creator'], class_="thumbnail_small")}
            ##% endif
    
            ## ${content_icons(content)}
            <a class="link_new_frag prompt" href="${item_url}" data-frag="${data_frag}">
            ##<a href="${item_url}" ${js_link_to_frag} class="prompt">
                <img src="/images/settings/arrow.png" />
            </a>
        </div>
    </li>
    
    <%doc>
        % if creator and 'creator' in content:
          <p><small class="content_by">${_("By: %s") % content['creator']['name']}</small>
        % endif
    </%doc>
    <%doc>
        % if request.GET.get('term', '') and 'content_short' in content:
        <tr><td colspan="5">
        	## content_short is stripped of html tags, so any that are in here are search highlights
        	<small class="content_short">${content['content_short']|n}</small>
        </td></tr>
        % endif
    </%doc>
</%def>

<%def name="content_icons(content)">
    <div class="content_icons">
        ## AllanC - HACK!! please remove type==draft after issue #515 is fixed
        % if content.get('private') or content.get('type')=='draft':
            ${h.icon('private')}
        % endif
        % if content.get('edit_lock'):
            ${h.icon('edit_lock')}
        % endif
        % if content.get('approval'):
            ${h.icon(content.get('approval'))}
        % endif
        % if content.get('auto_publish_trigger_datetime'):
            ${h.icon('auto_publish')}
        % endif
        ## Media icons
        % if content.get('location'):
            ${h.icon('map')}
        % endif
    </div>
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
        % if content.get('approval'):
            ${h.icon(content.get('approval'))}
        % endif
        % if content.get('auto_publish_trigger_datetime'):
            ${h.icon('auto_publish')}
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
    <div style="float:right;">
      % if list=="to":
      <a href    = "${url('message', id=message['id'])}"
         data-frag="${url('message', id=message['id'], format='frag')}"
         class   = "icon16 i_message link_new_frag" title="Open / Reply"
      >
      </a>
      % endif
    	
    % if list!='sent':
        ${h.secure_link(
            h.args_to_tuple('message', id=message['id'], format='redirect') ,
            method="delete",
            value="",
            title=_("Delete"),
            link_class="icon16 i_delete",
            form_data=dict(
                json_complete = "[ ['update'], ['update_message_indicators'] ]"
            ),
        )}
    % endif
    </div>
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
  
		  <a href    = "${url('message', id=message['id'])}"
		     data-frag="${url('message', id=message['id'], format='frag')}"
		     class="link_new_frag">
              <p class="subject" style="height:16px;">${message['subject']}</p>
          </a>
          % if list=='notification':
          ## It is safe to use literal here as notifications only come from the system
          <p class="content">${h.literal(h.links_to_frag_links(message['content']))}</p>
          % else:
          <p class="content">${message['content']}</p>
          % endif
  
      % else:
          
          <a href    = "${url('message', id=message['id'])}"
             data-frag= "${url('message', id=message['id'], format='frag')}"
             class="link_new_frag">
              <p class="subject" style="height:16px;">${message['subject']}</p>
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
    %>

    <div class="content_title">
        <a href="${h.url(controller='contents', action='show', id=id, title=h.make_username(content['title']))}"
            data-frag="${h.url('content', id=id, format='frag')}"
            class="link_new_frag">
            <p>${h.truncate(content['title']  , length=45, indicator='...', whole_word=True)}</p>
        </a>
        <%doc><div class="content_avatar">
            % if content and 'creator' in content:
                ${member_includes.avatar(content['creator'], class_="thumbnail_small")}
            % endif
        </div></%doc>
    </div>

    <div class="separator"></div>
    
    <div class="content">
        <div class="thumbnail">
            <a href="${h.url(controller='contents', action='show', id=id, title=h.make_username(content['title']))}" ${js_link_to_frag}>
                ${content_thumbnail_icons(content)}
                <img src="${content['thumbnail_url']}" alt="${content['title']}" class="img"/>
            </a>
        </div>
        % if content and 'content_short' in content:
            ${h.truncate(content['content_short'], length=140, indicator='...', whole_word=True)}
            <a href="${h.url(controller='contents', action='show', id=id, title=h.make_username(content['title']))}" ${js_link_to_frag} style="font-size: 75%;">${_("learn more")}</a>
        % endif
        <a href="${h.url(controller='contents', action='show', id=id, title=h.make_username(content['title']))}" ${js_link_to_frag} class="prompt">${_("Click here to participate")} <img src="/images/settings/arrow.png" style="vertical-align: middle;" /></a>
    </div>

    <div class="separator"></div>

    <div class="content-info">
        % if content and 'creator' in content:
            <div class="creator">
                % if creator and 'creator' in content:
                    ${member_includes.avatar(content['creator'], class_="thumbnail_small", show_name=True)}
                    <small class="content_by">${_("%s") % content['creator']['name']}</small>
                % endif
            </div>
        % endif
        
        <div class="timestamp">
            <small>${timestamp(content)}</small>
        </div>
        
        % if content and 'views' in content:
            <div class="views">
                <small>${ungettext("%d view", "%d views", content['views']) % content['views']}</small>
            </div>
        % endif
        
        % if content and 'num_responses' in content:
            <div class="responses">
                <small>${ungettext("%d response", "%d responses", content['num_responses']) % content['num_responses']}</small>
            </div>
        % endif
        
        <%doc>% if content and 'num_comments' in content:
            <div class="comments">
                <small>${_("%d comments") % content['num_comments']}</small>
            </div>
        % endif</%doc>
    </div>
    <div class="separator"></div>
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
