<%inherit file="/html/web/common/frag_container.mako"/>

<%!
    ##frag_container_css_class  = 'frag_bridge' # bit of a hack here to get the search box half width to start with
    frag_col_sizes = [1,2]
%>


##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------

<%def name="title()">${_('Search _content')}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------



<%def name="body()">
    <% self.attr.frags = [search, list] %>
</%def>

<%def name="search()">
<% args, kwargs = c.web_params_to_kwargs %>
<!--#include virtual="${h.url(controller='misc', action='search_contents', format='frag', **kwargs)}"-->
</%def>

<%def name="list()">
    <%include file="/frag/contents/index.mako"/>
</%def>