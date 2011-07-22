<%inherit file="../base_email.mako"/>

<%def name="body()">
    
    <h1>New Members Summary</h1>
    <p>Since ${timedelta}</p>

    ##--------------------------------------------------------------------------
    <%def name="member_link(member)">\
        <a href="${member.__link__()}">${member}</a>\
        % if hasattr(member, 'email_normalized'):
        (<a href="mailto:${member.email_normalized}?Subject=${_('_site_name')}">${member.email_normalized}</a>)\
        % endif
    </%def>
    
    ##--------------------------------------------------------------------------
    
    <h2>Users</h2>
    <ul>
    % for user in [member for member in members if member.__type__ == 'user']:
        <li>
            ${member_link(user)}: ${user.join_date}
        </li>
    % endfor
    </ul>
    
    ##--------------------------------------------------------------------------
    
    <h2>Groups</h2>
    <ul>
    % for group in [member for member in members if member.__type__ == 'group']:
        <li>
            <a href="${group.__link__()}">${group}</a>: ${group.join_date}
            <ul>
            % for member, role in [(mr.member, mr.role) for mr in group.members_roles]:
                <li>${member_link(member)}: ${role}</li>
            % endfor
            </ul>
        </li>
    % endfor
    </ul>
    
</%def>
