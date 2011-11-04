<%
    logged_in = c.logged_in_persona and c.logged_in_persona.status == 'active'
%>

##------------------------------------------------------------------------------
## Logo
##------------------------------------------------------------------------------
<h1 id="logo">
	<a href='/'>
		<img  class='logo_img'     src='${h.wh_url("public", "images/logo-v3-128x28.png")}'    alt='${_("_site_name")}' width="128" height="28"/>
		<span class='logo_text'>${_("_site_name")}</span>
	</a>
    <span class='beta_overlay'>beta</span>
</h1>

##------------------------------------------------------------------------------
## Content creation actions
##------------------------------------------------------------------------------
<nav id="actions">
	${h.secure_link(h.url('new_content', target_type='assignment'), _("Ask for stories"), css_class="button")}
	##${h.secure_link(h.url('new_content', target_type='article'   ), _("Post a story") , css_class="button")}
    <a href="${h.url(controller='misc', action='new_content')}" class="button">${_("Post a story")}</a>
</nav>

##------------------------------------------------------------------------------
## New Search (by Magical Shish)
##------------------------------------------------------------------------------
<div id="search">
    <form action="${url(controller='misc', action='search_redirector')}">
        <input type="search" name="term" placeholder="${_("Find _assignments, _articles and _members")}" class="search_input">
        <input type="submit" name="type" class="button b0" value="V">
## IMPORTANT!!! These need to match up with controllers/misc.py:search_redirector()
        <input type="submit" name="type" class="button b1" value="${_("_Assignments")}">
        <input type="submit" name="type" class="button b2" value="${_("_Articles")}">
        <input type="submit" name="type" class="button b3" value="${_("_Users / _Groups")}">
    </form>
</div>

##------------------------------------------------------------------------------
## Persona Switching
##------------------------------------------------------------------------------
  ## AllanC - must check status=active otherwise registration page keeps displaying 'unauthorised error' repeatedly
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
                        var jQe = $(icons[key]); 
                        //alert (icons[key].html());
                        jQe.html('&nbsp;' + data.data[key] + '&nbsp;');
                        if (data.data[key] == 0) {
                            jQe.css('display', 'none');
                        } else {
                            jQe.css('display', 'inline');
                        }
                        _total += (data.data[key] * 1);
                    }
                }
                if (typeof icons['_total'] != 'undefined') {
                    var jQe = $(icons['_total']);
                    jQe.html('&nbsp;' + _total + '&nbsp;');
                    if (_total == 0) {
                        jQe.css('display', 'none');
                    } else {
                        jQe.css('display', 'inline');
                    }
                }
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
        <div class="icon_overlay_red ${id}"
            % if messages == 0:
                style="display:none;"
            % endif
        >&nbsp;${messages}&nbsp;</div>
</%def>
<div id="persona_select">
    <div id="persona_holder" style="vertical-align: center;" onclick="window.location='/profile';">
      <a id="persona_avatar" href="${url(controller='profile', action='index')}"><!--
        --><img src="${c.logged_in_persona.avatar_url}" alt="${c.logged_in_persona.name}" onerror='this.onerror=null;this.src="/images/default/avatar_user.png"' /><!--
      --></a>
      <div id="persona_details">
        ${c.logged_in_persona.name}
      </div>
      <div id="message_holder">
        <a class   = "icon16 i_message"
           href    = "${h.url('messages',list='to')}"
           title   = "${_('Messages')}"
           onclick = "cb_frag($(this), '${h.url('messages', list='to'          , format='frag')}', 'frag_col_1'); return false;"
        ><span>${_('Messages')}</span>
        </a>
        ${messageIcon(c.logged_in_persona.num_unread_messages + c.logged_in_persona.num_unread_notifications, "msg_c_o")}
      </div>
    </div>
    <table>
        <tr>
            <td colspan="4">
                <a href="${h.url('settings')}" id="settings">${_('My settings')}</a>
                % if c.logged_in_persona_role == 'admin':
                    <span style="float:right;">
                    % if c.logged_in_persona.payment_account_id:
                        <a href="${h.url('payments')}">${_('My payment account')}</a>
                    % else:
                        <a href="${h.url('new_payment')}">${_('Upgrade your account')}</a>
                    % endif
                    </span>
                % endif
            </td>
        </tr>
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
                <td class="avatar">
                    <img src="${member.avatar_url}" alt="" onerror='this.onerror=null;this.src="/images/default/avatar_user.png"'/>
                </td>
                <td class="name">
                    <p class="name">${member.name or member.username}</p>
                    % for k,v in kwargs.iteritems():
                        % if v:
                        <p class="info">${_(k.capitalize())}: ${_(str(v).capitalize())}</p>
                        % endif
                    % endfor
                </td>
                <td class="messages">
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
            ${persona_select(c.logged_in_persona, role=c.logged_in_persona_role)}
            ## , members=num_members)}
        % endif
        ## Show currently logged in persona's groups:
        % for membership in [membership for membership in c.logged_in_persona.groups_roles if membership.status=="active" and membership.group!=c.logged_in_persona and membership.group!=c.logged_in_user]:
            ${persona_select(membership.group, role=membership.role)}
            ## , members=membership.group.num_members)}
        % endfor
        <tr class="extras selectable" onclick="window.location='/misc/what_is_a_hub';">
            <td class="avatar">
                <div style="position: relative;">
                    <img src="/images/default/avatar_group.png" alt=""/>
                    <a class="icon16 i_plus_bordered" style="position: absolute; bottom: 0px; right: 0px;"></a>
                </div>
            </td>
            <td class="name" colspan="2">
                <p class="name">${_("Create a _Group")}</p>
            </td>
        </tr>
        <tr class="extras">
            <td colspan="3" style="text-align: right;">
                ${h.secure_link(
                    h.url(controller='account', action='signout'),
                    _('Sign out')
                )}
            </td>
        </tr>
    </table>
</div>
% else:
    <div id="signin">
        <a class="button" href="${url(controller='account', action='signin')}">
            ##<img src="/styles/web/login.png" alt="${_("Log in")}" width="68" height="17">
            ${_('Sign in')}
        </a>
    </div>
% endif
