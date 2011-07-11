<%inherit file="/html/web/common/frag_container.mako"/>


##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------

<%def name="title()">${_('Featured Content')}</%def>
<%def name="description()">${_("Highlights of what's happening now on _site_name")}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <% self.attr.frags = content %>
</%def>

<%def name="content()">
    <%include file="/frag/misc/featured.mako"/>
</%def>
