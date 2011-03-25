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
        self.attr.title     = "Invite people"
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
		}
		#frag_containers .frag_container .frag_right_col {
		    float: right;
		    width: 50%;
		}
	</style>
	<form method="POST" action="/invite">
	    <div class="frag_right_col">
	        <div class="frag_col">
	        	<h1>Invite people</h1>
	        	<div>
	        		<h2>Search</h2>
	        		<select name="search-type">
	        			${select_item('', 'Everyone', d.get('search-type'))}
##	        			${select_item('member_of', 'Members', d.get('search-type'))}
						${select_item('follower_of', 'Followers', d.get('search-type'))}
	        			${select_item('followed_by', 'Following', d.get('search-type'))}
	        		</select>
	        		<input name="search-name" type="text" value="${d.get('search-name')}" /><br />
	        		<input class="button" type="submit" name="search" value="Search" />
	        	</div>
	        	<div class="invite-list">
	        		${invite_list()}
	        	</div>
	        </div>
	    </div>
	    <div class="frag_left_col">
	        <div class="frag_col">
	        	<h1>Invitees</h1>
		        <div class="invitee-list">
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
	<ul>
		% if len(list) == 0:
			${_('Select people to invite from the right')}
		% endif
		% for item in list:
			<li style="padding-top: 3px; display: inline-block; width: 100%;">
				<div style="float:left">${member_avatar(item)}</div>
				% if len(item.get('name')) > 0:
					${item.get('name')}<br />
				% endif
				${item.get('username')}
				<div style="float:right"><input class="button" type="submit" name="rem-${item.get('username')}" value="Remove" /></div>
				<input type="hidden" name="inv-${item.get('username')}" value="${item.get('username')}" />
			</li>
		% endfor
	</ul>
</%def>

<%def name="invite_list()">
	<%
		list = d['invite_list']['items']
	%>
	<ul>
		% if len(list) == 0:
			${_('Your search returned no results')}
		% endif
		% for item in list:
			<li style="padding-top: 3px; display: inline-block; width: 100%;">
				<div style="float:left">${member_avatar(item)}</div>
				% if len(item.get('name')) > 0:
					${item.get('name')}<br />
				% endif
				${item.get('username')}
				<div style="float:right"><input class="button" type="submit" name="add-${item.get('username')}" value="Add" /></div>
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
