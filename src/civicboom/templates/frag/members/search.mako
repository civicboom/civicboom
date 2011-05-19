<%inherit file="/frag/common/frag.mako"/>

<%namespace name="loc" file="/html/web/common/location.mako"/>

<%!
    rss_url = False
%>

##------------------------------------------------------------------------------
## Variables
##------------------------------------------------------------------------------

<%def name="init_vars()">
    <%
        self.attr.title     = _('Search')
        self.attr.icon_type = 'search'
        
        self.attr.frag_data_css_class = 'frag_search'
    %>
</%def>


##------------------------------------------------------------------------------
## Content Fragment
##------------------------------------------------------------------------------
<%def name="body()">
    <div class="frag_col">
        <form id="form_search" action="${url('members')}" method="GET"
              onsubmit="cb_frag($(this), '/members.frag?' + $('#form_search').serialize(), 'frag_col_1'); return false;">
            <fieldset>
				<!--
                <legend>Search</legend>
                <br/>
				-->
                <% args, kwargs = c.web_params_to_kwargs %>
                <p><label for="term">Name</label><br/>
                <input type="text" style="width: 210px" name="term" value="${kwargs.get('term')}"/>

                <p><label for="sort">Order By</label><br/>
				<select name="sort" style="width: 100%;">
					<option value="-id">Join Date</option>
					<option value="name">Name</option>
				</select>

                <p>&nbsp;<br>
                <input type="submit" value="Search" class="button" style="width: 100%;"/>
            </fieldset>
        </form>
    </div>
</%def>
