<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="title()">${_("Search members")}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <% self.attr.frags = search_members %>
</%def>

<%def name="search_members()">
    <%include file="/frag/misc/search_members.mako"/>
</%def>
