<%namespace name="member_includes"  file="/web/common/member.mako"  />
##<%namespace name="content_includes" file="/web/common/content_list.mako"/>

<%namespace name="frag_list" file="/frag/common/frag_lists.mako"/>
<%namespace name="share"     file="/frag/common/share.mako"     />

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
${frag_member(d)}
</%def>

##------------------------------------------------------------------------------
## Member Fragment
##------------------------------------------------------------------------------
<%def name="frag_member(d)">
    <% member = d['member']  %>
    <% id     = member['id'] %>
    
    <div class="title_bar">
        ${title_bar(d['actions'])}
    </div>
    <div class="action_bar">
        ${action_bar(d['actions'])}
    </div>
    
    <div class="frag_data frag_member">
        <div class="frag_left_col">
            <div class="frag_col">
            ## Member Details
            ${member_avatar(member)}
            ${member_map(  member)}
            </div>
        </div>
        <div class="frag_right_col">
            <div class="frag_col">
            ## Member Content
            ${frag_list.member_list(
                d['following'],
                _('Following'),
                h.args_to_tuple('member_action', id=id, action='following'),
            )}
            ${frag_list.member_list(
                d['followers'] ,
                _('Followers') ,
                h.args_to_tuple('member_action', id=id, action='followers') ,
            )}
            
            ${frag_list.content_list(
                d['assignments_accepted'],
                _('Accepted _assignments'),
                h.args_to_tuple('member_action', id=id, action='assignments_accepted'),
                creator = True,
            )}
            ##${frag_list.content_list(d['content']             , _('Content')              , url('member_actions', id=id, action='content')              )}
            
            <% import datetime %>
            
            ${frag_list.content_list(
                [c for c in d['content'] if c['type']=='draft'] ,
                _('Drafts') ,
                h.args_to_tuple('contents', creator=id, list='drafts') , ##format='html'),
            )}
            
            ${frag_list.content_list(
                [c for c in d['content'] if c['type']=='assignment' and (c['due_date']==None or c['due_date']>=datetime.datetime.now()) ] ,
                _('Assignments Active') ,
                h.args_to_tuple('contents', creator=id, list='assignments_active') ,
            )}
            
            ${frag_list.content_list(
                [c for c in d['content'] if c['type']=='assignment' and (c['due_date']!=None and c['due_date']<=datetime.datetime.now()) ] ,
                _('Assignments Previous') ,
                h.args_to_tuple('contents', creator=id, list='assignments_previous') ,
            )}
            
            ${frag_list.content_list(
                [c for c in d['content'] if c['type']=='article' and c['response_type']!='none' ] ,
                _('Responses') ,
                h.args_to_tuple('contents', creator=id, list='responses') ,
            )}
            
            ${frag_list.content_list(
                [c for c in d['content'] if c['type']=='article' and c['response_type']=='none' ] ,
                _('Articles') ,
                h.args_to_tuple('contents', creator=id, list='articles') ,
            )}

            ${frag_list.content_list(
                d['boomed_content'],
                _('Boomed content'),
                h.args_to_tuple('member_action', id=id, action='boomed_content') ,
                #h.args_to_tuple('contents', boomed_by=id) ,
                creator = True ,
            )}
            
            % if member['type']=='group':
            ${frag_list.group_members_list(
                d['members'],
                _('Members'),
                h.args_to_tuple('member_action', id=id, action='members')
            )}
            % endif
            </div>
        </div>
    </div>
</%def>

##------------------------------------------------------------------------------
## Avatar
##------------------------------------------------------------------------------
<%def name="member_avatar(member)">
    ${member_includes.avatar(member, class_='thumbnail_large')}
</%def>



##------------------------------------------------------------------------------
## Map
##------------------------------------------------------------------------------
<%def name="member_map(member)">
    <p>implement map</p>
</%def>



##------------------------------------------------------------------------------
## Action/Title Bar
##------------------------------------------------------------------------------
<%def name="title_bar(actions)">
    <div class="title">
        <% type = d['member']['type'] %>
        <span class="icon icon_${type}"></span><span class="title_text">${type.capitalize()}</span>
    </div>

    <div class="common_actions">
        ${share.share(
            url         = url('member', id=d['member']['username'], host=app_globals.site_host, protocol='http'),
            title       = _('%s on _site_name' % d['member']['name']) ,
            description = d['member'].get('description') or '' ,
        )}
        
        ##<a href='${url('formatted_member', id=d['member']['username'], format='rss')}' title='RSS for ${d['member']['username']}' class="icon icon_rss"  ><span>RSS</span></a>
        <a href='${url.current(format='rss')}' title='RSS' class="icon icon_rss"><span>RSS</span></a>
        <a href='' onclick="cb_frag_remove($(this)); return false;" title='${_('Close')}' class="icon icon_close"><span>${_('Close')}</span></a>
    </div>
</%def>

<%def name="action_bar(actions)">

    <% member = d['member'] %>
    <% name   = d['member'].get('name') or d['member'].get('username') %>

    <div class="object_actions_specific">
        % if c.logged_in_persona and c.logged_in_persona.username != member['username']:
            % if c.logged_in_persona and c.logged_in_persona.is_following(member['username']):
            ${h.secure_link(h.args_to_tuple('member_action', action='unfollow'  , id=member['username'], format='redirect'), _(' '), title=_("Stop following %s" % name),         css_class="icon icon_unfollow")}
            ##${h.secure_link(url('member_action', action='unfollow', id=member['username'], format='redirect'), _(' '), title=_("Stop following %s" % member['username']), css_class="follow_action icon icon_unfollow")}
            % else:
            ${h.secure_link(h.args_to_tuple('member_action', action='follow'    , id=member['username'], format='redirect'), _(' '), title=_("Follow %s" % name),         css_class="icon icon_follow")}
            % endif
        % endif
    
        % if 'join' in actions:
            ${h.secure_link(h.args_to_tuple('group_action', action='join'  , id=member['id']          , member=c.logged_in_persona.username, format='redirect'), _('Join this _group')                                                          , css_class="icon icon_join"  )}
        % endif
        
        % if 'invite' in actions: ##and c.logged_in_persona and c.logged_in_persona.__type__=='group':
            ${h.secure_link(h.args_to_tuple('group_action', action='invite', id=c.logged_in_persona.id, member=member['username']          , format='redirect'), _('Invite %s to join %s' % (member['name'], c.logged_in_persona['name']))      , css_class="icon icon_invite")}
        % endif

    </div>

    <div class="object_actions_common">
        % if 'message' in actions:
            <a class="icon icon_message" href="#" title="${_('Send %s a message') % name}"><span>${_('Message')}</span></a>
        % endif
        <a class="icon icon_widget"  href="${url(controller='misc', action='widget_preview')}" title="${_('Widget Preview')}"><span>${_('Widget Preview')}</span></a>
    </div>

    
    
    
    

</%def>

##------------------------------------------------------------------------------
## 
##------------------------------------------------------------------------------
<%def name="member_(member)">

</%def>

