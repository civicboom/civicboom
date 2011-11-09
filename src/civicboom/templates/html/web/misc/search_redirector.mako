<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="title()">${_("Search")}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <% self.attr.frags = [articles, assignments, members] %>
</%def>

<%def name="assignments()">
    <!--#include virtual="${h.url(controller='contents', action='index', format='frag', term=c.result['data']['term'], list='assignments_active')}"-->
</%def>

<%def name="articles()">
    <!--#include virtual="${h.url(controller='contents', action='index', format='frag', term=c.result['data']['term'], list='articles')}"-->
</%def>

<%def name="members()">
    <!--#include virtual="${h.url(controller='members', action='index', format='frag', term=c.result['data']['term'])}"-->
</%def>
