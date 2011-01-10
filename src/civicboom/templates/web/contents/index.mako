<%inherit file="/web/common/frag_container.mako"/>

<%!
    frag_container_css_class  = 'frag_bridge' # bit of a hack here to get the search box half width to start with
%>


##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------

<%def name="title()">${_('Search')}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------



<%def name="body()">
    <% self.attr.frags = [search, list] %>
</%def>

<%def name="search()">
	<%include file="/frag/contents/search.mako"/>
</%def>
<%def name="list()">
    <%include file="/frag/contents/index.mako"/>
</%def>