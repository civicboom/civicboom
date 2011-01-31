<%inherit file="/html/web/common/frag_container.mako"/>

<%!
    ##frag_container_css_class  = 'frag_bridge' # bit of a hack here to get the search box half width to start with
    frag_col_sizes = [1,1]
%>

<%def name="title()">${_('Search _members')}</%def>

<%def name="body()">
    <% self.attr.frags = [search, list] %>
</%def>

<%def name="search()">
	<%include file="/frag/members/search.mako"/>
</%def>

<%def name="list()">
    <%include file="/frag/members/index.mako"/>
</%def>
