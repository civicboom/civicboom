<%inherit file="/html/mobile/common/mobile_base.mako"/>

##-----------------------------------------------------------------------------
## includes
##-----------------------------------------------------------------------------
<%namespace name="components"      file="/html/mobile/common/components.mako" />
<%namespace name="member_includes" file="/html/mobile/common/member.mako" />
<%namespace name="list_includes"   file="/html/mobile/common/lists.mako" />
<%namespace name="frag_list"       file="/frag/common/frag_lists.mako" />

<%def name="init_vars()">
    <%
        self.member    = d['member']
        self.id        = self.member.get('id')
        self.name      = self.member.get('name')
        self.actions   = d['actions']
    %>
</%def>

<%def name="page_title()">
    ${self.id}
</%def>

<%def name="body()">

    ## Main member detail page (username/description/etc)
    <div data-role="page" data-theme="b" id="member-details-${self.id}" class="member_details_page">
        ${components.header(title=self.name, next_link="#member-extra-"+self.id)}
        
        <div data-role="content">
            ${parent.flash_message()}
            ${member_details_full(self.member)}
            <a href="#member_persona-${self.id}" data-rel="dialog" data-transition="fade">Switch persona</a>
        </div>
        
        ${signout_navbar()}
    </div>
    
    ## Extra info (content/boomed/etc)
    <div data-role="page" data-theme="b" id="member-extra-${self.id}" class="member_extra_page">
        ${components.header(title=self.name, back_link="#member-details-"+self.id)}
        
        <div data-role="content">
            <h2 style="text-align: center;">${self.id}'s ${_('_content')}</h2>
            ${member_content_list(d)}
        </div>
    </div>
    
    % if config['development_mode']:
        ## Persona switching
        <div data-role="page" id="member_persona-${self.id}" class="member_persona">
            ${persona()}
        </div>
    % endif
    
</%def>

## Persona switch
<%def name="persona()">
    <table>
        <%def name="persona_select(member, **kwargs)">
            <%
                current_persona = member==c.logged_in_persona
            %>
            <tr
                % if current_persona:
                    class   = "current_persona selectable"
                    onclick = "window.location = '/profile';"
                % else:
                    class   = "selectable"
                    onclick = "$(this).find('form').submit();"
                % endif
            >
                <td>
                    <img src="${member.avatar_url}" alt="" onerror='this.onerror=null;this.src="/images/default/avatar_user.png"'/>
                </td>
                <td>
                    <p class="name">${member.name or member.username}</p>
                    % for k,v in kwargs.iteritems():
                        % if v:
                            <p class="info">${_(k.capitalize())}: ${_(str(v).capitalize())}</p>
                        % endif
                    % endfor
                </td>
                <td class="hide_if_js">
                    % if not current_persona:
                    ${h.secure_link(
                        h.url(controller='account', action='set_persona', id=member.username, format='html') ,
                        'switch user',
                        css_class="persona_link",
                    )}
                    % endif
                </td>
            </tr>
        </%def>
        
        <%
            num_members = None
            if hasattr(c.logged_in_persona, 'num_members'):
                num_members = c.logged_in_persona.num_members
        %>
        
        ## Show default persona (the user logged in)
        ${persona_select(c.logged_in_user)}
        
        ## Show current persona (current group persona if applicable)
        % if c.logged_in_persona != c.logged_in_user:
            ${persona_select(c.logged_in_persona, role=c.logged_in_persona_role, members=num_members)}
        % endif
        
        ## Show currently logged in persona's groups:
        % for membership in [membership for membership in c.logged_in_persona.groups_roles if membership.status=="active" and membership.group!=c.logged_in_persona and membership.group!=c.logged_in_user]:
            ${persona_select(membership.group, role=membership.role, members=membership.group.num_members)}
        % endfor
    </table>
</%def>

##-----------------------------------------------------------------------------
## Signout nav bar link
##-----------------------------------------------------------------------------
<%def name="signout_navbar()">
    % if "logout" in self.actions:
        <div data-role="footer" data-position="inline" data-id="page_footer" data-theme="a">
            <div data-role="navbar" class="ui-navbar">
                <ul>
                    <li>
                        ${h.secure_link(
                            h.url(controller='account', action='signout'),
                            _('Sign out'),
                            css_class="button",
                        )}
                    </li>
                </ul>
            </div>
        </div>
    % endif
</%def>

##-----------------------------------------------------------------------------
## Short member details - Username, real name and user type + avatar
##-----------------------------------------------------------------------------
<%def name="member_details_short(member, as_link=True)">
    % if member:
        <%
            if hasattr(member,'to_dict'):
                member = member.to_dict()
        %>
        <div class="member_details">
            <ul data-role="listview" data-inset="true">
                <li>
                    % if as_link:
                    <a href="${h.url('member', id=member['username'])}" title="${member['name']}" rel="external">
                    % endif
                        ${member_includes.avatar(member, as_link=0, img_class="thumbnail")}
                        <h3>${member['name']}</h3>
                        <p>Username: <b>${member['username']}</b></p>
                        <p>Type: <b>${member['type'].capitalize()}</b></p>
                    % if as_link:
                    </a>
                    % endif
                </li>
            </ul>
        </div>
    % endif
</%def>

