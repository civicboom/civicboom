<%inherit file="/frag/common/frag.mako"/>

<%namespace name="loc" file="/html/web/common/location.mako"/>


<%!
    import civicboom.lib.constants as constants
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
		<form class="form search" id="form_search" action="${url('contents')}" method="get"
		  ## update current frag with new search 
	      data-frag="${h.url(controller='misc', action='search_contents', format='frag')}"
	      data-frag-new="${h.url('contents', format='frag')}">
            <fieldset>
				<p><label>${_("Search for")}</label><br>
                <input type="search" name="term" placeholder="${_("Enter key words")}" value="${kwargs.get('term')}"/>

				<p><label>${_("Type")}</label><br>
				<select name="list" style="width: 100%;">
				<%
				types = [
					("all",                  _("All _content")),
					("assignments_active",   _("_Assignments")),
					("responses",            _("_Responses")),
					("articles",             _("_Articles")),
					("assignments_previous", _("Past _assignments")),
				]
				%>
                % for list, name in types:
                    <% checked = 'selected' if (kwargs.get('list') == list) else '' %>
                    <option value="${list}" ${checked}>${name}</option>
                % endfor
				</select>

                <p><label>${_("Near to")}</label>
                ${loc.location_picker(width='100%', height="213px")}

                <p>&nbsp;<br>
				<input type="submit" value="${_("Search")}" class="button"/>
            </fieldset>
        </form>
	    </div>
    </div>
</%def>
