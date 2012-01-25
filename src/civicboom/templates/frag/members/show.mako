<%inherit file="/frag/common/frag.mako"/>

<%!
    import civicboom.lib.constants as constants
    rss_url = True
%>

<%namespace name="frag_list"       file="/frag/common/frag_lists.mako"     />
<%namespace name="member_includes" file="/html/web/common/member.mako"     />
<%namespace name="popup"           file="/html/web/common/popup_base.mako" />
<%namespace name="share"           file="/frag/common/share.mako"          />
<%namespace name="components"      file="/html/web/common/components.mako" />


##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%def name="custom_share()">
    <a href="#" class="janrain_link" onclick="${share.janrain_social_call_member(self.member, 'new', self.member['type']) | n }; return false;"><p>${_("Get others involved!")}</p></a>
</%def>

<%def name="custom_share_widget()">
    
</%def>

<%def name="init_vars()">
    <%
        self.member    = d['member']
        self.id        = self.member['username']
        self.name      = self.member.get('name')
        self.actions   = d.get('actions', [])
        
        self.num_unread_messages = d.get('num_unread_messages');
        self.num_unread_notifications = d.get('num_unread_notifications');
        
        self.attr.title     = _('_' + self.member['type'].capitalize())
        self.attr.icon_type = self.member['type']
        
        self.current_user = c.logged_in_persona and self.member['username'] == c.logged_in_persona.username

        def custom_share_line():
            popup.link(
                h.args_to_tuple(controller='misc', action='get_widget', id=self.id),
                title = _('Get _widget'),
                text  = h.literal("<span class='icon16 i_widget'></span>%s") % _('Get _widget'),
            )
            
        self.attr.share_kwargs = {
            'url'               : h.url('member', id=self.id, qualified=True) ,
            'title'             : self.name ,
            'image'             : self.member['avatar_url'] ,
            ## 'custom_share_line' : custom_share_line,
            'custom_share'      : custom_share
        }
        
        # Customize layout based on logged in user or group
        if self.current_user:
        # GregM: Removed popups as we have the janrain share popup now :D
            if self.member['type'] == 'group':
                self.attr.title     = _('Current _Group Persona')
                self.attr.icon_type = 'group'
                self.attr.help_frag = 'group_persona'
            #    if c.logged_in_user and not c.logged_in_user.config['help_popup_created_group']:
            #        self.attr.popup_url = url(controller='misc', action='help', id='created_group', format='frag')
            else:
                self.attr.title     = _('Current User')
                self.attr.icon_type = 'current_user'
                self.attr.help_frag = 'profile'
            #    if c.logged_in_user and not c.logged_in_user.config['help_popup_created_user']:
            #        self.attr.popup_url = url(controller='misc', action='help', id='created_user', format='frag')
            
            self.attr.share_kwargs.update({
                'url'  : h.url('member', id=self.id, protocol='http', sub_domain='www') ,
            })
            self.attr.rss_url = h.url('member', id=self.id, format='rss', sub_domain='www')
        
        # Manipulate Action List
        # - remove actions in exclude_actions kwarg
        if self.kwargs.get('exclude_actions'):
            self.actions = list(set(self.actions) - set(self.kwargs.get('exclude_actions', '').split(',')))
        
        
        self.attr.frag_data_css_class = 'frag_member'
        
        # Contents index was sorted by date. it was awkward to get a single list from the multiple lists of a member object
        #  but shish said that clients will sort the RSS by date so it was all ok
        #self.attr.rss_url = url('contents', creator=self.id, format='rss')
        
        self.attr.auto_georss_link = True
        
        # GregM: Dynamic translation templates:
        
        trans_if = self.member['type']+('profile' if self.current_user else '')
        
        if trans_if == 'user':
            self.trans_strings = [
                #list name , icon, description
                ('all'                 , 'article'    , _('All')   ),
                ('drafts'              , 'draft'      , _("Drafts")   ),
                ('assignments_active'  , 'assignment' , _("Requests I want you to respond to")  ),
                ('assignments_previous', 'assignment' , _('Previous _assignments') ),
                ('responses'           , 'response'   , _("Responses I've written") ),
                ('articles'            , 'article'    , _("My news")    ),
            ]
        elif trans_if == 'userprofile':
            self.trans_strings = [
                #list name , icon, description
                ('all'                 , 'article'    , _('All')   ),
                ('drafts'              , 'draft'      , _("Drafts")   ),
                ('assignments_active'  , 'assignment' , _("Requests I want a response to")  ),
                ('assignments_previous', 'assignment' , _('Previous _assignments') ),
                ('responses'           , 'response'   , _("Responses I've written") ),
                ('articles'            , 'article'    , _("My news")    ),
            ]
        elif trans_if == 'group':
            self.trans_strings = [
                #list name , icon, description
                ('all'                 , 'article'    , _('All')   ),
                ('drafts'              , 'draft'      , _("Drafts")   ),
                ('assignments_active'  , 'assignment' , _("Requests we want you to respond to")  ),
                ('assignments_previous', 'assignment' , _('Previous _assignments') ),
                ('responses'           , 'response'   , _("Responses we've written") ),
                ('articles'            , 'article'    , _("My news")    ),
            ]
        elif trans_if == 'groupprofile':
            self.trans_strings = [
                #list name , icon, description
                ('all'                 , 'article'    , _('All')   ),
                ('drafts'              , 'draft'      , _("Drafts")   ),
                ('assignments_active'  , 'assignment' , _("Requests we want a response to")  ),
                ('assignments_previous', 'assignment' , _('Previous _assignments') ),
                ('responses'           , 'response'   , _("Responses we've written") ),
                ('articles'            , 'article'    , _("My news")    ),
            ]
        
        # GregM: Hand holding adverts
        hand_guidance = {
            'ind': ['advert_hand_article', 'advert_hand_response', 'advert_hand_mobile'],
            'org': ['advert_hand_content', 'advert_hand_hub', 'advert_hand_mobile'],
            'hub': ['advert_hand_widget' , 'advert_hand_assignment'],
        }
        
        self.guidance_content = {
            "assignment":{
                'guidance_class': 'long',
                'title'         : _('Ask for _articles!'),
                'secure_href'   : h.url('new_content', target_type='assignment'),
            },
            "article":{
                'title'         : _('Post _articles!'),
                'href'          : h.url(controller='misc', action='new_content'),
            },
            "response":{
                'title'         : _('Get involved!'),
                'content_text'  : _("Post your _content directly to a news organisation, on _site_name or respond to a _assignment!"),
                'href'          : h.url(controller='misc', action='new_content'),
            },
            "widget":{
                'guidance_class': 'small',
                'title'         : _('Grab the _widget for your site!'),
                'popup_href'    : h.args_to_tuple(controller='misc', action='get_widget', id=self.id),
            },
            "hub":{
                'guidance_class': 'small',
                'title'         : _('Create a _Group!'),
                'href'          : h.url(controller='misc', action='what_is_a_hub'),
            },
            "mobile":{
                'title'         : _('Make the news with the Civicboom mobile app!'),
                'href'          : h.url(controller="misc", action="about", id="mobile"),
            }
        }
        
        self.adverts_hand = []
        if self.current_user:
            my_type = 'hub' if c.logged_in_persona.__type__ == 'group' else (c.logged_in_persona.config.get('help_type') or 'ind')
            self.adverts_hand = hand_guidance[my_type]
    %>
