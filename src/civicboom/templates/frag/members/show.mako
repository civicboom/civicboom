<%inherit file="/frag/common/frag.mako"/>

<% import datetime %>

<%namespace name="frag_list"       file="/frag/common/frag_lists.mako"/>
<%namespace name="member_includes" file="/web/common/member.mako"     />

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
        
        if c.logged_in_persona and self.member['username'] == c.logged_in_persona.username:
            self.attr.title     = 'Current User'
            self.attr.icon_type = 'current_user'
            
        
        self.attr.frag_data_css_class = 'frag_member'
        
        self.attr.share_kwargs = {
            'url'      : self.attr.html_url ,
            'title'    : self.name ,
            'image'    : self.member['avatar_url'] ,
        }

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
        
        ${frag_list.member_list(
            d['following'],
            _('Following'),
            h.args_to_tuple('member_action', id=self.id, action='following'),
        )}
        ${frag_list.member_list(
            d['followers'] ,
            _('Followers') ,
            h.args_to_tuple('member_action', id=self.id, action='followers') ,
        )}

        ${frag_list.member_list(
            d['groups'] ,
            _('Groups') ,
            h.args_to_tuple('member_action', id=self.id, action='groups') ,
        )}
        
        % if self.member['type']=='group':
        ${frag_list.member_list(
            d['members'],
            _('Members'),
            h.args_to_tuple('member_action', id=self.id, action='members')
        )}
        % endif
        
        ${member_map()}
        </div>
    </div>
    
    <div class="frag_right_col">
        <div class="frag_col">
        
        ${frag_list.content_list(
            d['assignments_accepted'],
            _('Accepted _assignments'),
            h.args_to_tuple('member_action', id=self.id, action='assignments_accepted'),
            creator = True,
        )}
        
        ## Content --------------------------------------------
        
        ## All content for development
        ##${frag_list.content_list(d['content']             , _('Content')              , url('member_actions', id=id, action='content')              )}
        
        ${frag_list.content_list(
            [c for c in d['content'] if c['type']=='draft'] ,
            _('Drafts') ,
            h.args_to_tuple('contents', creator=self.id, list='drafts') , ##format='html'),
        )}
        
        ${frag_list.content_list(
            [c for c in d['content'] if c['type']=='assignment' and (c['due_date']==None or c['due_date']>=datetime.datetime.now()) ] ,
            _('Assignments Active') ,
            h.args_to_tuple('contents', creator=self.id, list='assignments_active') ,
        )}
        
        ${frag_list.content_list(
            [c for c in d['content'] if c['type']=='assignment' and (c['due_date']!=None and c['due_date']<=datetime.datetime.now()) ] ,
            _('Assignments Previous') ,
            h.args_to_tuple('contents', creator=self.id, list='assignments_previous') ,
        )}
        
        ${frag_list.content_list(
            [c for c in d['content'] if c['type']=='article' and c['response_type']!='none' ] ,
            _('Responses') ,
            h.args_to_tuple('contents', creator=self.id, list='responses') ,
        )}
        
        ${frag_list.content_list(
            [c for c in d['content'] if c['type']=='article' and c['response_type']=='none' ] ,
            _('Articles') ,
            h.args_to_tuple('contents', creator=self.id, list='articles') ,
        )}
        
        ${frag_list.content_list(
            d['boomed_content'],
            _('Boomed content'),
            h.args_to_tuple('member_action', id=self.id, action='boomed_content') ,
            #h.args_to_tuple('contents', boomed_by=id) ,
            creator = True ,
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
            _(' ') ,
            title     = _("Follow %s" % self.name) ,
            css_class = "icon icon_follow" ,
            json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
    % endif

    % if 'unfollow' in self.actions:
        ${h.secure_link(
            h.args_to_tuple('member_action', action='unfollow'  , id=self.id, format='redirect') ,
            _(' ') ,
            title=_("Stop following %s" % self.name) ,
            css_class="icon icon_unfollow" ,
            json_form_complete_actions = "cb_frag_reload('members/%s');" % self.id ,
        )}
    % endif

    % if 'join' in self.actions:
        ${h.secure_link(h.args_to_tuple('group_action', action='join'       , id=self.id, member=c.logged_in_persona.username, format='redirect'), _('Join this _group'), css_class="icon icon_join"  )}
    % endif
    
    % if 'invite' in self.actions and c.logged_in_persona and c.logged_in_persona.__type__=='group':
        ${h.secure_link(h.args_to_tuple('group_action', action='invite'     , id=c.logged_in_persona.username, member=self.id, format='redirect'), _('Invite %s to join %s' % (self.name, c.logged_in_persona['name']))      , css_class="icon icon_invite")}
    % endif
</%def>


<%def name="actions_common()">
    % if 'message' in self.actions:
        <a class="icon icon_message" href="" title="${_('Send %s a message') % self.name}"><span>${_('Message')}</span></a>
    % endif
    % if 'settings' in self.actions:
        <a class="icon icon_settings" href="${url('settings')}" title="${_('Settings')}"><span>${_('Settings')}</span></a>
    % endif
    <a class="icon icon_widget"  href="${url(controller='misc', action='widget_preview')}" title="${_('Widget Preview')}"><span>${_('Widget Preview')}</span></a>
    
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
    <p>implement map</p>
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