##-----------------------------------------------------------------------------
## Full user details for member/profile pages
## Includes username/etc, description, followers/etc
##-----------------------------------------------------------------------------
<%def name="member_details_full(member)">
    % if member:
        <%
            if hasattr(member,'to_dict'):
                member = member.to_dict()
            username = member['username']
            description = member['description']
            website = member['website']
        %>
        <div class="member_details">
            ## Avatar/name
            <h3>${member['name']}</h3>
            ${member_includes.avatar(member, as_link=0, img_class="avatar")}
            <p>Username: <b>${username}</b></p>
            <p>Type: <b>${member['type'].capitalize()}</b></p>
            
            <div class="separator" style="padding: 0.5em;"></div>
            
            ${messages_bar()}
            ${actions_buttons()}
            
            <ul data-role="listview" data-inset="true">
                ## User website
                % if website:
                    <li data-role="list-divider" role="heading">
                        ${username}'s website
                    </li>
                    <li>
                        <a href="${website}">
                            ${website}
                        </a>
                    </li>
                % endif
                
                ## User description
                % if description:
                    <li data-role="list-divider" role="heading">
                        ${username}'s description
                    </li>
                    <li>
                        ${description}
                    </li>
                % endif
            </ul>
                
            ${member_list("following")}
            ${member_list("followers")}
            ${member_list("groups")}
            ${member_list("members")}
        </div>
    % endif
</%def>

##-----------------------------------------------------------------------------
## Member action buttons (follow, etc)
##-----------------------------------------------------------------------------
<%def name="actions_buttons()">

    % if c.logged_in_user and self.actions:
            % if 'message' in self.actions:
                <a href="${h.url(controller='messages', action='new', target=self.id)}" data-rel="dialog" data-transition="fade"><button>Send message</button></a>
            % endif

            % if 'follow' in self.actions:
                ${h.secure_link(
                    h.url('member_action', action='follow', id=self.id, format='redirect') ,
                    value           = _('Follow'),
                    value_formatted = h.literal("<button>%s</button>") % _('Follow'),
                    title           = _("Follow %s" % self.name) ,
                )}
            % endif
            
            % if 'unfollow' in self.actions:
                ${h.secure_link(
                    h.url('member_action', action='unfollow', id=self.id, format='redirect') ,
                    value           = _('Stop Following') if 'follow' not in self.actions else _('Ignore invite') ,
                    value_formatted = h.literal("<button>%s</button>") % _('Stop Following'),
                    title           = _("Stop following %s" % self.name) if 'follow' not in self.actions else _('Ignore invite from %s' % self.name) ,
                )}
            % endif
            
            % if 'join' in self.actions:
                ${h.secure_link(
                    h.url('group_action', action='join'       , id=self.id, member=c.logged_in_persona.username, format='redirect') ,
                    value           = _('Join _group') ,
                    value_formatted = h.literal("<button>%s</button>") % _('Join _Group'),
                )}
            % endif
            
            % if 'join_request' in self.actions:
                ${h.secure_link(
                    h.url('group_action', action='join'       , id=self.id, member=c.logged_in_persona.username, format='redirect') ,
                    value           = _('Request to join _group') ,
                    value_formatted = h.literal("<button>%s</button>") % _('Request to join _group'),
                )}
            % endif
    % endif
</%def>

##-----------------------------------------------------------------------------
## Message and notification bar
##-----------------------------------------------------------------------------
<%def name="messages_bar()">
    % if c.logged_in_user and c.logged_in_user.username == self.id and d.get('num_unread_messages') != None:
        <%
            unread_messages =       d['num_unread_messages']
            unread_notifications =  d['num_unread_notifications']
        %>
        <div class="messages ui-grid-b" data-theme="b">
            <div class="ui-block-a">
                <a href="${h.url('messages', list='to', format='html' )}" rel="external">Messages
                % if unread_messages:
                    <br />(${unread_messages} new)
                % endif
                </a>
            </div>
            <div class="ui-block-b">
                <a href="${h.url('messages', list='sent', format='html' )}" rel="external">Sent</a>
            </div>
            <div class="ui-block-c">
                <a href="${h.url('messages', list='notification', format='html' )}" rel="external">Notifications
                % if unread_notifications:
                    <br />(${unread_notifications} new)
                % endif
                </a>
            </div>
        </div>
    % endif
</%def>

##-----------------------------------------------------------------------------
## 
##-----------------------------------------------------------------------------
<%def name="member_list(list_title)">
    <% count = d[list_title]['count'] %>
    % if count:
        <ul data-role="listview" data-inset="true">
            <li data-role="list-divider" role="heading">
                ${list_title.capitalize()}
                <span class="ui-li-count">${count}</span>
            </li>
            <li class="ui-li ui-li-static ui-body-c">
                ${member_includes.member_thumbnail_list(d[list_title])}
            </li>
        </ul>
    % endif
</%def>

##-----------------------------------------------------------------------------
## List the content relating to this user
## Includes assignments, articles, responses, etc
##-----------------------------------------------------------------------------
<%def name="member_content_list(data)">
    % if data:
        <%
            member = data['member']
            if hasattr(member,'to_dict'):
                member = member.to_dict()
            requests = data['assignments_active']
            responses = data['responses']
            articles = data['articles']
        %>
        <div class="member_content">
            ${list_includes.list_contents(requests, "Active requests", more=1)}
            ${list_includes.list_contents(responses, "Responses", more=1)}
            ${list_includes.list_contents(articles, "Stories", more=1)}
        </div>
    % endif
</%def>

##-----------------------------------------------------------------------------
## Creates the control bar/footer
##-----------------------------------------------------------------------------
<%def name="control_bar()">
    % if c.logged_in_user:
        <div data-role="navbar" class="ui-navbar">
            <ul>
                <li>
                    <a href="${h.url(controller='profile', action='index')}" rel="external">Profile</a>
                </li>
                <li>
                    <a href="${h.url(controller='contents', action='index')}" rel="external">Explore</a>
                </li>
                <li>
                    ${h.secure_link(
                        h.url(controller='account', action='signout'),
                        _('Sign out')
                    )}
                </li>
            </ul>
        </div>
    % endif
</%def>