</%def>

<%def name="invite_members(title, href_tuple, help_text, help_classes)">
    <span class="mo-help" style="display: inline;">
        ${h.frag_link(value='', title=title, class_='icon16 i_plus_blue', href_tuple=href_tuple)}
        <div class="${help_classes}">
            ${help_text}
        </div> 
    </span>
</%def>

##------------------------------------------------------------------------------
## Member Fragment
##------------------------------------------------------------------------------
<%def name="body()">
    ## AllanC!?! (c.logged_in_persona.username or c.logged_in_user.username) this is a meaninless statement because or returns one or the other? logged_in_persona always not null if logged_in_user
    % if c.logged_in_persona and c.logged_in_persona.username == self.member['username'] and request.params.get('prompt_aggregate')=='True':
        <div class="link_janrain event_load" ${share.janrain_social_data_member(self.member, 'new', self.member['type'])}></div>
    % endif
    
    ## Top row (avatar/about me)
    <div class="frag_top_row">
        <div class="frag_col">
            ## About Me
            <div class="frag_list">
            <div class="member_details">
                <div class="col_left">
                    <h2 class="name">${h.guess_hcard_name(self.member['name'])}</h2>
                    % if self.member.get('website'):
                        <p class="website"><a href="${self.member['website']}" target="_blank">${h.nicen_url(self.member['website'])}</a></p>
                    % endif
                    % if self.member.get('description'):
                        <p class="description">${self.member['description']}</p>
                    % elif c.logged_in_user and c.logged_in_user.username == self.member['username']:
                        <p class="description" style="font-size: 150%;">${_('To complete your profile, add a description')}<a href="/settings" style="color: blue;">here</a></p>
                    % else:
                        <p class="description">${_('This user has not added a description about themselves yet')}</p>
                    % endif
                    
                    <div class="separator"></div>
                    ${actions_buttons()}
                </div>
                
                <div class="col_right">
                    <div class="avatar"><img src="${self.member['avatar_url']}" alt="${self.member['username']}"></div>
                    % if 'message' in self.actions:
                        ${popup.link(
                        h.args_to_tuple('new_message', target=self.id),
                        title = _('Send message'),
                        text  = h.literal("<div class='button'>%s</div>") % _('Send message'),
                        )}
                        ##<div style="clear: both;"></div>
                    % endif
                </div>
                
                <div class="separator"></div>
            </div>
            % if self.attr.share_kwargs:
                ${share.AddThisLine(**self.attr.share_kwargs)}
            % endif
                <span style="float: right; font-size: 1.25em; padding-right: 1.1em;" class="mo-help">
                    <div class="mo-help-l">${_("The Boombox is a widget that lets your audience post their _content and respond to requests for _content")}</div>
                    <a href="#">
                    <p class="boombox_link">
                        ${popup.link(
                            h.args_to_tuple(controller='misc', action='get_widget', id=self.id),
                            title = _('Get _widget'),
                            text  = h.literal("%s") % _("Get _widget"),
                        )}
                    </p>
                    </a>
                </span>
    
                <a class="link_janrain" style="float: right; font-size: 1.25em; padding-right: 3em;" href="#" ${share.janrain_social_data_member(self.member, 'existing' if c.logged_in_persona and c.logged_in_persona.username == self.id else 'other', self.member['type'])}><p class="janrain_link">${_("Get others involved!")}</p></a>
    
            <div class="qr">
            <%
                popup.link(
                    h.args_to_tuple(controller='misc', action='get_link_embed', type='member', id=self.id),
                    title = _('Link to this member'),
                    text  = h.literal("<span class='icon16 i_widget'></span>%s") % _("Link to this member"),
                )
            %>
            </div>
            </div>    
            
            ## My requests
            % for list, icon, description in [n for n in self.trans_strings if n[0]  in ["assignments_active"]]:
            ${frag_list.content_list(
                d[list] ,
                description ,
                h.args_to_tuple('contents', creator=self.id, list=list),
                icon = icon ,
                extra_info = True ,
            )}
            % endfor
            
        </div>
    </div>
    
    ## Left col
    <div class="frag_col frag_left_col short">
        ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ## this class attributes in this section are rather important; rather
        ## than being used for CSS, they are part of the hCard standard, they
        ## need to stay the same in order for search engines to recognise the
        ## current page as being a person or organisation's profile
        ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        <div class="frag_col hideable hide_if_nojs vcard">
            <div class="user-details">
                
                <span class="name fn" style="display: none;">${h.guess_hcard_name(self.member['name'])}</span>
                <span class="detail-title">${_('Username')}:</span> <span class="uid nickname">${self.member['username']}</span><br />
                % if self.member.get('website'):
                    <span class="detail-title">${_('Website')}:</span> <a href="${self.member['website']}" class="url" target="_blank">${h.nicen_url(self.member['website'])}</a><br />
                % endif
                % if self.member.get('google_profile'):
                    <span class="detail-title">${_('Google Profile')}:</span> <a href="${self.member['google_profile']}" rel="me" target="_blank">${self.member['name']}</a><br />
                % endif
                <span class="detail-title">Joined:</span> ${_('%s ago') % h.time_ago(self.member['join_date'])  }<br />
                % if self.current_user:
                    <span class="detail-title">${_('Type')}:</span> ${_('_' + self.member['account_type']).capitalize()}
                % endif
                
                <br />
                <%
                    groups = d['groups']['items']
                    if len(groups) == 0:
                        _type = "_"+d['member']['type'].capitalize()
                        role = _(_type)
                        org  = "Civicboom"
                    elif len(groups) == 1:
                        role = groups[0]['role'].capitalize()
                        org = groups[0]['name'] or groups[0]['username']
                    else:
                        role = "Contributor"
                        org = _("%s groups") % len(groups)
                %>
                
                <span class="org"><span class="value-title" title="${org}"></span></span>
                <span class="role"><span class="value-title" title="${role}"></span></span>
                
                % if self.member['type'] == "group" and self.member['location_home']:
                    <% lon, lat = self.member['location_home'].split() %>
                    <span class="geo">
                        <span class="latitude"><span class="value-title" title="${lat}"></span></span>
                        <span class="longitude"><span class="value-title" title="${lon}"></span></span>
                    </span>
                % endif
                
                % if 'follow' in self.actions:
                    ${h.secure_link(
                        h.args_to_tuple('member_action', action='follow'    , id=self.id, format='redirect') ,
                        value           = _('Follow') ,
                        link_class = 'button button_large',
                        title           = _("Follow %s" % self.name) ,
                    )}
                    <span class="separtor"></span>
                % endif
                
                % if 'unfollow' in self.actions:
                    ${h.secure_link(
                        h.args_to_tuple('member_action', action='unfollow'  , id=self.id, format='redirect') ,
                        value           = _('Unfollow') if 'follow' not in self.actions else _('Ignore invite') ,
                        link_class = 'button button_large',
                        title           = _("Stop following %s" % self.name) if 'follow' not in self.actions else _('Ignore invite from %s' % self.name) ,
                    )}
                    <span class="separtor"></span>
                % endif
            </div>
        </div>
        
        ## Community ----------------------------------------
        % if self.num_unread_messages != None and self.num_unread_notifications != None:
            ${messages_frag_list()}
        % endif
        
        ${frag_list.member_list_thumbnails(
            d['following'],
            _('Following'),
            icon =  'follow'
        )}
        
        <%def name="invite_members_trusted()">
            ${invite_members(
               title='Invite Trusted Followers',
               href_tuple=h.args_to_tuple(controller='invite', action='index', id='me', invite='trusted_follower'),
               help_text=_('Invite other members to become trusted followers'),
               help_classes='mo-help-r mo-help-b'
            )}
        </%def>
    
        ${frag_list.member_list_thumbnails(
            d['followers'] ,
            _('Followers') ,
            icon    = 'follow',
            actions = invite_members_trusted if 'invite_trusted_followers' in self.actions else None ,
        )}
        
        ${frag_list.member_list_thumbnails(
            [m for m in d['groups']['items'] if m['status']=='active'],
            _('My _Groups') ,
            h.args_to_tuple('member_action', id=self.id, action='groups') ,
            icon    = 'group' ,
        )}
        
        ${frag_list.member_list_thumbnails(
            [m for m in d['groups']['items'] if m['status']=='invite'] ,
            _('Pending group invitations') ,
            h.args_to_tuple('member_action', id=self.id, action='groups') ,
            icon = 'group' ,
        )}
        
        % if self.member['type']=='group':
        <%def name="invite_members_group()">
            ${invite_members(
               title='Invite Members to join',
               href_tuple=h.args_to_tuple(controller='invite', action='index', id='me', invite='group'),
               help_text=_('Invite other members to join this _Group'),
               help_classes='mo-help-r mo-help-b'
            )}
        </%def>
        
        ${frag_list.member_list_thumbnails(
            [m for m in d['members']['items'] if m['status']=='active'],
            _('Members'),
            h.args_to_tuple('member_action', id=self.id, action='members') ,
            icon = 'user' ,
            actions = invite_members_group if 'invite_members' in self.actions else None ,
        )}
        
        ${frag_list.member_list_thumbnails(
            [m for m in d['members']['items'] if m['status']=='invite'],
            _('Invited Members'),
            h.args_to_tuple('member_action', id=self.id, action='members') ,
            icon = 'invite' ,
        )}
    
        % endif
        
        ${member_map()}
    </div>
    
    ## Right col
    <div class="frag_col frag_right_col long">
        ${guides()}
        
        <%doc>
        ## AllanC - display removed because users have drafts created and dont need it pushed to them twice.
        ## Accepted Assignments --------------------------------------
        ${frag_list.content_list(
            d['assignments_accepted'] ,
            _('My to-do'), #_('Accepted _assignments') ,
            h.args_to_tuple('member_action', id=self.id, action='assignments_accepted') ,
            creator = True ,
            icon = 'assignment' ,
            extra_info = True ,
        )}
        </%doc>
        
        ## Memers Content --------------------------------------------
        % for list, icon, description in [n for n in self.trans_strings if n[0] not in ["all","assignments_active" ]]:
        ${frag_list.content_list(
            d[list] ,
            description ,
            #h.args_to_tuple('contents', creator=self.id, list=list), # AllanC - this is no longer needed as the kwargs are provided in the api_list output
            icon = icon ,
            extra_info = True ,
        )}
        % endfor
        
        
        ## Boomed Content --------------------------------------------
        ${frag_list.content_list(
            d['boomed'],
            _('Boomed _content'),
            #h.args_to_tuple('member_action', id=self.id, action='boomed') , 
            #h.args_to_tuple('contents', boomed_by=self.id) , # AllanC - list kwargs are now in API output, so this manual url generating is not needed anymore
            creator = True ,
            icon = 'boom' ,
            extra_info = True ,
        )}
    </div>
