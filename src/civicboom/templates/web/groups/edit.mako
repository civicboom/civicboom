<%inherit file="/web/common/html_base.mako"/>




<%def name="body()">

    <%
        from civicboom.model.member import group_member_roles, group_join_mode, group_member_visability, group_content_visability
        
        def get_param(name):
            if 'group' in d and name in d['group']:
                param = d['group'][name]
                if isinstance(param, basestring):
                    return param
                elif 'value' in param:
                    return param['value']
            return ''
    %>

    <%def name="show_error(name)">
        % if 'group' in d and name in d['group'] and 'error' in d['group'][name]:
            <span class="error-message">${d['group'][name]['error']}</span>
        % endif
    </%def>

    <%
        if 'action' not in d:
            d['action'] = 'create'
    %>

    % if d['action']=='edit' and 'group' in d:
        ## Editing Form
        ${h.form(h.url('group', id=get_param('id')), method='put')}
    % else:
        ## Creating Form
        ${h.form(h.url('groups', ), method='post')}
    % endif

    ##${d}
    
    <fieldset><legend>Group</legend>
        
        Groupname:
        % if d['action'] == "create":
            <input type="text" name="username" value="${get_param('username')}"/>
            ${show_error('username')}
        % else:
            ${get_param('username')}
        % endif
        
        Full Name:<input type="text" name="name" value="${get_param('name')}"/>
        ${show_error('name')}
        
        Description:<input type="text" name="description" value="${get_param('description')}"/>
        ${show_error('description')}
        
        <br/>
        
        ${_("default member role")}
        ${h.html.select('default_role', get_param('default_role'), group_member_roles.enums)}
        ${show_error('default_role')}
        
        <br/>
        
        ${_("join mode")}
        ${h.html.select('join_mode', get_param('join_mode'), group_join_mode.enums)}
        ${show_error('join_mode')}
        
        <br/>
        
        ${_("member visability")}
        ${h.html.select('member_visability', get_param('member_visability'), group_member_visability.enums)}
        ${show_error('member_visability')}
        
        <br/>
        
        ${_("default content visability")}
        ${h.html.select('default_content_visability', get_param('default_content_visability'), group_content_visability.enums)}
        ${show_error('default_content_visability')}
        
    </fieldset>
    
    <input type="submit" name="submit" value="${_('Submit')}"/>
    ${h.end_form()}
</%def>


<%doc>
    Radio button temp example
    <%
    if ():
        type_selected = "checked='checked' "
    else:
        type_selected = ""
    %>
    ##<option value="${newsarticle_type.id}" ${type_selected}>${newsarticle_type.type}</option>
    <input type="radio" name="newsarticle_type" value="${newsarticle_type.id}" ${type_selected}/>${newsarticle_type.type}</a>
</%doc>