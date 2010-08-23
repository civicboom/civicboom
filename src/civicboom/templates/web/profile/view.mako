<%inherit file="/web/layout_3cols.mako"/>

<%namespace name="member_includes" file="/web/design09/includes/member.mako"  />

<%def name="col_left()">
    ${member_includes.avatar(c.viewing_user, show_name=True, show_follow_button=True)}

    <h2>Following</h2>
        ${member_includes.member_list(c.viewing_user.following, show_avatar=True, class_="avatar_thumbnail_list")}
  
  
    <h2>Followers</h2>
        ${member_includes.member_list(c.viewing_user.followers, show_avatar=True, class_="avatar_thumbnail_list")}
</%def>

<%def name="col_right()">
</%def>

<%def name="body()">
</%def>
