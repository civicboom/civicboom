<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="title()">${_("New _article")}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <% self.attr.frags = new_article %>
</%def>

<%def name="new_article()">
    ##<!--#include virtual="${h.url(controller='misc', action='new_article', format='frag')}"-->
    <%include file="/frag/misc/new_article.mako"/>
</%def>