</%def>

##------------------------------------------------------------------------------
## Guides
##------------------------------------------------------------------------------
<%def name="guides()">
    <% guide_count = 1 %>
    
    ## Hub/widget hybrid advert
    % if "advert_hand_hub" in self.adverts_hand and not c.logged_in_user.config["advert_hand_hub"]:
        ${components.guidance(
            contents=[self.guidance_content['hub'], self.guidance_content['widget']],
            int=guide_count,
            heading="What next?",
            config_key="advert_hand_hub"
        )}
        <% guide_count += 1 %>
    % endif
    
    ## Request advert
    % if "advert_hand_assignment" in self.adverts_hand and not c.logged_in_user.config["advert_hand_assignment"]:
        ${components.guidance(
            contents=[self.guidance_content['assignment']],
            int=guide_count,
            heading="What next?",
            config_key="advert_hand_assignment"
        )}
        <% guide_count += 1 %>
    % endif
    
    ## Content advert
    % if "advert_hand_content" in self.adverts_hand and not c.logged_in_user.config["advert_hand_content"]:
        ${components.guidance(
            contents=[self.guidance_content["assignment"], self.guidance_content["article"]],
            int=guide_count,
            config_key="advert_hand_content"
        )}
        <% guide_count += 1 %>
    % endif
    
    ## Response advert
    % if "advert_hand_response" in self.adverts_hand and not c.logged_in_user.config["advert_hand_response"]:
        ${components.guidance(
            contents=[self.guidance_content["response"]],
            int=guide_count,
            heading=_("What next?"),
            config_key="advert_hand_response"
        )}
        <% guide_count += 1 %>
    % endif

    ## Widget advert
    % if "advert_hand_widget" in self.adverts_hand and not c.logged_in_user.config["advert_hand_widget"]:
        ${components.guidance(
            contents=[self.guidance_content['widget']],
            int=guide_count,
            config_key="advert_hand_widget"
        )}
        <% guide_count += 1 %>
    % endif
    
    ## Mobile advert
    % if "advert_hand_mobile" in self.adverts_hand and not c.logged_in_user.config["advert_hand_mobile"]:
        ${components.guidance(
            contents=[self.guidance_content['mobile']],
            config_key="advert_hand_mobile",
            int=guide_count,
        )}
        <% guide_count += 1 %>
    % endif
