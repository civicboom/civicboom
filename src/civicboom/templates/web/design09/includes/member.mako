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
## Member Avatar - display a member as text/image + link to profile + follow actions
##------------------------------------------------------------------------------

<%def name="avatar(member, show_avatar=True, show_name=False, show_follow_button=False, class_=None)">
    % if class_:
    <div class="${class_}">
    % endif
        <a href="${h.url(controller='profile', action='view', id=member.username)}" title="${member.username}">
            % if show_avatar:
                <img src="${member.avatar_url}" alt="${member.username}"/>
            % endif
            % if show_name:
                ${member.name} (${member.username})
            % endif
        </a>
        % if show_follow_button and c.logged_in_user != member:
            % if c.logged_in_user in member.followers:
            <a class="button_small button_small_style_2" href="${h.url(controller='member', action='unfollow', id=member.username)}">${_('Stop following')}</a>
            % else:
            <a class="button_small button_small_style_1" href="${h.url(controller='member', action=  'follow', id=member.username)}">${_('Follow')}</a>
            % endif
        % endif
    % if class_:
    </div>
    % endif
</%def>


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