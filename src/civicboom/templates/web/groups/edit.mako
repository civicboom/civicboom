<%inherit file="/web/common/frag_container.mako"/>

<%namespace name="frag" file="/frag/common/frag.mako"/>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <%
        self.attr.frags = group
        if c.action == 'new':
            self.attr.frags = [group, quick_group]
    %>
</%def>


##------------------------------------------------------------------------------
## new/edit group
##------------------------------------------------------------------------------

<%def name="group()">
    ${frag.frag_basic(title=_('%s group') % c.action.capitalize(), icon='group', frag_content=group_content)}
</%def>
<%def name="group_content()">
    <%
        from civicboom.model.member import group_member_roles, group_join_mode, group_member_visibility, group_content_visibility
        
        def get_param(name):
            if 'group' in d and name in d['group']:
                return d['group'][name]
            return ''
    %>
    <%def name="show_error(name)">
        ##% if 'group' in d and name in d['group'] and 'error' in d['group'][name]:
        % if 'invalid' in d and name in d['invalid']:
            <span class="error-message">${d['invalid'][name]}</span>
        % endif
    </%def>



    ## Setup Form
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


    
    <fieldset>
		<!--<legend>${_("Group")}</legend>-->
        
		<table class='form formpage border'>
			<tr class='title_bar'>
				<th colspan="2">${_("Group Settings")}</th>
			</tr>
			<tr>
				<td>${_("Group Name")}</td>
				<td>
		<input type="text" name="name" value="${get_param('name')}"/>
        ${show_error('name')}
				</td>
			</tr>
			<tr>
				<td>${_("Description")}</td>
				<td>
		<input type="text" name="description" value="${get_param('description')}"/>
        ${show_error('description')}
				</td>
			</tr>
			<tr>
				<td>${_("Default member role")}</td>
				<td>
        ${h.html.select('default_role', get_param('default_role'), group_member_roles.enums)}
        ${show_error('default_role')}
				</td>
			</tr>
			<tr>
				<td>${_("Join mode")}</td>
				<td>
        ${h.html.select('join_mode', get_param('join_mode'), group_join_mode.enums)}
        ${show_error('join_mode')}
				</td>
			</tr>
			<tr>
				<td>${_("Member visibility")}</td>
				<td>
        ${h.html.select('member_visibility', get_param('member_visibility'), group_member_visibility.enums)}
        ${show_error('member_visibility')}
				</td>
			</tr>
			<tr>
				<td>${_("Default content visibility")}</td>
				<td>
        ${h.html.select('default_content_visibility', get_param('default_content_visibility'), group_content_visibility.enums)}
        ${show_error('default_content_visibility')}
				</td>
			</tr>
			<tr>
				<td colspan="2">
				% if d['action']=='edit':
					<input type="submit" name="submit" value="${_('Save Group')}" class="button" />
				% else:
					<input type="submit" name="submit" value="${_('Create Group')}" class="button" />
				% endif
				</td>
			</tr>
        </table>
    </fieldset>
    
    ${h.end_form()}
</%def>


##------------------------------------------------------------------------------
## Quick group
##------------------------------------------------------------------------------

<%def name="quick_group()">
    ${frag.frag_basic(title=_('Quick group'), icon='group', frag_content=quick_group_content)}
</%def>
<%def name="quick_group_content()">

</%def>


##------------------------------------------------------------------------------
## Deprication
##------------------------------------------------------------------------------

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
