<%inherit file="/web/layout_3cols.mako"/>

<%namespace name="member_includes"  file="/web/design09/includes/member.mako"  />
<%namespace name="content_includes" file="/web/design09/includes/content_list.mako"/>

<%def name="rss()">${self.rss_header_link()}</%def>
<%def name="rss_url()">${url(controller='search', action='content', author=c.viewing_user.username, format='xml')}</%def>
<%def name="rss_title()">Articles by ${c.viewing_user.name}</%def>

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

    % for content_type in ["article", "assignment"]:
        <h2>${content_type}</h2>
        <%
            content_list = [content for content in c.viewing_user.content if content.__type__==content_type]
        %>
        % if len(content_list)>0:
            ${content_includes.content_list(content_list)}
        % else:
            <span class="message_empty">No ${content_type}</span>
        % endif
    % endfor

</%def>
