<%inherit file="/html/web/common/frag_container.mako"/>

<%namespace name="frag"       file="/frag/common/frag.mako"       />
<%namespace name="frag_lists" file="/frag/common/frag_lists.mako" />

<%def name="title()">${_("Search")}</%def>

<%def name="body()">
    <% self.attr.frags = search_summary %>
</%def>

<%def name="search_summary()">
    ${frag.frag_basic(title=_('Search summary'), icon='search', frag_content=search_summary_, include_white_background=False)}
</%def>

<%def name="search_summary_()">
    ${frag_lists.content_list(
        d['assignments'],
        _("_Assignments"),
        #creator=True
        hide_if_empty=False,
    )}
    ${frag_lists.content_list(
        d['articles'],
        _("_Articles"),
        #creator=True
        hide_if_empty=False,
    )}
    ${frag_lists.member_list(
        d['members'],
        _("_Users / _Groups"),
        hide_if_empty=False,
    )}
</%def>







##--------- Old ass stuff ------------------------------------------------------
<%doc>

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

</%doc>