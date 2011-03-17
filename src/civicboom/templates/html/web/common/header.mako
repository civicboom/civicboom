##------------------------------------------------------------------------------
## Logo
##------------------------------------------------------------------------------
<h1 id="logo">
	<a href='/'>
		<img  class='logo_img'     src='/images/logo.png'                  alt='${_("_site_name")}' />
        <img  class='beta_overlay' src='/styles/web/logo_beta_overlay.png' alt='${_("Beta")}'       />
		<span class='logo_text'>${_("_site_name")}</span>
	</a>
</h1>


##------------------------------------------------------------------------------
## Persona Switching
##------------------------------------------------------------------------------
% if c.logged_in_persona:
<div id="persona_select">
    <div id="persona_holder" style="vertical-align: center;">
      <a class="name" href="${url(controller='profile', action='index')}"><!--
	  	--><img src="${c.logged_in_persona.avatar_url}" alt="${c.logged_in_persona.name}" onerror='this.onerror=null;this.src="/images/default/avatar.png"' /><!--
	  --></a>
      <%def name="messageIcon(messages)">
        % if messages > 0:
          <div class="icon_overlay_red">&nbsp;${messages}&nbsp;</div>
        % endif
      </%def>
      <div id="message_holder">
        <a class   = "icon16 i_message"
           href    = "${h.url('messages',list='to')}"
           title   = "${_('Messages')}"
           onclick = "cb_frag($(this), '${h.url('messages', list='to'          , format='frag')}', 'frag_col_1'); return false;"
        ><span>${_('Messages')}</span>
        </a>
        ${messageIcon(c.logged_in_persona.num_unread_messages)}<br />
        <a class   = "icon16 i_notification"
           href    = "${h.url('messages',list='notification')}"
           title   = "${_('Notification')}"
           onclick = "cb_frag($(this), '${h.url('messages', list='notification', format='frag')}', 'frag_col_1'); return false;"
        ><span>${_('Notifications')}</span>
        </a>
        ${messageIcon(c.logged_in_persona.num_unread_notifications)}
      </div>
    </div>
    <table>
        <%def name="persona_select(member, **kwargs)">
            <%
                current_persona = member==c.logged_in_persona
            %>
            <tr
                % if current_persona:
                    class   = "current_persona"
                % else:
                    class   = "selectable"
                    ##onclick = "$(this).find('.persona_link').click();"
                    onclick = "$(this).find('form').submit();"
                % endif
            >
                <td>
                    <img src="${member.avatar_url}" alt="" onerror='this.onerror=null;this.src="/images/default/avatar.png"'/>
                </td>
                <td>
                    <p class="name">${member.name or member.username}</p>
                    % for k,v in kwargs.iteritems():
                        % if v:
                        <p class="info">${k.capitalize()}: ${str(v).capitalize()}</p>
                        % endif
                    % endfor
                </td>
                <td>
                  <a class   = "icon16 i_message"
                     href    = "${h.url('messages',list='to')}"
                     title   = "${_('Messages')}"
                     onclick = "cb_frag($(this), '${h.url('messages', list='to'          , format='frag')}', 'frag_col_1'); return false;"
                  ><span>${_('Messages')}</span>
                  </a>
                  ${messageIcon(member.num_unread_messages)}<br />
                  <a class   = "icon16 i_notification"
                     href    = "${h.url('messages',list='notification')}"
                     title   = "${_('Notifications')}"
                     onclick = "cb_frag($(this), '${h.url('messages', list='notification', format='frag')}', 'frag_col_1'); return false;"
                  ><span>${_('Notifications')}</span>
                  </a>
                  ${messageIcon(member.num_unread_notifications)}
                </td>
                <td class="hide_if_js">
                    % if not current_persona:
                    ${h.secure_link(
                        h.url(controller='account', action='set_persona', id=member.username, format='html') ,
                        ##args_to_tuple(
                        'swtich user',
                        css_class="persona_link",
                        ##json_form_complete_actions = 'window.location.replace(\'%s\');' % url(controller='profile', action='index', host=app_globals.site_host) ,
                        ## AllanC TODO: non javascript users need to be forwarded to there profile page
                    )}
                    % endif
                </td>
            </tr>
        </%def>
        
        <%
            num_members = None
            if hasattr(c.logged_in_persona, 'num_members'):
                num_members = c.logged_in_persona.num_members
        %>
        
        ${persona_select(c.logged_in_persona, role=c.logged_in_persona_role, members=num_members)}
        % if c.logged_in_user!=c.logged_in_persona:
            ${persona_select(c.logged_in_user)}
        % endif
        % for membership in [membership for membership in c.logged_in_user.groups_roles if membership.status=="active" and membership.group!=c.logged_in_persona]:
            ${persona_select(membership.group, role=membership.role, members=membership.group.num_members)}
        % endfor
    </table>

