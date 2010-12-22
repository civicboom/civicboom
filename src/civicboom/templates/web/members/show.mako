<%inherit file="/web/common/frag_container.mako"/>

<%namespace name="frag_member" file="/frag/members/show.mako"/>

##------------------------------------------------------------------------------
## RSS
##------------------------------------------------------------------------------
<%def name="rss()"      >${self.rss_header_link()}</%def>
<%def name="rss_url()"  >${url(controller='search', action='content', creator=d['member']['username'], format='rss')}</%def>
<%def name="rss_title()">Articles by ${d['member']['username']}</%def>


##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------

<%def name="title()">${d['member']['username']}</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
	${frag_member.frag_member(d)}
</%def>