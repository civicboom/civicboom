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
        <form id="form_search" action="${url('members')}" method="GET"
              onsubmit="cb_frag($(this), '/members.frag?' + $('#form_search').serialize(), 'bridge'); return false;">
            <fieldset>
				<!--
                <legend>Search</legend>
                <br/>
				-->
                <% args, kwargs = c.web_params_to_kwargs %>
                Name: <input type="text" name="term" value="${kwargs.get('term')}"/>
                <br/>
                <input type="submit" value="Search" class="button"/>
            </fieldset>
        </form>
    </div>
</%def>