</div>


% endif

##------------------------------------------------------------------------------
## Home Link
##------------------------------------------------------------------------------

<%doc>
% if c.logged_in_persona:
<a id="home_link" href="${url(controller='profile', action='index')}">
% else:
<a id="home_link" href="/">
% endif
    <img src="/styles/common/icons32/home-icon.png" alt="${_('Home')}" width="32" height="24" />
</a>
</%doc>

##------------------------------------------------------------------------------
## Menu
##------------------------------------------------------------------------------
<nav class="menuh-container">
    
<div class="menuh">
    <ul>
        <li><a href="#" class="top_parent button">${_("Create")}</a>
        <ul>
            <li>${h.secure_link(h.url('new_content', target_type='assignment'), _("_Assignment"), css_class="sub_option")}</li>
            <li>${h.secure_link(h.url('new_content', target_type='article'   ), _("_Article")   , css_class="sub_option")}</li>
            <li><a href="${h.url('new_group')}" class="sub_option">${_("_Group")}</a></li>
        </ul>
        </li>
    </ul>

    <ul>
        <li><a href="#" class="top_parent button">${_("Explore")}</a>
        <ul>
            <!--<li><form action="${h.url('contents')}" method='GET'><input type="search" name="query" placeholder="${_("Quick Search")}"></form></li>-->
% if c.logged_in_persona:
<!--
            <li><a href="/feeds" class="parent">${_("News Feeds")}</a>
				<ul>
					% for f in c.logged_in_persona.feeds:
					<li><a href="/feeds/${f.id}" class="sub_option">${f.name}</a></li>
					% endfor
					<li><a href="/feeds/new" class="sub_option">${_("Create New Feed")}</a></li>
				</ul>
			</li>
-->
% endif
            <li><a href="/contents?list=assignments_active" class="sub_option">${_("_Assignments")}</a></li>
            <li><a href="/contents?list=articles"           class="sub_option">${_("_Articles")}</a></li>
            <li><a href="/members?type=user"                class="sub_option">${_("_Users")}</a></li>
            <li><a href="/members?type=group"               class="sub_option">${_("_Groups")}</a></li>
        </ul>
        </li>
    </ul>
% if c.logged_in_persona:
    <ul>
        <li><a href="#" class="top_parent button">${_("Manage")}</a>
        <ul>
            <li><a href="/profile"  class="sub_option">${_("Profile")}</a></li>
            <li><a href="/settings" class="sub_option">${_("Settings")}</a></li>
            ##<li><a href="/profile"  class="sub_option">${_("Content")}</a></li>
            ##<li><a href="/profile"  class="sub_option">${_("_Assignments")}</a></li>
            ##<li><a href="${url('member_action', id=c.logged_in_persona.username, action='groups')}"  class="sub_option">${_("My _Groups")}</a></li>
        </ul>
        </li>
    </ul>
% endif

</div>
</nav>

##------------------------------------------------------------------------------
## Search
##------------------------------------------------------------------------------
<div id="search">
	<form action="${h.url('contents')}" method='GET'>
		<input type="search" class="search_input" name="term" placeholder=" ${_("Search")}" />
		<input type="submit" class="button" value="GO">
	</form>
</div>


##------------------------------------------------------------------------------
## Logout
##------------------------------------------------------------------------------
<div id="signin">
% if c.logged_in_persona:
    ${h.secure_link(
        h.url(controller='account', action='signout'),
        _('Sign out'),
        css_class="button"
    )}
% else:
    <a class="button" href="${url(controller='account', action='signin')}">
        ##<img src="/styles/web/login.png" alt="${_("Log in")}" width="68" height="17">
        ${_('Sign in')}
    </a>
% endif
</div>
