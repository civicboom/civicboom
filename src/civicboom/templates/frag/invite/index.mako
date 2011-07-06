<%inherit file="/frag/common/frag.mako"/>

<%!
    rss_url = False
    auto_georss_link = False
%>

<%namespace name="frag_list"       file="/frag/common/frag_lists.mako" />
<%namespace name="member_includes" file="/html/web/common/member.mako" />

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%def name="init_vars()">
    <%
    	invite_types		= { 'trusted_follower' : _('Invite people to become trusted followers'),
    							'assignment'       : _('Invite people to participate in this _assignment'),
    							'group'            : _('Invite people to join this _group'),
    							'payment_add_user' : _('Add members and _groups to this payment account'),
    	}
    	invite_types_desc   = { 'trusted_follower' : _('The people below will be invited to become trusted followers'),
    							'assignment'       : _('The people below will be invited to participate in this _assignment'),
    							'group'            : _('The people below will be invited to join this _group'),
                                'payment_add_user' : _('The people below will be added to this payment account'),
    	}
        self.attr.title     = invite_types[d['invite']]
        self.attr.desc      = invite_types_desc[d['invite']]
        self.attr.icon_type = None
    %>
</%def>

<%def name="select_item(value, text, current_value)">
	<option value="${value}" ${'selected="selected"' if value==current_value else ''}>${text}</option>
</%def>

##------------------------------------------------------------------------------
## Member Fragment
##------------------------------------------------------------------------------
<%def name="body()">
	% if c.format=="frag" and c.result.get('message', '') != '':
		<script type="text/javascript">
			flash_message({ message: '${c.result['message']}', status: '${c.result['status']}' });
		</script>
	% endif

	<form onsubmit="" class="inviteform" method="POST" action="/${h.url('invite')}">
		<input type="hidden" class="search-limit" name="search-limit" value="${d['search-limit']}" />
		<input type="hidden" name="id" value="${d.get('id')}" />
		<input type="hidden" name="invite" value="${d.get('invite')}" />
	    <div class="frag_right_col">
	        <div class="frag_col">
		        <div class="invite_header">
		        	<h1>${_('Invite people & hubs')}</h1>
		        	<div>
		        		<h2>${_('Search')}</h2>
		        		<select name="search-type">
		        			${select_item('', 'Everyone', d.get('search-type'))}
##		        			${select_item('member_of', 'Members', d.get('search-type'))}
							${select_item('follower_of', 'Followers', d.get('search-type'))}
		        			${select_item('followed_by', 'Following', d.get('search-type'))}
		        		</select>
		        		<input name="search-name" placeholder="Enter your search here..." type="text" value="${d.get('search-name')}" />
		        		<div class="pad_top align_right">
			        		<input class="button" onclick="return postInviteFrag($(this))" type="submit" name="submit-everyone" value="Add All" />
			        		<input class="button" onclick="return inviteClick(this)" type="submit" name="search-button" value="Search" />
			        	</div>
		        	</div>
		        </div>
	        	<div class="invite_area invite-list">
	        		${invite_list()}
	        	</div>
	        </div>
	    </div>
	    <div class="frag_left_col">
	        <div class="frag_col">
		        <div class="invite_header">
	        		<h1>${_('Invitees')}</h1>
	        		<p>${self.attr.desc}</p>
	        		% if 'roles' in d:
	        			<p>
	        				${_('Invite as role:')}
	        				<select name="invite-role">
	        				% for role in d['roles']:
	        					${select_item(role, role.capitalize(), d.get('invite-role'))}
	        				% endfor
	        				</select>
	        			</p>
	        		% endif
	        		% if 'error-list' in d:
	        			<p class="error">${_('Unfortunately there was a problem inviting the people below')}</p>
	        		% endif
	        	</div>
		        <div class="invite_area invitee-list">
			        ${invitee_list()}
		        </div>
	        </div>
	    </div>
		        <div class="bottom" class="">
		        	<div class="frag_left_col frag_col ">
	    			<input class="button" type="submit" onclick="return postInviteFrag($(this));" name="submit-invite" value="Invite" />
	    			</div>
	   			</div>

	</form>

</%def>

<%def name="page_button(name, text, disabled)">
	<input class="button ${'disabled'if disabled else''}" onclick="return inviteClick(this)" ${'disabled=disabled'if disabled else''} type="submit" name="${name}" value="${text}" />
</%def>

<%def name="invitee_list()">
	<%
		list = d['invitee_list']['items']
		list_keys = sorted(list.keys(), reverse=True)
		i = -1
	%>
	<div class="invite-controls">
		${page_button("invitee-prev", "<<", d['invitee-offset']==0)}
		<div>${page_button("invitee-next", ">>", d['invitee-offset']+d['search-limit']>d['invitee_list']['count'])}</div>
	</div>
	<input type="hidden" class="invitee-offset" name="invitee-offset" value="${d['invitee-offset']}" />
	<ul class="invitee_ul">
		% if len(list) == 0:
			<li class="none">${_('Select people to invite from the right')}</li>
		% endif
		% for key in list_keys:
		<%
			item = list[key]
			i += 1
		%>
			<li class="pad_top" style="display: ${'inline-block' if i >= d['invitee-offset'] and i < d['invitee-offset']+d['search-limit'] else 'none'};">
				<div class="action"><button onclick="return inviteClick(this)" class="button_white" type="submit" name="rem-${key}"><div class="icon16 i_delete"><span>${_('Add')}</span></div></button></div>
				<div class="avatar">${member_avatar(item)}</div>
				<div class="data">
					% if len(item.get('name')) > 0:
						${item.get('name')}<br />
					% endif
					${item.get('username')}
					% if 'error-list' in d and item['username'] in d['error-list']:
						<br /><span class="error">${d['error-list'][item['username']]['message']}</span>
					% endif
				</div>
				<input type="hidden" class="username" name="inv-${key}" value="${item.get('username')}" />
			</li>
		% endfor
	</ul>
</%def>

<%def name="invite_list()">
	<%
		list = d['invite_list']['items']
	%>
	<div class="invite-controls">
		${page_button("search-prev", "<<", d['search-offset']==0)}
		<div>${page_button("search-next", ">>", d['search-offset']+d['search-limit']>d['invite_list']['count'])}</div>
	</div>
	<input type="hidden" class="search-offset" name="search-offset" value="${d['search-offset']}" />
	<input type="hidden" class="exclude-members" name="exclude-members" value="${d['exclude-members']}" />
	<ul class="invite_ul">
		% if len(list) == 0:
			<li>${_('Your search returned no results')}</li>
		% endif
		% for item in list:
			<li class="pad_top">
				<div class="action"><button onclick="return inviteClick(this)" class="button_white" type="submit" name="add-${item.get('username')}"><div class="icon16 i_plus"><span>${_('Add')}</span></div></button></div>
				<div class="avatar">${member_avatar(item)}</div>
				<div class="data">
					% if len(item.get('name')) > 0:
						${item.get('name')}<br />
					% endif
					${item.get('username')}
				</div>
			</li>
		% endfor
	</ul>
</%def>

##------------------------------------------------------------------------------
## Avatar
##------------------------------------------------------------------------------
<%def name="member_avatar(member)">
    ${member_includes.avatar(member, class_='thumbnail_small')}
</%def>



##------------------------------------------------------------------------------
## Map
##------------------------------------------------------------------------------
<%def name="member_map()">
    ##<p>implement map</p>
</%def>
