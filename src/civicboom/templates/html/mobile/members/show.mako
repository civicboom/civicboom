<%inherit file="/html/mobile/common/mobile_base.mako"/>

##-----------------------------------------------------------------------------
## includes
##-----------------------------------------------------------------------------

<%namespace name="content_list_includes" file="/html/mobile/contents/index.mako" />
<%namespace name="member_list_includes"  file="/html/mobile/members/index.mako" />

<%namespace name="member_includes" file="/html/mobile/common/member.mako" />

<%namespace name="frag_list"       file="/frag/common/frag_lists.mako" />


<%def name="page_title()">${d['member'].get('name')}</%def>

<%def name="body()">
    <%
        # AllanC - hu? - this only renders an API return, withc is always a dict? so why is this here?
        #if hasattr(member,'to_dict'):
        #    member = member.to_dict()
        
        member    = d['member']
        id        = member.get('id')
        name      = member.get('name')
        current_user = c.logged_in_persona and self.id == c.logged_in_persona.id
        actions   = d['actions']
    %>
    
    ##--------------------------------------------------------------------------
    ## Main member detail page (username/description/etc)
    ##--------------------------------------------------------------------------
    <%self:page>
        ${self.swipe_event('#member-details-%s' % id, '#member-extra-%s' % id, 'left')}
        <%def name="page_attr()"   >id="member-details-${id}" class="member_details_page"</%def>
        <%def name="header()"      >${self.header(title=self.name, next_link="#member-extra-%s" % id)}</%def>
        <%def name="page_content()">
            ##${parent.flash_message()}
            ## BODY
            ##${signout_navbar()}
            
            ## Full user details for member/profile pages
            ## Includes username/etc, description, followers/etc
            
            ##% if member:

            <div class="member_details">
                ## Avatar/name
                <h3>${member['name']}</h3>
                ${member_includes.avatar(member, as_link=0, img_class="avatar")}
                <p>Username: <b>${name}</b></p>
                <p>Type: <b>${member['type'].capitalize()}</b></p>
                
                <div class="separator" style="padding: 0.5em;"></div>
                
                ## Message and notification bar --------------------------------
                ## AllanC - only for profile view - can this be abstracted?
                % if d.get('num_unread_messages'):
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

                
                ## Action Buttons ----------------------------------------------
                % if actions:
                    % if 'message' in actions:
                        <a href="${h.url(controller='messages', action='new', target=id)}" data-rel="dialog" data-transition="fade"><button>Send message</button></a>
                    % endif
            
                    % if 'follow' in actions:
                        ${h.secure_link(
                            h.url('member_action', action='follow', id=id, format='redirect') ,
                            value           = _('Follow'),
                            value_formatted = h.literal("<button>%s</button>") % _('Follow'),
                            title           = _("Follow %s" % name) ,
                        )}
                    % endif
                    
                    % if 'unfollow' in actions:
                        ${h.secure_link(
                            h.url('member_action', action='unfollow', id=id, format='redirect') ,
                            value           = _('Stop Following') if 'follow' not in actions else _('Ignore invite') ,
                            value_formatted = h.literal("<button>%s</button>") % _('Stop Following'),
                            title           = _("Stop following %s" % name) if 'follow' not in actions else _('Ignore invite from %s' % name) ,
                        )}
                    % endif
                    
                    % if 'join' in actions:
                        ${h.secure_link(
                            h.url('group_action', action='join'       , id=id, member=c.logged_in_persona.id, format='redirect') ,
                            value           = _('Join _group') ,
                            value_formatted = h.literal("<button>%s</button>") % _('Join _Group'),
                        )}
                    % endif
                    
                    % if 'join_request' in actions:
                        ${h.secure_link(
                            h.url('group_action', action='join'       , id=id, member=c.logged_in_persona.id, format='redirect') ,
                            value           = _('Request to join _group') ,
                            value_formatted = h.literal("<button>%s</button>") % _('Request to join _group'),
                        )}
                    % endif
                % endif
                
                ## Description -------------------------------------------------
                <ul data-role="listview" data-inset="true">
                    ## User website
                    % if member.get('website'):
                        <li data-role="list-divider" role="heading">${_("%s's website" % name)}</li>
                        <li                                        ><a href="${member.get('website')}">${member.get('website')}</a></li>
                    % endif
                    
                    ## User description
                    % if member.get('description'):
                        <li data-role="list-divider" role="heading">${_("%s's description" % name)}</li>
                        <li                                        >${member.get('description')   }</li>
                    % endif
                </ul>
                
                ## Member Lists ------------------------------------------------
                % for list_name in ["following", "followers", "groups", "members"]:
                    ${member_list_includes.list_members_avatars(d[list_name], list_name)}
                % endfor

            </div>
        </%def>
        <%def name="footer_attr()">data-theme="a"</%def>
        <%def name="footer()"     >${signout_navbar()}</%def>
    </%self:page>
    
    ##--------------------------------------------------------------------------
    ## Extra info (content/boomed/etc)
    ##--------------------------------------------------------------------------
    <%self:page>
        ${self.swipe_event('#member-extra-%s' % id, '#member-details-%s' % id, 'right')}
        <%def name="page_attr()"   >id="member-extra-${id}" class="member_extra_page"</%def>
        <%def name="header()"      >${self.header(title=name, back_link="#member-details-%s"%id)}</%def>
        <%def name="page_content()">
            <h2 style="text-align: center;">${name}'s ${_('_content')}</h2>
            
            ## List the content relating to this user
            ## Includes assignments, articles, responses, etc
            <div class="member_content">
                <% content_lists = [
                    (_("Active requests"), 'assignments_active'),
                    (_("Responses"      ), 'responses'         ),
                    (_("Stories"        ), 'articles'          ),
                ] %>
                % for title, list_name in content_lists:
                    ${content_list_includes.list_contents(d[list_name], title=title)}
                % endfor
            </div>
        </%def>
            
        <%def name="footer_attr()">data-theme="a"</%def>
        <%def name="footer()"     >${signout_navbar()}</%def>
    </%self:page>


    ##--------------------------------------------------------------------------
    ## Persona switch
    ##--------------------------------------------------------------------------
    % if current_user:
    <self:page>
        <%def name="page_attr()"   >id="member_persona-${id}" class="member_persona"</%def>
        <%def name="page_header()" ><h1>Switch persona</h1></%def>
        <%def name="page_content()">
            <h2>Select the persona you want to switch to</h2>
            <ul data-role="listview" data-inset="true">
                <%def name="persona_select(member, **kwargs)">
                    <%
                        current_persona = member==c.logged_in_persona
                    %>
                    <li
                        % if current_persona:
                            class   = "current_persona"
                            onclick = "window.location = '/profile';"
                            data-theme  = "a"
                        % else:
                            onclick = "$(this).find('form').submit();"
                        % endif
                    >
                        <img src="${member.avatar_url}" class="thumbnail" />
                        <h1 class="name">${member.name or member.username}</h1>
                        % for k,v in kwargs.iteritems():
                            % if v:
                                <p>${_(k.capitalize())}: ${_(str(v).capitalize())}</p>
                            % endif
                        % endfor
                        % if not current_persona:
                                ${h.secure_link(
                                    h.url(controller='account', action='set_persona', id=member.username, format='html') ,
                                    'switch user',
                                    css_class='hidden',
                                )}
                        % else:
                            <p>This is your current persona</p>
                        % endif
                    </li>
                </%def>
                
                <%
                    num_members = None
                    if hasattr(c.logged_in_persona, 'num_members'):
                        num_members = c.logged_in_persona.num_members
                %>
                
                ## Show default persona (the user logged in)
                ${persona_select(c.logged_in_user, followers=num_followers)}
                
                ## Show current persona (current group persona if applicable)
                % if c.logged_in_persona != c.logged_in_user:
                    ${persona_select(c.logged_in_persona, role=c.logged_in_persona_role, members=num_members)}
                % endif
                
                ## Show currently logged in persona's groups:
                % for membership in [membership for membership in c.logged_in_persona.groups_roles if membership.status=="active" and membership.group!=c.logged_in_persona and membership.group!=c.logged_in_user]:
                    ${persona_select(membership.group, role=membership.role, members=membership.group.num_members)}
                % endfor
            </ul>
        </%def>
    </self:page>
    % endif
    
</%def>

##-----------------------------------------------------------------------------
## Signout nav bar link
##-----------------------------------------------------------------------------
<%def name="signout_navbar()">
    % if self.current_user:
        <div data-role="navbar" class="ui-navbar" data-theme="a">
            <ul>
                <li>
                    <a href="#member_persona-${self.id}" data-rel="dialog" data-transition="fade">Switch persona</a>
                </li>
                % if "logout" in self.actions:
                    <li>
                        ${h.secure_link(
                            h.url(controller='account', action='signout'),
                            _('Sign out'),
                            css_class="button",
                        )}
                    </li>
                % endif
                <li>
                    <a href="${h.url(controller='misc', action='force_web')}" rel="external">View full website</a>
                </li>
            </ul>
        </div>
        </div>
    % endif
</%def>

<%doc>
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
</%doc>




##-----------------------------------------------------------------------------
## 
##-----------------------------------------------------------------------------




