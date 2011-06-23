<%
    logged_in = c.logged_in_persona and c.logged_in_persona.status == 'active'
%>

##------------------------------------------------------------------------------
## Logo
##------------------------------------------------------------------------------
<h1 id="logo">
	<a href='/'>
		<img  class='logo_img'     src='${h.wh_url("public", "images/logo.png")}'              alt='${_("_site_name")}' />
        <img  class='beta_overlay' src='${h.wh_url("public", "images/logo_beta_overlay.png")}' alt='${_("Beta")}'       />
		<span class='logo_text'>${_("_site_name")}</span>
	</a>
</h1>

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
## Content creation actions
##------------------------------------------------------------------------------
<nav id="actions">
	${h.secure_link(h.url('new_content', target_type='assignment'), _("Make a request"), css_class="button")}
	${h.secure_link(h.url('new_content', target_type='article'   ), _("Post my story") , css_class="button")}
</nav>

##------------------------------------------------------------------------------
## Menu
##------------------------------------------------------------------------------
<%doc>
<nav class="menuh-container">
    
<div class="menuh">
	<ul>
		<li>${h.secure_link(h.url('new_content', target_type='assignment'), _("Make a request"), css_class="top_parent button")}</li>
	</ul>
	<ul>
		<li>${h.secure_link(h.url('new_content', target_type='article'   ), _("Post my story")   , css_class="top_parent button")}</li>
	</ul>
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
        <li><a href="#" class="top_parent buttonesque_link">${_("Explore...")}</a>
        <ul>
            <!--<li><form action="${h.url('contents')}" method='GET'><input type="search" name="query" placeholder="${_("Quick Search")}"></form></li>-->
% if logged_in:
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
            <!-- <li><a href="/members?type=user"                class="sub_option">${_("_Users")}</a></li>  -->
            <!-- <li><a href="/members?type=group"               class="sub_option">${_("_Groups")}</a></li> -->
            <li><a href="/members"                          class="sub_option">${_("_Members")}</a></li>
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
</%doc>

##------------------------------------------------------------------------------
## About Buttons
##------------------------------------------------------------------------------
<%doc>
<div id="aboutbtns">
    <a class="buttonesque_link" style="padding: 0 5px;" href="${url(controller='about', action='howto')}">
        ${_('How to')}
    </a>
    <a class="buttonesque_link" href="${url(controller='about', action='mobile')}">
        ${_('Mobile')}
    </a>
</div>
</%doc>

##------------------------------------------------------------------------------
## Search
##------------------------------------------------------------------------------
<%doc>
<div id="search">
	<form action="${h.url('contents')}" method='GET'>
		<input type="search" class="search_input" name="term" placeholder="${_("Search Content")}" />
		<input type="submit" class="button" value="GO">
	</form>
</div>
</%doc>


##------------------------------------------------------------------------------
## Logout
##------------------------------------------------------------------------------
##<div id="signin">
##% if c.logged_in_persona:
##    ${h.secure_link(
##        h.url(controller='account', action='signout'),
##        _('Sign out'),
##        css_class="button"
##    )}
##% else:
##    <a class="button" href="${url(controller='account', action='signin')}">
##        ##<img src="/styles/web/login.png" alt="${_("Log in")}" width="68" height="17">
##        ${_('Sign in')}
##    </a>
##% endif
##</div>

##------------------------------------------------------------------------------
## New Search (by Magical Shish)
##------------------------------------------------------------------------------
<div id="search">
    <form action="${url(controller='misc', action='search_redirector')}">
        <input type="search" name="term" placeholder="Search" class="search_input">
        <input type="submit" name="type" class="button b0" value="All">
        <input type="submit" name="type" class="button b1" value="Requests">
        <input type="submit" name="type" class="button b2" value="Stories">
        <input type="submit" name="type" class="button b3" value="Members">
    </form>
</div>

##------------------------------------------------------------------------------
## Persona Switching
##------------------------------------------------------------------------------
  ## AllanC - must check status=active otherwise registration page keeps displaying 'unauthroised error' repeatedly
% if logged_in:
<%
    from civicboom.model import Group
%>
<script type="text/javascript">
    var icons;
    function refreshMessages() {
        $.getJSON('/profile/messages.json',function(data) {
            if (typeof data['data'] != 'undefined') {
                var _total = 0;
                for (var key in icons) {
                    if (typeof data.data[key] != 'undefined') {
                        //alert (icons[key].html());
                        $(icons[key]).html('&nbsp;' + data.data[key] + '&nbsp;');
                        _total += (data.data[key] * 1);
                    }
                }
                if (typeof icons['_total'] != 'undefined')
                    $(icons['_total']).html('&nbsp;' + _total + '&nbsp;')
            }
        });
    }
    $(function() {
        icons = {num_unread_messages: '.msg_c_m',
                 num_unread_notifications: '.msg_c_n',
                 _total: '.msg_c_o'
                }
        setInterval(refreshMessages, 180000);
    });
</script>

<%def name="messageIcon(messages, id)">
    % if messages > 0:
        <div class="icon_overlay_red ${id}">&nbsp;${messages}&nbsp;</div>
    % endif
