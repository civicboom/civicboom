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

<%def name="title()">${d['member']['name']} [${d['member']['username']}]</%def>
<%def name="description()">${h.strip_html_tags(d['member']['description'])[:300]}</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
	<% self.attr.frags = member %>
</%def>

<%def name="member()">
	<%include file="/frag/members/show.mako"/>
</%def>
