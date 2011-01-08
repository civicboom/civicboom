<%inherit file="/frag/common/frag.mako"/>

<%namespace name="loc" file="/web/common/location.mako"/>

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
        <form id="form_search" action="${url('contents')}" method="GET"
              onsubmit="cb_frag($(this), '/contents.frag?' + $('#form_search').serialize(), 'bridge'); return false;">
            <fieldset>
				<!--
                <legend>Search</legend>
                <br/>
				-->
                <% args, kwargs = c.web_params_to_kwargs %>
                Text: <input type="text" name="query" value="${kwargs.get('query')}"/>
                <br/>
                Location: ${loc.location_picker()}
                <br/>
                <input type="submit" value="Search" class="button"/>
            </fieldset>
        </form>
    </div>
</%def>
