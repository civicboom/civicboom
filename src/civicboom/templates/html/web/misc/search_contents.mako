<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="title()">${_("Search contents")}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <% self.attr.frags = search_contents %>
</%def>

<%def name="search_contents()">
    <%include file="/frag/misc/search_contents.mako"/>
</%def>
