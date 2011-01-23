<%inherit file="/frag/common/frag.mako"/>

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
                self.attr.title     = _('Current Group Persona')
                self.attr.icon_type = 'group'
            else:
                self.attr.title     = _('Current User')
                self.attr.icon_type = 'current_user'
            
            self.attr.share_kwargs.update({
                'url'  : h.url('member', id=self.id, host=app_globals.site_host, protocol='http') ,
            })
        
        self.attr.frag_data_css_class = 'frag_member'
        
        self.attr.rss_url = url('contents', creator=self.id, format='rss')
        
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
		<h1>${self.member['name']} (${self.member['username']})</h1>
        <br>${member_avatar()}
        
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
            _('Groups') ,
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
            <a class   = "icon icon_message"
               href    = "${url('messages',list='to')}"
               title   = "${_('Messages')}"
               onclick = "cb_frag($(this), '${url('messages', list='to'          , format='frag')}', 'bridge'); return false;"
            ><span>${_('Messages')}</span></a>
    
            <a class   = "icon icon_message"
               href    = "${url('messages',list='sent')}"
               title   = "${_('Messages Sent')}"
               onclick = "cb_frag($(this), '${url('messages', list='sent'        , format='frag')}', 'bridge'); return false;"
            ><span>${_('Messages')}</span></a>
            
            <a class   = "icon icon_notification"
               href    = "${url('messages', list='notification')}"
               title   = "${_('Notifications')}"
               onclick = "cb_frag($(this), '${url('messages', list='notification', format='frag')}', 'bridge'); return false;"
            ><span>${_('Notifications')}</span></a>
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
        
        % for list, icon in app_globals.contents_list_names.iteritems():
            ${frag_list.content_list(
                d[list] ,
                list ,
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
            value_formatted = h.literal("<span class='icon icon_join'></span>%s") % _('Join Group'),
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
        ${popup.link(h.args_to_tuple('new_message', target=self.id), title=_('Send message') , class_='icon icon_message')}
    % endif
    % if 'settings' in self.actions:
        <a class="icon icon_settings" href="${url('settings')}" title="${_('Settings')}"><span>${_('Settings')}</span></a>
    % endif
    ${popup.link(h.args_to_tuple(controller='misc', action='get_widget', id=self.id), title=_('Get widget'), class_='icon icon_widget')}
    
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

