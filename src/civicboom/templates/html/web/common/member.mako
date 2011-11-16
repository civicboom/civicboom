<%def name="kwargs_attrs(**kwargs)">
    % for key, value in kwargs.iteritems():
${key}="${value}" 
    % endfor
</%def>

##------------------------------------------------------------------------------
## Member Autocomplete - used? where?
##------------------------------------------------------------------------------

<%def name="autocomplete_member(field_name='member', size='250px')">
<div style="width: ${size}; padding-bottom: 2em;">
	<input id="${field_name}_name" name="${field_name}_name" type="text">
	<div id="${field_name}_comp"></div>
	<input id="${field_name}" name="${field_name}" type="hidden">
</div>
<script>autocomplete_member("${field_name}_name", "${field_name}_comp", "${field_name}");</script>
</%def>

##------------------------------------------------------------------------------
## Member Link
##------------------------------------------------------------------------------
<%def name="member_link(member, js_link_to_frag=True, new_window=False, class_='', qualified=False, **kwargs)">
<%
    if js_link_to_frag:
        class_ = class_ + ' link_new_frag'
        
    if new_window:
        new_window = 'target="_blank"'
    else:
        new_window = ''
%>
<a href="${h.url('member', id=member['username'], qualified=qualified)}" data-frag="${h.url('member', id=member['username'], format='frag')}" title="${member['name']}" class="${class_}" ${new_window} ${kwargs_attrs(**kwargs)}>${member['name']}</a>
</%def>

##------------------------------------------------------------------------------
## Member Avatar - display a member as text/image + link to profile + follow actions
##------------------------------------------------------------------------------

<%def name="avatar(member, class_='', js_link_to_frag=True, new_window=False, img_class='', as_link=True, qualified=False, **kwargs)">
    % if member:
    <%
        # AllanC - WOOOOOW!!! This is REALLY ineffiencet for passing multiple member objects that are not dicts already
        #          Can this be profiled and checked as to how often this occours?
        if hasattr(member,'to_dict'):
            member = member.to_dict()
            

        if js_link_to_frag:
            js_link_to_frag = h.literal(""" onclick="cb_frag($(this), '%s'); return false;" """ % h.url('member', id=member['username'], format='frag'))
        else:
            js_link_to_frag = ''
            
        if new_window:
            new_window = 'target="_blank"'
        else:
            new_window = ''

    %>\
    <%def name="member_link()"><a class="link_new_frag" href="${h.url('member', id=member['username'], qualified=qualified)}" title="${member['name']}" data-frag="${h.url('member', id=member['username'], format='frag')}"></%def>
    ##<a href="${h.url('member', id=member['username'])}" title="${member['name']}" ${js_link_to_frag} ${new_window}></%def>
    ##% if include_name == 'prefix':
    ##  nothing
    ##% endif
    <div class="thumbnail ${class_}">
	% if as_link:
		${member_link()}
	% endif
              <img src="${member['avatar_url']}" alt="${member['username']}" class="img ${img_class}" onerror='this.onerror=null;this.src="/images/default/avatar_user.png"'/>
	% if as_link:
		</a>
	% endif
    </div>
    % endif
</%def>

## Old Avatar render for reference
<%doc>
 <%def name="avatar(member, show_avatar=True, show_name=False, show_follow_button=False, show_join_button=False, show_invite_button=False, class_=None)">
    <div class="${class_} avatar">
		% if show_avatar:
		<div class="clipper">
            <a href="${h.url('member', id=member['username'])}" title="${member['name']}">
			  <img src="${member['avatar_url']}" alt="${member['username']}" class="img" onerror='this.onerror=null;this.src="/images/default/avatar_user.png"'/>
            </a>
			##<img src="/images/badges/user.png" alt="User" class="type">
            ##% if member['type']=="user":
            ##<div class="type icon16 i_user"></div>
            ##% endif
            % if member['type']=="group":
                ##<div class="type icon16 i_group" title="group"></div>
                ${h.icon('group', class_="type")}
            % endif
            % if 'account_type' in member and member['account_type']!='free':
                ${h.icon('account_type_'+member['account_type'], class_="type")}
            % endif
            
            
            ## TODO - onClick javascript AJAX id card:
            <a class="info icon16 i_userid" href="${h.url('member', id=member['username'])}" title="${_("click for more info about %s" % member['username'])}"><span>more</span></a>
            
            % if not c.logged_in_persona or (c.logged_in_persona and c.logged_in_persona.username != member['username']):
                % if c.logged_in_persona and c.logged_in_persona.is_following(member['username']):
                ${h.secure_link(url('member_action', action='unfollow', id=member['username'], format='redirect'), _(' '), title=_("Stop following %s" % member['username']), css_class="follow_action icon16 i_unfollow")}
                % else:
                ${h.secure_link(url('member_action', action='follow'  , id=member['username'], format='redirect'), _(' '), title=_("Follow %s" % member['username']),         css_class="follow_action icon16 i_follow"  )}
                % endif
            % endif
		</div>
		% endif
		% if show_name:
			<br/>${member['name']} (${member['username']})
		% endif
        ## AllanC -FIXME? - this is cheating! how are API users ment to have access to this!
        ## AllanC - No need to fix API users can get a list of follower and perform this comparison themselfs
        ##          If we did the checking for them that would take lots of querys and time and reducde the ability to cache generated member lists
        % if show_follow_button and c.logged_in_persona and c.logged_in_persona.username != member['username']:
            % if c.logged_in_persona.is_following(member['username']):
            ${h.secure_link(url('member_action', action='unfollow', id=member['username'], format='redirect'), _('Stop following'), css_class="button_small button_small_style_2")}
            % else:
            ${h.secure_link(url('member_action', action='follow'  , id=member['username'], format='redirect'), _('Follow')        , css_class="button_small button_small_style_1")}
            % endif
        % endif
        % if show_join_button:
            ${h.secure_link(url('group_action', action='join'     , id=member['id']       , member=c.logged_in_persona.username), _('Join')        , css_class="button_small button_small_style_1")}
        % endif
        % if show_invite_button and c.logged_in_persona and c.logged_in_persona.__type__=='group':
            ${h.secure_link(url('group_action', action='invite'   , id=c.logged_in_persona.id, member=member['username'] , format='redirect'), _('Invite')      , css_class="button_small button_small_style_1")}
        % endif
    </div>
</%def>
</%doc>

##------------------------------------------------------------------------------
## Member List
##------------------------------------------------------------------------------

<%def name="member_list(members, show_avatar=False, show_name=False, class_=None)">
    <ul class="${class_}">
    % for member in members:
        <li>${avatar(member, show_avatar=show_avatar, show_name=show_name)}</li>
    % endfor
    </ul>
</%def>
