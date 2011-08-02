<%inherit file="/html/web/common/html_base.mako"/>

<%namespace name="member_includes"  file="/html/web/common/member.mako"       />
<%namespace name="content_includes" file="/html/web/common/content_list.mako" />


<%def name="body()">

    <%
        from civicboom.model.member import group_member_roles, group_join_mode, group_member_visibility, group_content_visibility
        
        permission_edit        = 'edit'        in d['actions']
        permission_set_role    = 'set_role'    in d['actions']
        permission_remove      = 'remove'      in d['actions']
        permission_remove_self = 'remove_self' in d['actions']
        show_join_button       = 'join'        in d['actions']
        
        group = d['member']
    %>


    ${member_includes.avatar(group , show_name=True, show_follow_button=True, show_join_button=show_join_button)}
    
    % if permission_edit:
        <a href="${h.url('edit_group', id=group['username'])}">edit</a>
    % endif
    
    <h2>Details</h2>
    <p>full name ${group['name']}</p>
    <p>default_role ${group['default_role']}</p>
    <p>member_visibility ${group['member_visibility']}</p>
    <p>default_content_visibility ${group['default_content_visibility']}</p>
    <p>join_mode ${group['join_mode']}</p>
    
    
    <h2>Members</h2>
    
    % if group['member_visibility']=="private" and not d['members']:
        <p>${_("Members are private")}</p>
    % else:
        ## members are public
        <%
            member_status = ['active', 'invite', 'request']
            members = {}
            for status in member_status:
                members[status] = [member for member in d['members'] if member['status']==status]
        %>
        % for status in member_status:
            % if len(members[status])>0:
                <h3>${_(status)}</h3>
                <ul>
                % for member in members[status]:
                    <li>
                        ${member['name']} (${member['username']}) [${_(member['role'])}]
                        % if permission_set_role:
                            ${h.form(h.url('group_action', id=group['id'], action='set_role', format='redirect'), method='post')}
                                <input type="hidden" name="member" value="${member['username']}"/>
                                % if member['status']=='active':
                                        ${h.html.select('role', member['role'], group_member_roles.enums)}
                                        <input type="submit" name="submit" value="${_('Set role')}"/>
                                % elif member['status']=='request':
                                        <input type="hidden" name="role"   value=""/>
                                        <input type="submit" name="submit" value="${_('Accept join request')}"/>
                                % endif
                            ${h.end_form()}
                        % endif
                        % if c.logged_in_persona and ((c.logged_in_persona.username == member['username'] and permission_remove_self) or (c.logged_in_persona.username != member['username'] and permission_remove)):
                            ${h.form(h.url('group_action', id=group['id'], action='remove_member', format='redirect'), method='post')}
                                <input type="hidden" name="member" value="${member['username']}"/>
                                <input type="submit" name="submit" value="${_('Remove')}"/>
                            ${h.end_form()}
                        % endif
                    </li>
                % endfor
                </ul>
            % endif
        % endfor
    % endif
    
    <h2>${_("Followers")}</h2>
    ${member_includes.member_list(d['followers'], show_avatar=False, show_name=True)}
</%def>
