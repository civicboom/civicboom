<%inherit file="/web/common/html_base.mako"/>

<%namespace name="frag_member" file="/frag/members/show.mako"/>

##------------------------------------------------------------------------------
## RSS
##------------------------------------------------------------------------------
<%def name="rss()">${self.rss_header_link()}</%def>
<%def name="rss_url()">${url(controller='search', action='content', creator=d['member']['username'], format='rss')}</%def>
<%def name="rss_title()">Articles by ${d['member']['username']}</%def>


##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------

<%def name="title()">${d['member']['username']}</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
    <div id='frag_containers'>
		## AllanC - see /web/contents/show.mako for more details about this call
		
		<div id="frag_" class="frag_container">
			${frag_member.frag_member(d)}
		</div>
		
    </div>
</%def>