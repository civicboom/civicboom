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
	    <div class="frag_list">
        <form class="form" id="form_search" action="${url('members')}" method="GET"
              onsubmit="cb_frag($(this), '/members.frag?' + $('#form_search').serialize(), 'frag_col_1'); return false;">
            <fieldset>
                <p><label for="term">Search for</label><br/>
                <input type="text" name="term" value="${kwargs.get('term')}" placeholder="Enter key words"/>

				<p><label for="type">Type</label><br>
				<select name="type">
                    <option value="">${_("_Users and _groups")}</option>
                    <option value="user">${_("Just _users")}</option>
                    <option value="group">${_("Just _groups")}</option>
				</select>

                <p><label for="sort">Order by</label><br/>
				<select name="sort">
					<option value="-id">Newest first</option>
					<option value="name">Display name</option>
				</select>

                <p>&nbsp;<br>
                <input type="submit" value="Search" class="button"/>
            </fieldset>
        </form>
		</div>
    </div>
</%def>
