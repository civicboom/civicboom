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
	<% args, kwargs = c.web_params_to_kwargs %>
    <div class="frag_col">
        <form class="form" id="form_search" action="${url('members')}" method="GET"
              onsubmit="cb_frag($(this), '/members.frag?' + $('#form_search').serialize(), 'frag_col_1'); return false;">
            <fieldset>
                <p><label for="term">Search for</label><br/>
                <input type="text" name="term" value="${kwargs.get('term')}" placeholder="Enter key words"/>

				<p><label for="type">Type</label><br>
				<select name="type">
                    <option value="">${_("_Users and _Groups")}</option>
                    <option value="user">${_("Just _Users")}</option>
                    <option value="group">${_("Just _Groups")}</option>
				</select>

                <p><label for="sort">Order by</label><br/>
				<select name="sort">
					<option value="-id">Newest First</option>
					<option value="name">Display Name</option>
				</select>

                <p>&nbsp;<br>
                <input type="submit" value="Search" class="button"/>
            </fieldset>
        </form>
    </div>
</%def>