</%def>
<div id="persona_select_new">
    <ul>
        <li class="current_persona">
            <div class="persona_detail">
                <a class="name" href="${url(controller='profile', action='index')}">
                    <img src="${c.logged_in_persona.avatar_url}" onerror='this.onerror=null;this.src="/images/default/avatar.png"' />
                </a>
                ##RAR<br />
                ${c.logged_in_persona.name}
            </div>
            <div class="message_holder">
                <span class="icon16 i_blank"></span>
                ${messageIcon(c.logged_in_persona.num_unread_messages + c.logged_in_persona.num_unread_notifications, "msg_c_o")}
            </div>
        </li>
        
        <%def name="persona_new(member, **kwargs)">
            <%
                current_persona = member==c.logged_in_persona
            %>
            <li
                % if current_persona:
                    onclick = "window.location = '/profile';"
                % else:
                    onclick = "$(this).find('form').submit();"
                % endif
            class="hover">
                <div class="persona_detail">
                    <img src="${member.avatar_url}" onerror='this.onerror=null;this.src="/images/default/avatar.png"' />
                    ${member.name}
                </div>
                <div class="message_holder">
                        <a class   = "icon16 i_message"
                           href    = "${h.url('messages',list='to')}"
                           title   = "${_('Messages')}"
                           onclick = "cb_frag($(this), '${h.url('messages', list='to'          , format='frag')}', 'frag_col_1'); return false;"
                        ><span>${_('Messages')}</span>
                        </a>
                        ${messageIcon(member.num_unread_messages, "msg_%s_m" % ('c' if current_persona else member.id))}
                        <br />
                        <a class   = "icon16 i_notification"
                           href    = "${h.url('messages',list='notification')}"
                           title   = "${_('Notifications')}"
                           onclick = "cb_frag($(this), '${h.url('messages', list='notification', format='frag')}', 'frag_col_1'); return false;"
                        ><span>${_('Notifications')}</span>
                        </a>
                        ${messageIcon(member.num_unread_notifications, "msg_%s_n" % ('c' if current_persona else member.id))}
                </div>
            </li>
        </%def>
        ## Show default persona (the user logged in)
        ${persona_new(c.logged_in_user)}
        ## Show current persona (current group persona if applicable)
        % if c.logged_in_persona != c.logged_in_user:
            ${persona_new(c.logged_in_persona, role=c.logged_in_persona_role, members=num_members)}
        % endif
        ## Show currently logged in persona's groups:
        % for membership in [membership for membership in c.logged_in_persona.groups_roles if membership.status=="active" and membership.group!=c.logged_in_persona and membership.group!=c.logged_in_user]:
            ${persona_new(membership.group, role=membership.role, members=membership.group.num_members)}
        % endfor
    </ul>
</div>

<div id="persona_select">
    <div id="persona_holder" style="vertical-align: center;">
      <a class="name" href="${url(controller='profile', action='index')}"><!--
        --><img src="${c.logged_in_persona.avatar_url}" alt="${c.logged_in_persona.name}" onerror='this.onerror=null;this.src="/images/default/avatar.png"' /><!--
      --></a>
      <div id="persona_details" class="name">
        ${c.logged_in_persona.name}
      </div>
      <div id="message_holder">
##        <a class   = "icon16 i_message"
##           href    = "${h.url('messages',list='to')}"
##           title   = "${_('Messages')}"
##           onclick = "cb_frag($(this), '${h.url('messages', list='to'          , format='frag')}', 'frag_col_1'); return false;"
##        ><span>${_('Messages')}</span>
        </a>
        ${messageIcon(c.logged_in_persona.num_unread_messages + c.logged_in_persona.num_unread_notifications, "msg_c_o")}
      </div>
    </div>
    <table>
        <%def name="persona_select(member, **kwargs)">
            <%
                current_persona = member==c.logged_in_persona
            %>
            <tr
                % if current_persona:
                    class   = "current_persona selectable"
                    onclick = "window.location = '/profile';"
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
                    % if current_persona:
                        <p>
                            <a href="${h.url('settings')}" id="settings">${_('My settings')}</a>
                        </p>
                    % endif
                </td>
                <td>
                  <a class   = "icon16 i_message"
                     href    = "${h.url('messages',list='to')}"
                     title   = "${_('Messages')}"
                     onclick = "cb_frag($(this), '${h.url('messages', list='to'          , format='frag')}', 'frag_col_1'); return false;"
                  ><span>${_('Messages')}</span>
                  </a>
                  ${messageIcon(member.num_unread_messages, "msg_%s_m" % ('c' if current_persona else member.id))}<br />
                  <a class   = "icon16 i_notification"
                     href    = "${h.url('messages',list='notification')}"
                     title   = "${_('Notifications')}"
                     onclick = "cb_frag($(this), '${h.url('messages', list='notification', format='frag')}', 'frag_col_1'); return false;"
                  ><span>${_('Notifications')}</span>
                  </a>
                  ${messageIcon(member.num_unread_notifications, "msg_%s_n" % ('c' if current_persona else member.id))}
                </td>
                <td class="hide_if_js">
                    % if not current_persona:
                    ${h.secure_link(
                        h.url(controller='account', action='set_persona', id=member.username, format='html') ,
                        ##args_to_tuple(
                        'switch user',
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
        
        ## Show default persona (the user logged in)
        ${persona_select(c.logged_in_user)}
        ## Show current persona (current group persona if applicable)
        % if c.logged_in_persona != c.logged_in_user:
            ${persona_select(c.logged_in_persona, role=c.logged_in_persona_role, members=num_members)}
        % endif
        ## Show currently logged in persona's groups:
        % for membership in [membership for membership in c.logged_in_persona.groups_roles if membership.status=="active" and membership.group!=c.logged_in_persona and membership.group!=c.logged_in_user]:
            ${persona_select(membership.group, role=membership.role, members=membership.group.num_members)}
        % endfor
        <tr>
            <td colspan="4">
                ${h.secure_link(
                    h.url(controller='account', action='signout'),
                    _('Sign out'),
                    css_class="button"
                )}
            </td>
        </tr>
    </table>
</div>
% endif
