_<%inherit file="/frag/common/frag.mako"/>

<%!
    import civicboom.lib.constants as constants
    rss_url = True
%>

<%namespace name="frag_list"       file="/frag/common/frag_lists.mako"/>
<%namespace name="member_includes" file="/html/web/common/member.mako"     />
<%namespace name="popup"           file="/html/web/common/popup_base.mako" />

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%def name="init_vars()">
    <%
        self.member    = d['member']
        self.id        = self.member['username']
        self.name      = self.member.get('name') or self.member.get('username')
        self.actions   = d.get('actions', [])
        
        self.num_unread_messages = d.get('num_unread_messages', 0);
        self.num_unread_notifications = d.get('num_unread_notifications', 0);
        
        self.attr.title     = self.member['type'].capitalize()
        self.attr.icon_type = self.member['type']
        
        self.current_user = c.logged_in_persona and self.member['username'] == c.logged_in_persona.username

        self.attr.share_kwargs = {
            'url'      : self.attr.html_url ,
            'title'    : self.name ,
            'image'    : self.member['avatar_url'] ,
        }
        
        if self.current_user:
            if self.member['type'] == 'group':
                self.attr.title     = _('Current _Group Persona')
                self.attr.icon_type = 'group'
                self.attr.help_frag = 'group_persona'
            else:
                self.attr.title     = _('Current User')
                self.attr.icon_type = 'current_user'
                self.attr.help_frag = 'profile'
            
            self.attr.share_kwargs.update({
                'url'  : h.url('member', id=self.id, protocol='http', subdomain='') ,
            })
            self.attr.rss_url = h.url('formatted_member', id=self.id, format='rss', subdomain='')
        
        self.attr.frag_data_css_class = 'frag_member'
        
        # Contents index was sorted by date. it was awkward to get a single list from the multiple lists of a member object
        #  but shish said that clients will sort the RSS by date so it was all ok
        #self.attr.rss_url = url('contents', creator=self.id, format='rss')
        
        self.attr.auto_georss_link = True
    %>
</%def>

