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
        <form class="form search" id="form_search" action="${url('members')}" method="GET"
            data-frag="${h.url('members', format='frag')}">
            <fieldset>
                <p><label for="term">${_("Search for")}</label><br/>
                <input type="text" name="term" value="${kwargs.get('term')}" placeholder="${_("Enter key words")}"/>

				<p><label for="type">${_("Type")}</label><br>
				<select name="type">
                    <option value="">${_("_Users and _groups")}</option>
                    <option value="user">${_("Just _users")}</option>
                    <option value="group">${_("Just _groups")}</option>
				</select>

                <p><label for="sort">${_("Order by")}</label><br/>
				<select name="sort">
					<option value="-id">${_("Newest first")}</option>
					<option value="name">${_("Display name")}</option>
				</select>

                <p>&nbsp;<br>
                <input type="submit" value="${_("Search")}" class="button"/>
            </fieldset>
        </form>
		</div>
    </div>
</%def>
