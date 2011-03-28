<%namespace name="member_includes" file="/html/web/common/member.mako"     />
##------------------------------------------------------------------------------
## Avatar
##------------------------------------------------------------------------------
<%def name="member_avatar(member)">
    ${member_includes.avatar(member, class_='thumbnail_small')}
</%def>


	<%
		list = d['invite_list']['items']
	%>
	<ul class="invite_ul">
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
				<div style="float:right"><input onclick="return inviteClick(this)" class="button" type="submit" name="add-${item.get('username')}" value="Add" /></div>
			</li>
		% endfor
	</ul>
