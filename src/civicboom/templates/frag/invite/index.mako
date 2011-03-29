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
					invitee_ul.append(li);
					invitee_ul.children('li.none').remove();
					exclude_members.push(button_key);
					li.append('<input type="hidden" class="username" name="inv-' + (exclude_members.length - 1) + '" value="' + button_key + '" />');
					li.find('input.button').val('Remove').attr('name', 'rem-' + (exclude_members.length - 1));
					// refreshSearch(button); Needs adding when exclude-members starts working
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
			}
			return false;
		}
		function refreshSearch(element, extra_fields) {
			var form = element.parents('form');
			var ul = form.find('.invite_ul');
			var formArray = form.serializeArray();
			if (typeof extra_fields != 'undefined')
				formArray = formArray.concat(extra_fields)
			formArray.push({'name': 'exclude-members', 'value': exclude_members});
			$.post('/invite/search.frag', formArray, function (data) {
				ul.html(data);
			});
		}
	</script>
	<form method="POST" action="/invite?invite=${d.get('invite')}&id=${d.get('id')}">
	    <div class="frag_right_col">
	        <div class="frag_col">
		        <div class="invite_header">
		        	<h1>Invite people</h1>
		        	<div>
		        		<h2>Search</h2>
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
	        	<div class="invite-controls">
	        	% if d['search-offset'] > 0:
	        		<input class="button" onclick="return inviteClick(this)" type="submit" name="search-prev" value="<<" />
	        	% endif
	        		<input class="button" onclick="return inviteClick(this)" type="submit" name="search-next" value=">>" />
	        	</div>
	        </div>
	    </div>
	    <div class="frag_left_col">
	        <div class="frag_col">
		        <div class="invite_header">
	        		<h1>Invitees</h1>
	        		<p>The invitees below will...</p>
	        	</div>
		        <div class="invite_area invitee-list">
			        ${invitee_list()}
		        </div>
	        </div>
	    </div>
	</form>

</%def>

<%def name="select_item(value, text, current_value)">
	<option value="${value}" ${'selected="selected"' if value==current_value else ''}>${text}</option>
</%def>

<%def name="invitee_list()">
	<%
		list = d['invitee_list']['items']
	%>
	<ul class="invitee_ul">
		% if len(list) == 0:
			<li class="none">${_('Select people to invite from the right')}</li>
		% endif
		% for key in list.keys():
		<%
			item = list[key]
		%>
			<li style="padding-top: 3px; display: inline-block; width: 100%;">
				<div style="float:left">${member_avatar(item)}</div>
				% if len(item.get('name')) > 0:
					${item.get('name')}<br />
				% endif
				${item.get('username')}
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
