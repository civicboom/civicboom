<%inherit file="/html/web/common/frag_container.mako"/>


##------------------------------------------------------------------------------
## RSS
##------------------------------------------------------------------------------
<%def name="rss()"      >${self.rss_header_link()}</%def>
<%def name="rss_url()"  >${url(controller='search', action='content', creator=d['member']['username'], format='rss')}</%def>
<%def name="rss_title()">Articles by ${d['member']['username']}</%def>


##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------

<%def name="title()">${d['member']['name'] or d['member']['username']}</%def>
<%def name="description()">${h.strip_html_tags(d['member']['description'] or '')[:300]}</%def>
<%def name="breadcrumbs()">
<span itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
	<a href="${h.url('members')}" itemprop="url"><span itemprop="title">Members</span></a>
</span>
&rarr;
<span itemscope itemtype="http://data-vocabulary.org/Breadcrumb">
<%
_mtype = "_%ss" % d['member']['type'].capitalize()
%>
	<a href="${h.url('members', type=d['member']['type'])}" itemprop="url"><span itemprop="title">${_(_mtype)}</span></a>
</span>
</%def>



##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
	<% self.attr.frags = member %>
</%def>

<%def name="member()">
	<%include file="/frag/members/show.mako"/>
</%def>