</%def>
    
##------------------------------------------------------------------------------
## Messages Frag List
##------------------------------------------------------------------------------
<%def name="messages_frag_list()">
    <div class="frag_list">
        <h2>${_('Messages')}</h2>
        <div class="frag_list_contents">
            <div class="content">
                <ul>
                    <li>
                        <a class="link_new_frag"
                            data-frag="${h.url('messages', list='to', format='frag')}"
                            href="${h.url('messages', list='to')}">
                            <div style="float:left; width: 4em;">
                                <span class="icon16 i_message"     ></span>
                                <div class="icon_overlay_red"
                                    % if self.num_unread_messages == 0:
                                        style="display:none"
                                    % endif
                                >&nbsp;${self.num_unread_messages}&nbsp;</div>
                            </div>${_('Inbox')}
                        </a>
                    </li>
                    <li>
                        <a class="link_new_frag"
                            data-frag="${h.url('messages', list='sent', format='frag')}"
                            href="${h.url('messages', list='sent')}">
                            <div style="float:left; width: 4em;">
                                <span class="icon16 i_message_sent"></span>
                            </div>${_('Sent')}
                        </a>
                    </li>
                    <li>
                        <a class="link_new_frag"
                            data-frag="${h.url('messages', list='notification', format='frag')}"
                            href="${h.url('messages', list='notification')}">
                            <div style="float:left; width: 4em;">
                                <span class="icon16 i_notification"></span>
                                <div class="icon_overlay_red"
                                    % if self.num_unread_notifications == 0:
                                        style="display:none"
                                    % endif
                                >&nbsp;${self.num_unread_notifications}&nbsp;</div>
                            </div>${_('Notifications')}
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
    </%def>

