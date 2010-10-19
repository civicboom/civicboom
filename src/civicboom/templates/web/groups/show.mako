<%inherit file="/web/common/html_base.mako"/>

<%namespace name="member_includes"  file="/web/common/member.mako"       />
<%namespace name="content_includes" file="/web/common/content_list.mako" />


##<%def name="col_left()">
##</%def>

##<%def name="col_right()">
##</%def>

<%def name="body()">

    <%
        from civicboom.model.member import group_member_roles, group_join_mode, group_member_visability, group_content_visability
        
        permission_set_role    = 'set_role'    in d['group']['actions']
        permission_remove      = 'remove'      in d['group']['actions']
        permission_remove_self = 'remove_self' in d['group']['actions']
        show_join_button       = 'join'        in d['group']['actions']
    %>


    ${member_includes.avatar(d['group'] , show_name=True, show_follow_button=True, show_join_button=show_join_button)}
    
    
    <h2>deatails</h2>
    <p>full name ${d['group']['name']}</p>
    <p>default_role ${d['group']['default_role']}</p>
    <p>member_visability ${d['group']['member_visability']}</p>
    <p>default_content_visability ${d['group']['default_content_visability']}</p>
    <p>join_mode ${d['group']['join_mode']}</p>
    
    
    <h2>Members</h2>
    ##${member_includes.member_list(d['group']['members'], show_avatar=False, show_name=True, class_="avatar_thumbnail_list")}
    
    % if d['group']['member_visability']=="private" and not d['group']['members']:
        <p>members are private</p>
    % else:
        <ul>
        % for member in d['group']['members']:
            <li>
                ${member['name']} (${member['username']}) [${member['role']}]
                % if permission_set_role:
                    ${h.form(h.url('group_action', id=d['group']['id'], action='set_role'), method='post')}
                        <input type="hidden" name="member" value="${member['username']}"/>
                        ${h.html.select('role', member['role'], group_member_roles.enums)}
                        <input type="submit" name="submit" value="${_('Set role')}"/>
                    ${h.end_form()}
                % endif
                % if c.logged_in_user and (c.logged_in_user.username == member['username'] and permission_remove_self) or (c.logged_in_user.username != member['username'] and permission_remove):
                    ${h.form(h.url('group_action', id=d['group']['id'], action='remove_member'), method='post')}
                        <input type="hidden" name="member" value="${member['username']}"/>
                        <input type="submit" name="submit" value="${_('Remove')}"/>
                    ${h.end_form()}
                % endif
            </li>
        % endfor
        </ul>
    % endif
    
    <h2>Followers</h2>
    ${member_includes.member_list(d['group']['followers'], show_avatar=False, show_name=True)}


</%def>