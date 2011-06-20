<%inherit file="/frag/common/frag.mako"/>

<%!
    import civicboom.lib.constants as constants
    rss_url = True
%>

<%namespace name="frag_list"       file="/frag/common/frag_lists.mako"/>
<%namespace name="member_includes" file="/html/web/common/member.mako"     />
<%namespace name="popup"           file="/html/web/common/popup_base.mako" />
<%namespace name="share"           file="/frag/common/share.mako"          />

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%def name="custom_share()">
    <a href="#" onclick="${share.janrain_social_call_member(self.member, 'new_'+self.member['type']) | n }; return false;" class="icon16 i_share"><span>Janrain</span></a>
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
            'custom_share_line' : custom_share_line,
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
    %>
</%def>

##------------------------------------------------------------------------------
## Member Fragment
##------------------------------------------------------------------------------
<%def name="body()">
    ## AllanC!?! (c.logged_in_persona.username or c.logged_in_user.username) this is a meaninless statement because or returns one or the other? logged_in_persona always not null if logged_in_user
	% if c.logged_in_persona and c.logged_in_persona.username == self.member['username'] and request.params.get('prompt_aggregate')=='True':
	<script>
		${share.janrain_social_call_member(self.member, 'new_'+self.member['type']) | n }
	</script>
	% endif
	
    ## Top row (avatar/about me)
    <div class="frag_top_row">
	<div  class="about_me">
	    <div class="content">
		<div class="avatar">${member_avatar(img_class='photo')}</div>
		<h2 class="fn n">${h.guess_hcard_name(self.member['name'])}</h2>
		% if self.member.get('description'):
		    <div>${h.truncate(self.member['description'], length=500, whole_word=True, indicator='...')}</div>
		% endif
	    </div>
	    <div style="clear: both;"></div>
	    ${actions_buttons()}
	    % if 'message' in self.actions:
		${popup.link(
		    h.args_to_tuple('new_message', target=self.id),
		    title = _('Send Message'),
		    text  = h.literal("<div class='button' style='float: right; margin: 0;'>%s</div>") % _('Send Message'),
		)}
		## <span class="separtor"></span>
	    % endif
	    <div style="clear: both;"></div>
	</div>
	% for list, icon, description in [n for n in constants.contents_list_titles if n[0]  in ["assignments_active"]]:
	    ${frag_list.content_list(
		d[list] ,
		description ,
		h.args_to_tuple('contents', creator=self.id, list=list),
		icon = icon ,
		extra_info = True ,
	    )}
	% endfor
    </div>
    
    ## Left col
    <div class="frag_left_col">
	<div class="frag_col">
	    <%doc><div class="frag_col vcard">
		<div class="user-details">
		    <span class="detail-title">${_('Username')}:</span> <span class="uid nickname">${self.member['username']}</span><br />
		    % if self.member.get('website'):
		      <span class="detail-title">${_('Website')}:</span> <a href="${self.member['website']}" class="url" target="_blank">${self.member['website']}</a><br />
		    % endif
		    <span class="detail-title">Joined:</span> ${_('%s ago') % h.time_ago(self.member['join_date'])  }<br />
		    % if self.current_user:
		      <span class="detail-title">${_('Type')}:</span> ${_('_' + self.member['account_type']).capitalize()}
		    % endif
		    <br />
		    <%
		    groups = d['groups']['items']
		    if len(groups) == 0:
			role = _("_"+d['member']['type'].capitalize())
			org = "Civicboom"
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
			<%
			lon, lat = self.member['location_home'].split()
			%>
			<span class="geo">
				<span class="latitude"><span class="value-title" title="${lat}"></span></span>
				<span class="longitude"><span class="value-title" title="${lon}"></span></span>
			</span>
		    % endif
		    % if 'follow' in self.actions:
			${h.secure_link(
			    h.args_to_tuple('member_action', action='follow'    , id=self.id, format='redirect') ,
			    value           = _('Follow') ,
			    css_class = 'button button_large',
			    title           = _("Follow %s" % self.name) ,
			    json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
			)}
			<span class="separtor"></span>
		    % endif
		    % if 'unfollow' in self.actions:
			${h.secure_link(
			    h.args_to_tuple('member_action', action='unfollow'  , id=self.id, format='redirect') ,
			    value           = _('Unfollow') if 'follow' not in self.actions else _('Ignore invite') ,
			    css_class = 'button button_large',
			    title           = _("Stop following %s" % self.name) if 'follow' not in self.actions else _('Ignore invite from %s' % self.name) ,
			    json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
			)}
			<span class="separtor"></span>
		    % endif
		</div>
	    </div>
	    <div style="clear: both;"></div></%doc>
	    ## Community ----------------------------------------
	    
	${share.AddThisFragList(**self.attr.share_kwargs)}
	
	% if self.num_unread_messages != None and self.num_unread_notifications != None:
    	${messages_frag_list()}
    % endif
	
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
	    icon    = 'follow',
	    actions = h.frag_link(value='', title='Invite Trusted Followers', class_='icon16 i_invite', href_tuple=h.args_to_tuple(controller='invite', action='index', id='me', invite='trusted_follower')) if 'invite_trusted_followers' in self.actions else None ,
	)}
	
	${frag_list.member_list_thumbnails(
	    [m for m in d['groups']['items'] if m['status']=='active'],
	    _('_Groups') ,
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
	${frag_list.member_list_thumbnails(
	    [m for m in d['members']['items'] if m['status']=='active'],
	    _('Members'),
	    h.args_to_tuple('member_action', id=self.id, action='members') ,
	    icon = 'user' ,
	    actions = h.frag_link(value='', title='Invite Members', class_='icon16 i_invite', href_tuple=h.args_to_tuple(controller='invite', action='index', id='me', invite='group')) if 'invite_members' in self.actions else None ,
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
    
    ## Right col
    <div class="frag_right_col">
	    <div class="frag_col">
	    
	    <%doc> ## Messages/notification icons
	    % if self.current_user:
	    <div style="float: right; width: 66%; text-align: center;">
	      <%def name="messageIcon(messages)">
		% if messages > 0:
		  <div class="icon_overlay_red">&nbsp;${messages}&nbsp;</div>
		% endif
	      </%def>
	      <a style="text-align:left; float:left;" class   = "icon32 i_message"
		 href    = "${h.url('messages',list='to')}"
		 title   = "${_('Messages')}"
		 onclick = "cb_frag($(this), '${h.url('messages', list='to'          , format='frag')}', 'frag_col_1'); return false;"
	      ><span>${_('Messages')}</span>
	      ${messageIcon(self.num_unread_messages)}
	      </a>
	      <a class   = "icon32 i_message_sent"
		 href    = "${h.url('messages',list='sent')}"
		 title   = "${_('Messages Sent')}"
		 onclick = "cb_frag($(this), '${h.url('messages', list='sent'        , format='frag')}', 'frag_col_1'); return false;"
	      ><span>${_('Messages')}</span></a>
	      <a style="text-align:left; float:right;" class   = "icon32 i_notification"
		 href    = "${h.url('messages', list='notification')}"
		 title   = "${_('Notifications')}"
		 onclick = "cb_frag($(this), '${h.url('messages', list='notification', format='frag')}', 'frag_col_1'); return false;"
	      ><span>${_('Notifications')}</span>
	      ${messageIcon(self.num_unread_notifications)}
	      </a>
	    </div>
	    <div style="clear: both; width: 100%; height: 0;"></div>
	    % endif
	    </%doc>
	    
	    
	    ## Accepted Assignments --------------------------------------
	    
	    ${frag_list.content_list(
		d['assignments_accepted'] ,
		_('My to-do'), #_('Accepted _assignments') ,
		h.args_to_tuple('member_action', id=self.id, action='assignments_accepted') ,
		creator = True ,
		icon = 'assignment' ,
		extra_info = True ,
	    )}
	    
	    
	    ## Memers Content --------------------------------------------
	    
	    % for list, icon, description in [n for n in constants.contents_list_titles if n[0] not in ["all","assignments_active" ]]:
		${frag_list.content_list(
		    d[list] ,
		    description ,
		    h.args_to_tuple('contents', creator=self.id, list=list),
		    icon = icon ,
		    extra_info = True ,
		)}
	    % endfor
	    
	    
	    ## Boomed Content --------------------------------------------
	    
	    ${frag_list.content_list(
		d['boomed'],
		_('Boomed _content'),
		#h.args_to_tuple('member_action', id=self.id, action='boomed') ,
		h.args_to_tuple('contents', boomed_by=self.id) ,
		creator = True ,
		icon = 'boom' ,
		extra_info = True ,
	    )}
	    
	    </div>
	</div>

</%def>

##------------------------------------------------------------------------------
## Messages Frag List
##------------------------------------------------------------------------------
<%def name="messages_frag_list()">
    <div class="frag_list">
        <h2>${_('Messages')}</h2>
        <div class="frag_list_contents">
            <div class="content note">
                <span class="icon16 i_inbox"></span> ${self.num_unread_messages}
                <span class="icon16 i_sent" ></span>
                <span class="icon16 i_notifications"></span> ${self.num_unread_notifications}
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
            value_formatted = h.literal("<span class='button '>%s</span>") % _('Follow'),
            title           = _("Follow %s" % self.name) ,
            json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif

    % if 'unfollow' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('member_action', action='unfollow'  , id=self.id, format='redirect') ,
            value           = _('Unfollow') if 'follow' not in self.actions else _('Ignore invite') ,
            value_formatted = h.literal("<span class='button'>%s</span>") % _('Stop Following'),
            title           = _("Stop following %s" % self.name) if 'follow' not in self.actions else _('Ignore invite from %s' % self.name) ,
            json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
    
    % if 'join' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('group_action', action='join'       , id=self.id, member=c.logged_in_persona.username, format='redirect') ,
            value           = _('Join _group') ,
            value_formatted = h.literal("<span class='button'>%s</span>") % _('Join _Group'),
            json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
    
    ## AllanC - same as above, could be neater but works
    % if 'join_request' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('group_action', action='join'       , id=self.id, member=c.logged_in_persona.username, format='redirect') ,
            value           = _('Request to join _group') ,
            value_formatted = h.literal("<span class='button'>%s</span>") % _('Request to join _group'),
            json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
    
    % if 'invite' in self.actions: #and c.logged_in_persona and c.logged_in_persona.__type__=='group':
        <% invite_text = _('Invite %s to join %s' % (self.name, c.logged_in_persona.name or c.logged_in_persona.username)) %>
        ${h.secure_link(
            h.args_to_tuple('group_action', action='invite'     , id=c.logged_in_persona.username, member=self.id, format='redirect') ,
            value           = _('Invite') ,
            value_formatted = h.literal("<span class='button'>%s</span>") % _('Invite') ,
            title           = invite_text , 
            json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
    
	## GregM: Addition of follower actions
	% if 'follower_invite_trusted' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('member_action', action='follower_invite_trusted'  , id=self.id, format='redirect') ,
            value           = _('Invite trusted') ,
            value_formatted = h.literal("<span class='button mo-help'>%s</span>") % _('Invite trusted'),
            title           = _("Invite %s as a trusted follower" % self.name) ,
            json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
    
	% if 'follower_trust' in self.actions:
	<% description = "Your trusted followers will be able to view your private content" %>
        ${h.secure_link(
            h.args_to_tuple('member_action', action='follower_trust'  , id=self.id, format='redirect') ,
            value           = _('Trust') ,
            value_formatted = h.literal("<span class='button mo-help'>%s<div class='mo-help-r'>%s</div></span>") % (_('Trust'), description),
            title           = _("Trust follower %s" % self.name) ,
            json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
	% elif 'follower_distrust' in self.actions:
	<% description = "By untrusting this user they will no longer be able to view your private content" %>
        ${h.secure_link(
            h.args_to_tuple('member_action', action='follower_distrust'  , id=self.id, format='redirect') ,
            value           = _('Distrust') ,
            value_formatted = h.literal("<span class='button mo-help'>%s<div class='mo-help-r'>%s</div></span>") % (_('Distrust'), description),
            title           = _("Distrust follower %s" % self.name) ,
            json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
        <span class="separtor"></span>
    % endif
</%def>


<%def name="actions_common()">

    <%doc>
    % if 'settings_group' in self.actions:
        <a href="${h.url('edit_group', id=self.id)}" title="${_('_group Settings').capitalize()}"><span class="icon16 i_group"></span>${_('_group Settings').capitalize()}</a>
        <span class="separtor"></span>
    % endif
    
    % if 'settings' in self.actions and self.member['type'] != 'group':
        <a href="${h.url('settings')}" title="${_('Settings')}"><span class="icon16 i_settings"></span>${_('Settings')}</a>
        <span class="separtor"></span>
    % endif
    </%doc>
    <%doc>
    % if 'delete' in self.actions and self.member['type'] == 'group':
        ${h.secure_link(
            h.args_to_tuple('group', id=self.id, format='redirect'),
            method = "DELETE",
            value           = _("Delete _group"),
            value_formatted = h.literal("<span class='icon16 i_delete'></span>%s") % _('Delete'),
            confirm_text    = _("Are your sure you want to delete this group?"),
            json_form_complete_actions = "cb_frag_remove(current_element); cb_frag_reload('members/%s');" % self.id,
        )}
        <span class="separtor"></span>
    % endif
    </%doc>
    
    % if self.member.get('location_current') or self.member.get('location_home'):
        ##${parent.georss_link()}
    % endif
</%def>



##------------------------------------------------------------------------------
## Avatar
##------------------------------------------------------------------------------
<%def name="member_avatar(img_class='')">
    ${member_includes.avatar(self.member, class_='thumbnail_large', img_class=img_class)}
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