##------------------------------------------------------------------------------
## Actions
##------------------------------------------------------------------------------

<%def name="actions_buttons()">
    ##% if c.logged_in_persona and c.logged_in_persona.username != member['username']:
    ##    % if c.logged_in_persona and c.logged_in_persona.is_following(member['username']):
        ##${h.secure_link(url('member_action', action='unfollow', id=member['username'], format='redirect'), _(' '), title=_("Stop following %s" % member['username']), css_class="follow_action icon16 i_unfollow")}
        ##% else:  
        ##% endif
    ##% endif

    % if 'follow' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('member_action', action='follow'    , id=self.id, format='redirect') ,
            value           = _('Follow') ,
            link_class       = "button" ,
            #value_formatted = h.literal("<span class='button '>%s</span>") % _('Follow'),
            title           = _("Follow %s" % self.name) ,
            #json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif

    % if 'unfollow' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('member_action', action='unfollow'  , id=self.id, format='redirect') ,
            value           = _('Stop Following') if 'follow' not in self.actions else _('Ignore invite') ,
            #value_formatted = h.literal("<span class='button'>%s</span>") % _('Stop Following'),
            link_class       = "button" ,
            title           = _("Stop following %s" % self.name) if 'follow' not in self.actions else _('Ignore invite from %s' % self.name) ,
            #json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
    
    % if 'join' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('group_action', action='join'       , id=self.id, member=c.logged_in_persona.username, format='redirect') ,
            value           = _('Join _group') ,
            link_class       = "button" ,
            #value_formatted = h.literal("<span class='button'>%s</span>") % _('Join _Group'),
            #json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
    
    ## AllanC - same as above, could be neater but works
    % if 'join_request' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('group_action', action='join'       , id=self.id, member=c.logged_in_persona.username, format='redirect') ,
            value           = _('Request to join _group') ,
            link_class       = "button" ,
            #value_formatted = h.literal("<span class='button'>%s</span>") % _('Request to join _group'),
            #json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
    
    % if 'invite' in self.actions: #and c.logged_in_persona and c.logged_in_persona.__type__=='group':
        <% invite_text = _('Invite %s to join %s' % (self.name, c.logged_in_persona.name or c.logged_in_persona.username)) %>
        ${h.secure_link(
            h.args_to_tuple('group_action', action='invite'     , id=c.logged_in_persona.username, member=self.id, format='redirect') ,
            value           = _('Invite to _Group') ,
            link_class       = "button" ,
            #value_formatted = h.literal("<span class='button'>%s</span>") % _('Invite') ,
            title           = invite_text , 
            #json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
    
    ## GregM: Addition of follower actions
    % if 'follower_invite_trusted' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('member_action', action='follower_invite_trusted'  , id=self.id, format='redirect') ,
            value           = _('Invite trusted') ,
            link_class       = "button" ,
            #value_formatted = h.literal("<span class='button'>%s</span>") % _('Invite trusted'),
            title           = _("Invite %s as a trusted follower" % self.name) ,
            #json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
    
    % if 'follower_trust' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('member_action', action='follower_trust'  , id=self.id, format='redirect') ,
            value           = _('Trust') ,
            link_class       = "button" ,
            #value_formatted = h.literal("<span class='button'>%s</span>") % _('Trust'),
            title           = _("Trust follower %s" % self.name) ,
            #json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % elif 'follower_distrust' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('member_action', action='follower_distrust'  , id=self.id, format='redirect') ,
            value           = _('Distrust') ,
            link_class       = "button" ,
            #value_formatted = h.literal("<span class='button'>%s</span>") % _('Distrust'),
            title           = _("Distrust follower %s" % self.name) ,
            #json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
    
    % if 'push_assignment' in self.actions and self.member.get('push_assignment'):
        ${h.secure_link(
            h.url('new_content', target_type='article', parent_id=self.member['push_assignment']),
            value           = _("Send us your _stories") ,
            link_class      = "button" ,
            title           = _("Got _content? Send us _content directly") ,
        )}
    % endif
</%def>


<%def name="actions_common()">
    
    % if self.member.get('location_current') or self.member.get('location_home'):
        ##${parent.georss_link()}
    % endif
</%def>



##------------------------------------------------------------------------------
## Avatar
##------------------------------------------------------------------------------
<%def name="member_avatar(img_class='')">
    ${member_includes.avatar(self.member, class_='thumbnail_large', img_class=img_class, as_link=False)}
</%def>



##------------------------------------------------------------------------------
## Map
##------------------------------------------------------------------------------
<%def name="member_map()">
    ##<p>implement map</p>
</%def>


##------------------------------------------------------------------------------
## Share
##------------------------------------------------------------------------------
<%doc>
        ${share.share(
            url         = url('member', id=d['member']['username'], host=app_globals.site_host, protocol='http'),
            title       = _('%s on _site_name' % d['member']['name']) ,
            description = d['member'].get('description') or '' ,
        )}
        
        ##<a href='${url('member', id=d['member']['username'], format='rss')}' title='RSS for ${d['member']['username']}' class="icon16 i_rss"  ><span>RSS</span></a>
        <a href='${url.current(format='rss')}' title='RSS' class="icon16 i_rss"><span>RSS</span></a>
        <a href='' onclick="cb_frag_remove($(this)); return false;" title='${_('Close')}' class="icon16 i_close"><span>${_('Close')}</span></a>
    </div>
</%doc>
