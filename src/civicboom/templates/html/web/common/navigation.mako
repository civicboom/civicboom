% if c.logged_in_persona:

<div class="persona_select menuh">
    <ul><li>
        <a class="name" href="${url(controller='profile', action='index')}">${c.logged_in_persona.name}</a>
        <ul>
            <li>
                <img src="${c.logged_in_user.avatar_url}"/>
                ${h.secure_link(url(controller='account', action='set_persona', id=c.logged_in_user.username, format='redirect'), "%s" % (c.logged_in_user.username))}
            </li>
            % for membership in [membership for membership in c.logged_in_user.groups_roles if membership.status=="active"]:
            <li>
                <img src="${membership.group.avatar_url}"/>
                ${h.secure_link(url(controller='account', action='set_persona', id=membership.group.username, format='redirect'), "%s:%s" % (membership.group.name, membership.role))}
            </li>
            % endfor
        </ul>
    </li><ul>
</div>

<a class="role">${c.logged_in_persona_role}</a>

<%
msg_count = c.logged_in_persona.num_unread_messages
if msg_count > 0:
	n = " [%d]" % msg_count
else:
	n = ""
%>
<a class="messages" href="${url('messages')}">${_("messages")+n}</a>

${h.secure_link(url(controller='account', action='signout'), "Log Out", css_class="logout")}
% else:
<a class="login" href="${url(controller='account', action='signin')}"><img src="/styles/web/login.png" alt="${_("Log in")}" width="68" height="17"></a>
% endif
