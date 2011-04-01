<%inherit file="/frag/common/frag.mako"/>

<%!
    import civicboom.lib.constants as constants
    rss_url = True
%>

<%namespace name="frag_list"       file="/frag/common/frag_lists.mako"/>
<%namespace name="member_includes" file="/html/web/common/member.mako"     />

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%def name="init_vars()">
    <%
    	invite_types		= { 'trusted_follower' : _('Invite people to become trusted followers'),
    							'assignment'       : _('Invite people to view this _assignment'),
    							'group'            : _('Invite people to join this _group'),
    	}
        self.attr.title     = invite_types[d['invite']]
        self.attr.icon_type = None
    %>
</%def>

##------------------------------------------------------------------------------
## Member Fragment
##------------------------------------------------------------------------------
<%def name="body()">
    <style type="text/css">
		#frag_containers .frag_container .frag_left_col {
		    float: left;
		    width: 50%;
		    height: 100%;
		}
		#frag_containers .frag_container .frag_right_col {
		    float: right;
		    width: 50%;
		    height: 100%;
		}
		.frag_col {
			position: relative;
			height: 100%;
		}
		.invite_header {
			height: 8.5em;
		}
	</style>
	<script type="text/javascript">
		Array.prototype.remove = function (subject) {
			var r = new Array();
			for(var i = 0, n = this.length; i < n; i++)
			{
				if(!(this[i]==subject))
				{
					r[r.length] = this[i];
				}
			}
			return r;
		}
		Array.prototype.contains = function (subject) {
			for(var i = 0, n = this.length; i < n; i++)
			{
				if((this[i]==subject))
				{
					return true;
				}
			}
			return false;
		}
		var exclude_members = "${d['exclude-members']}".split(',');
		function inviteClick(eO) {
			var button        = $(eO);
			var button_name   = button.attr('name');
			if (button_name  == 'Invite') return true;
			var button_action = button_name.split('-',1)[0];
			var button_key    = button_name.split('-',2)[1];
			switch (button_action) {
				case 'add':
					if (exclude_members.contains(button_key)) {
						// Already exists in invitee list!
						return false;
					}
					var invitee_ul = button.parents('form').find('.invitee_ul');
					var li = button.parents('li').detach();
					invitee_ul.prepend(li);
					invitee_ul.children('li.none').remove();
					exclude_members.push(button_key);
					li.append('<input type="hidden" class="username" name="inv-' + (exclude_members.length - 1) + '" value="' + button_key + '" />');
					li.find('input.button').val('Remove').attr('name', 'rem-' + (exclude_members.length - 1));
					refreshSearch(button);
				break;
				case 'rem':
					var li = button.parents('li');
					var ul = button.parents('ul');
					var username = li.find('input.username').val();
					// remove username from exclude list
					exclude_members = exclude_members.remove(username);
					refreshSearch(button);
					li.remove();
					if (ul.find('li').length == 0)
						ul.append('<li class="none">${_('Select people to invite from the right')}</li>');
				break;
				case 'search':
					refreshSearch(button, [{ 'name':button_name }]);
					break;
				case 'invitee':
					offset = getValue(button,'invitee-offset');
					limit  = getValue(button,'search-limit');
					ul     = button.parents('form').find('.invitee_ul');
					switch (button_key) {
						case 'next':
							if (offset + limit <= ul.find('li').count) {
								offset = offset + limit;
								ul.parents('form').find('.invitee-prev').attr('disabled','');
							} else {
								ul.parents('form').find('.invitee-prev').attr('disabled','disabled');
							}
						break;
						case 'prev':
							if (offset - limit <= 0) {
								offset = 0;
								ul.parents('form').find('.invitee-prev').attr('disabled','disabled');
								
							} else {
								offset = offset - limit;
							}
							ul.parents('form').find('.invitee-next').attr('disabled','');
						break;
					}
					
					listPaginate(ul, offset, limit);
					console.log('rar');
					break;
			}
			return false;
		}
		function refreshSearch(element, extra_fields) {
			var form = element.parents('form');
			var ul = form.find('.invite-list');
			var formArray = form.serializeArray();
			if (typeof extra_fields != 'undefined')
				formArray = formArray.concat(extra_fields)
			formArray.push({'name': 'exclude-members', 'value': exclude_members});
			$.post('/invite/search.frag', formArray, function (data) {
				ul.html(data);
				ul.children('.search-offset').val()
			});
		}
		function getValue(element, class) {
			return element.parents('form').find('.'+class).val() * 1;
		}
		function listPaginate(ul, offset, limit) {
			var visible = ul.children('li:eq('+offset+'),li:gt('+offset+')').filter('li:lt('+limit+')').css('display','inline-block');
			var hidden  = ul.children('li').not(visible).css('display','none');
		}
	</script>
	<form method="POST" action="/invite?invite=${d.get('invite')}&id=${d.get('id')}">
		<input type="hidden" class="search-limit" name="search-limit" value="${d['search-limit']}" />
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
		        		<div style="text-align: right; padding-top: 3px"><input class="button" onclick="return inviteClick(this)" type="submit" name="search-button" value="Search" /></div>
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
	        		<p>${_('The people below will be invited to...')}</p>
	        		% if 'error-list' in d:
	        			<p class="error">${_('Unfortunately there was a problem inviting the people below')}</p>
	        		% endif
	        	</div>
		        <div class="invite_area invitee-list">
			        ${invitee_list()}
		        </div>
	        </div>
	    </div>
		        <div class="bottom" style="clear:both;">
	    			<input class="button" type="submit" name="submit-invite" value="Invite" />
	   			</div>
	</form>

