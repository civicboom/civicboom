<%inherit file="../base_email.mako"/>

<%def name="body()">
    
    <h1>New Members Summary</h1>
    <p>Since ${timedelta}</p>
    
    ##--------------------------------------------------------------------------
    
    <h2>Users</h2>
    <ul>
    % for user in [member for member in members if member.__type__ == 'user']:
        <li>
            <a href="${user.__link__()}">${user}</a>: ${user.join_date}
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
                <li><a href="${member.__link__()}">${member}</a>: ${role}</li>
            % endfor
            </ul>
        </li>
    % endfor
    </ul>
    
</%def>