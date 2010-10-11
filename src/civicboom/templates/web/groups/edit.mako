<%inherit file="/web/common/layout_3cols.mako"/>

<% from civicboom.model.member import group_member_roles, group_join_mode, group_member_visability, group_content_visability %>


<%def name="col_left()">
</%def>

<%def name="col_right()">
</%def>

<%def name="body()">
    ${h.form(h.url('setting', id='None'), method='put')}
    
    <fieldset><legend>Group</legend>
        Name:<input type="text" name="name" value=""/>
        
        <br/>
        
        ${_("default member role")}
        ${h.select('default_member_role', None, group_member_roles)}
        
        <br/>
        
        ${_("join mode")}
        ${h.select('join_mode', None, group_join_mode)}
        
        <br/>
        
        ${_("member visability")}
        ${h.select('member_visability', None, group_member_visability)}
        
        <br/>
        
        ${_("content visability")}
        ${h.select('content_visability', None, group_content_visability)}
        
        
    </fieldset>
    
    <input type="submit" name="submit" value="${_('Submit')}"/>
    ${h.end_form()}
</%def>

<%def name="select(list, selected)">

</%def>


					  %if c.edit_report:
					  	${h.select('category',str(c.article.CatId), c.select_categories)}
					  %else:
					  	${h.select('category', None, c.select_categories)}
					  %endif

								<%
								if (hasattr(c.article, "newsarticle_type") and newsarticle_type == c.article.newsarticle_type) \
									 or \
									 ((not hasattr(c.article, "newsarticle_type")) and newsarticle_type == c.newsarticle_types[0]):
									type_selected = "checked='checked' "
								else:
									type_selected = ""
								%>
								##<option value="${newsarticle_type.id}" ${type_selected}>${newsarticle_type.type}</option>
								<input type="radio" name="newsarticle_type" value="${newsarticle_type.id}" ${type_selected}/>${newsarticle_type.type}</a>