</%def>

<%def name="select_item(value, text, current_value)">
	<option value="${value}" ${'selected="selected"' if value==current_value else ''}>${text}</option>
</%def>

<%def name="invitee_list()">
	<%
		list = d['invitee_list']['items']
		list_keys = sorted(list.keys(), reverse=True)
		i = -1
	%>
	<div class="invite-controls">
		<input class="button" onclick="return inviteClick(this)" ${'disabled=disabled' if d['invitee-offset']==0 else''} type="submit" name="invitee-prev" value="<<" />
		<input class="button" onclick="return inviteClick(this)" ${'disabled=disabled' if d['invitee-offset']+d['search-limit']>d['invitee_list']['count'] else''} type="submit" name="invitee-next" value=">>" />
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
			<li style="padding-top: 3px; display: ${'inline-block' if i >= d['invitee-offset'] and i < d['invitee-offset']+d['search-limit'] else 'none'} ; width: 100%;">
				<div style="float:left">${member_avatar(item)}</div>
				% if len(item.get('name')) > 0:
					${item.get('name')}<br />
				% endif
				${item.get('username')}
				% if 'error-list' in d and item['username'] in d['error-list']:
					<br />${d['error-list'][item['username']]['message']}
				% endif 
				<div style="float:right"><input onclick="return inviteClick(this)" class="button" type="submit" name="rem-${key}" value="Remove" /></div>
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
		<input class="button" onclick="return inviteClick(this)" ${'disabled=disabled' if d['search-offset']==0 else''} type="submit" name="search-prev" value="<<" />
		<input class="button" onclick="return inviteClick(this)" ${'disabled=disabled' if d['search-offset']+d['search-limit']>d['invite_list']['count'] else''} type="submit" name="search-next" value=">>" />
	</div>
	<input type="hidden" class="search-offset" name="search-offset" value="${d['search-offset']}" />
	<ul class="invite_ul">
		% if len(list) == 0:
			<li>${_('Your search returned no results')}</li>
		% endif
		% for item in list:
			<li style="padding-top: 3px; display: inline-block; width: 100%;">
				<div style="float:left">${member_avatar(item)}</div>
				% if len(item.get('name')) > 0:
					${item.get('name')}<br />
				% endif
				${item.get('username')}
				<div style="float:right"><input onclick="return inviteClick(this)" class="button" type="submit" name="add-${item.get('username')}" value="Add" /></div>
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
