<%inherit file="/web/common/layout_3cols.mako"/>



<%def name="col_left()">
</%def>

<%def name="col_right()">
</%def>

<%def name="body()">

    <% from civicboom.model.member import group_member_roles, group_join_mode, group_member_visability, group_content_visability %>

    ${h.form(h.url('setting', id='None'), method='put')}
    
    <fieldset><legend>Group</legend>
        Name:<input type="text" name="name" value=""/>
        
        <br/>
        
        ${_("default member role")}
        ${h.html.select('default_member_role', None, group_member_roles.enums)}
        
        <br/>
        
        ${_("join mode")}
        ${h.html.select('join_mode', None, group_join_mode.enums)}
        
        <br/>
        
        ${_("member visability")}
        ${h.html.select('member_visability', None, group_member_visability.enums)}
        
        <br/>
        
        ${_("content visability")}
        ${h.html.select('content_visability', None, group_content_visability.enums)}
        
        
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