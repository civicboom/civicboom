<%inherit file="/web/common/layout_3cols.mako"/>

<%namespace name="member_includes"  file="/web/design09/includes/member.mako"  />
<%namespace name="content_includes" file="/web/design09/includes/content_list.mako"/>

##------------------------------------------------------------------------------
## RSS
##------------------------------------------------------------------------------

<%def name="rss()">${self.rss_header_link()}</%def>
<%def name="rss_url()">${url(controller='search', action='content', creator=d['member']['username'], format='rss')}</%def>
<%def name="rss_title()">Articles by ${d['member']['username']}</%def>


##------------------------------------------------------------------------------
## Left Col
##------------------------------------------------------------------------------

<%def name="col_left()">

    % if 'member' in d:
        <div class="avatar">
            ${member_includes.avatar(d['member'] , show_name=True, show_follow_button=True)}
        </div>
    
        <h2>${_("Following")}</h2>
            <div id="following">
            % if d['member']['following']:
                ${member_includes.member_list(d['member']['following'], show_avatar=True, class_="avatar_thumbnail_list")}
            % else:
                <span class="message_empty">Not following anyone</span>
            % endif
            </div>
    
        <h2>${_("Followers")}</h2>
            <div id="followers">
            % if d['member']['followers']:
                ${member_includes.member_list(d['member']['followers'], show_avatar=True, class_="avatar_thumbnail_list")}
            % else:
                <span class="message_empty">No followers</span>
            % endif
            </div>
    % endif

</%def>

##------------------------------------------------------------------------------
## Right Col
##------------------------------------------------------------------------------


<%def name="col_right()">
    <h2>Public Messages</h2>
	% if d['member']['messages_public']:
        % for message in d['member']['messages_public']:
            ${message}
        % endfor
    % endif
</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">

	<h2>Write to ${c.viewing_user.name}</h2>
	${h.form(url('messages', format='redirect'))}
		<input type="hidden" name="target" value="${c.viewing_user.username}">
		<input type="text" name="subject">
		<textarea name="content"></textarea>
		<input type="submit" value="Send">
	${h.end_form()}


    ${content_list(d['content'], ["article", "assignment"])}
    
</%def>


##------------------------------------------------------------------------------
## Other Components
##------------------------------------------------------------------------------

<%def name="content_list(contents, content_types)">
    % for content_type in content_types:
        <%
            content_list = [content for content in contents if content['type']==content_type]
        %>
        <h2>${content_type} ${len(content_list)}</h2>

        % if len(content_list)>0:
            ${content_includes.content_list(content_list, actions=True)}
        % else:
            <span class="message_empty">No ${content_type}</span>
        % endif
    % endfor
</%def>