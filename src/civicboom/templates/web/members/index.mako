<%inherit file="/web/common/frag_container.mako"/>

<%!
    frag_container_css_class  = 'frag_bridge' # bit of a hack here to get the search box half width to start with
%>

<%def name="title()">${_('Search _members')}</%def>

<%def name="body()">
    <% self.attr.frags = [show, list] %>
</%def>

<%def name="search()">
	<%include file="/frag/members/search.mako"/>
</%def>

<%def name="list()">
    <%include file="/frag/members/index.mako"/>
</%def>
