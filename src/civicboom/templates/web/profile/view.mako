<%inherit file="/web/common/html_base.mako"/>

<%namespace name="member_includes"  file="/web/common/member.mako"  />
<%namespace name="content_includes" file="/web/common/content_list.mako"/>

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

	<h2>Write to ${d['member']['username']}</h2>
	${h.form(url('messages', format='redirect'))}
		<input type="hidden" name="target" value="${d['member']['username']}">
		<input type="text" name="subject">
		<textarea name="content"></textarea>
		<input type="submit" value="Send">
	${h.end_form()}


    ${content_list(d['member']['content_public'], type_filters=["article", "assignment"])}
    
    ${content_list_group(d['member']['assignments_accepted'], "assignments accepted")}
    
</%def>


##------------------------------------------------------------------------------
## Other Components
##------------------------------------------------------------------------------

<%def name="content_list(contents, type_filters, show_actions=False)">
    % for type_filter in type_filters:
        <%
            content_list = [content for content in contents if content['type']==type_filter]
        %>
        ${content_list_group(content_list, type_filter, show_actions=show_actions)}
    % endfor
</%def>
<%def name="content_list_group(contents, title, show_actions=False)">
        <h2>${title.capitalize()} ${len(contents)}</h2>
        % if len(contents)>0:
            ${content_includes.content_list(contents, show_actions=show_actions)}
        % else:
            <span class="message_empty">No ${title}</span>
        % endif
</%def>