##------------------------------------------------------------------------------
## Member Fragment
##------------------------------------------------------------------------------
<%def name="body()">
    
    <div class="frag_left_col">
        <div class="frag_col">
        ## Member Details
		<h1>${self.member['name'] or self.member['username']}</h1><br />
        <div>
          <span style="float:left; padding-right: 3px;">${member_avatar()}</span>
          <div style="padding-left: 92px" >
            % if self.member.get('website'):
              ${_('Website')}: <br /><a href="${self.member['website']}" target="_blank">${self.member['website']}</a><br />
            % endif
            Joined: ${self.member['join_date']}<br />
            % if self.current_user:
              ${_('Type')}: ${self.member['account_type'].capitalize()}
            % endif
            <br />
            % if 'follow' in self.actions:
                ${h.secure_link(
                    h.args_to_tuple('member_action', action='follow'    , id=self.id, format='redirect') ,
                    value           = _('Follow') ,
                    css_class = 'button button_large',
                    title           = _("Follow %s" % self.name) ,
                    json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
                )}
                <span class="separtor"></span>
            % elif 'unfollow' in self.actions:
                ${h.secure_link(
                    h.args_to_tuple('member_action', action='unfollow'  , id=self.id, format='redirect') ,
                    value           = _('Unfollow') ,
                    css_class = 'button button_large',
                    title           = _("Stop following %s" % self.name) ,
                    json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
                )}
                <span class="separtor"></span>
            % endif
              
          </div>
        </div>
        <div style="clear: both;"></div>
        % if self.member.get('description'):
          <div style="clear:left; height: 3px;">&nbsp;</div>
          <div style="clear:left;" class="frag_list">
            <h2><span class="icon icon_${self.attr.icon_type}"><span>description</span><div style="display:inline-block;padding-left:19px">Description</div></span></h2>
            <div class="frag_list_contents">
              <div class="content" style="padding-bottom: 3px;">
                ${self.member['description']}
              </div>
            </div>
          </div>
        % endif
        ## Comunity ----------------------------------------
        
        ${frag_list.member_list_thumbnails(
            d['following'],
            _('Following'),
            #h.args_to_tuple('member_action', id=self.id, action='following'),
            h.args_to_tuple('members', followed_by=self.id),
            icon =  'follow'
        )}
        ${frag_list.member_list_thumbnails(
            d['followers'] ,
            _('Followers') ,
            #h.args_to_tuple('member_action', id=self.id, action='followers') ,
            h.args_to_tuple('members', follower_of=self.id),
            icon =  'follow'
        )}
        
        ${frag_list.member_list_thumbnails(
            [m for m in d['groups']['items'] if m['status']=='active'],
            _('_Groups') ,
            h.args_to_tuple('member_action', id=self.id, action='groups') ,
            icon = 'group' ,
        )}
        
        ${frag_list.member_list_thumbnails(
            [m for m in d['groups']['items'] if m['status']=='invite'] ,
            _('Pending group invitations') ,
            h.args_to_tuple('member_action', id=self.id, action='groups') ,
            icon = 'group' ,
        )}
        
        % if self.member['type']=='group':
        ${frag_list.member_list_thumbnails(
            [m for m in d['members']['items'] if m['status']=='active'],
            _('Members'),
            h.args_to_tuple('member_action', id=self.id, action='members') ,
            icon = 'user' ,
            
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
    </div>
    
    <div class="frag_right_col">
        <div class="frag_col">
        
        % if self.current_user:
        <div style="float: right; width: 66%; text-align: center;">
          <%def name="messageIcon(messages)">
            % if messages > 0:
              <div class="icon_overlay_red">&nbsp;${messages}&nbsp;</div>
            % endif
          </%def>
          <a style="text-align:left; float:left;" class   = "icon_large icon_messages_large"
             href    = "${h.url('messages',list='to')}"
             title   = "${_('Messages')}"
             onclick = "cb_frag($(this), '${h.url('messages', list='to'          , format='frag')}', 'frag_col_1'); return false;"
          ><span>${_('Messages')}</span>
          ${messageIcon(self.num_unread_messages)}
          </a>
          <a class   = "icon_large icon_messagesent_large"
             href    = "${h.url('messages',list='sent')}"
             title   = "${_('Messages Sent')}"
             onclick = "cb_frag($(this), '${h.url('messages', list='sent'        , format='frag')}', 'frag_col_1'); return false;"
          ><span>${_('Messages')}</span></a>
          <a style="text-align:left; float:right;" class   = "icon_large icon_notifications_large"
             href    = "${h.url('messages', list='notification')}"
             title   = "${_('Notifications')}"
             onclick = "cb_frag($(this), '${h.url('messages', list='notification', format='frag')}', 'frag_col_1'); return false;"
          ><span>${_('Notifications')}</span>
          ${messageIcon(self.num_unread_notifications)}
          </a>
        </div>
        <div style="clear: both; width: 100%; height: 0;"></div>
        % endif
        
        
        
        ## Accepted Assignments --------------------------------------
        
        ${frag_list.content_list(
            d['assignments_accepted'] ,
            _('Accepted _assignments') ,
            h.args_to_tuple('member_action', id=self.id, action='assignments_accepted') ,
            creator = True ,
            icon = 'assignment' ,
        )}
        
        
        ## Memers Content --------------------------------------------
        
        % for list, icon, decription in constants.contents_list_titles:
            ${frag_list.content_list(
                d[list] ,
                decription ,
                h.args_to_tuple('contents', creator=self.id, list=list), 
                icon = icon ,
            )}
        % endfor
        
        
        ## Boomed Content --------------------------------------------
        
        ${frag_list.content_list(
            d['boomed_content'],
            _('Boomed content'),
            #h.args_to_tuple('member_action', id=self.id, action='boomed_content') ,
            h.args_to_tuple('contents', boomed_by=self.id) ,
            creator = True ,
            icon = 'boom' ,
        )}
        
        </div>
    </div>

</%def>


##------------------------------------------------------------------------------
## Actions
##------------------------------------------------------------------------------

<%def name="actions_specific()">
    ##% if c.logged_in_persona and c.logged_in_persona.username != member['username']:
    ##    % if c.logged_in_persona and c.logged_in_persona.is_following(member['username']):
        ##${h.secure_link(url('member_action', action='unfollow', id=member['username'], format='redirect'), _(' '), title=_("Stop following %s" % member['username']), css_class="follow_action icon icon_unfollow")}
        ##% else:  
        ##% endif
    ##% endif

    % if 'follow' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('member_action', action='follow'    , id=self.id, format='redirect') ,
            value           = _('Follow') ,
            value_formatted = h.literal("<span class='icon icon_follow'></span>%s") % _('Follow'),
            title           = _("Follow %s" % self.name) ,
            json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif

    % if 'unfollow' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('member_action', action='unfollow'  , id=self.id, format='redirect') ,
            value           = _('Unfollow') ,
            value_formatted = h.literal("<span class='icon icon_unfollow'></span>%s") % _('Stop Following'),
            title           = _("Stop following %s" % self.name) ,
            json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif

    % if 'join' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('group_action', action='join'       , id=self.id, member=c.logged_in_persona.username, format='redirect') ,
            value           = _('Join _group') ,
            value_formatted = h.literal("<span class='icon icon_join'></span>%s") % _('Join _Group'),
            json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
    
    % if 'invite' in self.actions: #and c.logged_in_persona and c.logged_in_persona.__type__=='group':
        <% invite_text = _('Invite %s to join %s' % (self.name, c.logged_in_persona.name or c.logged_in_persona.username)) %>
        ${h.secure_link(
            h.args_to_tuple('group_action', action='invite'     , id=c.logged_in_persona.username, member=self.id, format='redirect') ,
            value           = _('Invite') ,
            value_formatted = h.literal("<span class='icon icon_invite'></span>%s") % _('Invite') ,
            title           = invite_text , 
            json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
</%def>


<%def name="actions_common()">
    % if 'message' in self.actions:
        ${popup.link(
            h.args_to_tuple('new_message', target=self.id),
            title = _('Send Message'),
            text  = h.literal("<span class='icon icon_message'></span>%s") % _('Send Message'),
        )}
        <span class="separtor"></span>
    % endif
    
    % if 'settings_group' in self.actions:
        <a href="${h.url('edit_group', id=self.id)}" title="${_('_group Settings').capitalize()}"><span class="icon icon_group"></span>${_('_group Settings').capitalize()}</a>
        <span class="separtor"></span>
    % endif
    
    % if 'settings' in self.actions:
        <a href="${h.url('settings')}" title="${_('Settings')}"><span class="icon icon_settings"></span>${_('Settings')}</a>
        <span class="separtor"></span>
    % endif
    
    ${popup.link(
        h.args_to_tuple(controller='misc', action='get_widget', id=self.id),
        title = _('Get widget'),
        text  = h.literal("<span class='icon icon_widget'></span>%s") % _('Get widget'),
    )}
    
    % if self.member.get('location_current') or self.member.get('location_home'):
        ${parent.georss_link()}
    % endif
</%def>



##------------------------------------------------------------------------------
## Avatar
##------------------------------------------------------------------------------
<%def name="member_avatar()">
    ${member_includes.avatar(self.member, class_='thumbnail_large')}
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
        
        ##<a href='${url('formatted_member', id=d['member']['username'], format='rss')}' title='RSS for ${d['member']['username']}' class="icon icon_rss"  ><span>RSS</span></a>
        <a href='${url.current(format='rss')}' title='RSS' class="icon icon_rss"><span>RSS</span></a>
        <a href='' onclick="cb_frag_remove($(this)); return false;" title='${_('Close')}' class="icon icon_close"><span>${_('Close')}</span></a>
    </div>
</%doc>

