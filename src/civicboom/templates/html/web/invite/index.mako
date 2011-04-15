<%inherit file="/html/web/common/frag_container.mako"/>


##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------

<%def name="title()">${_('Invite')}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
	<%
		invite_type = d.get('invite')
		self.attr.frags = [frag, invite]
		self.attr.frag_col_sizes = [2, 2]
		
		if invite_type == 'assignment':
			self.attr.frag_url = h.url('content', action='show', id=d['id'], invite=d['invite'], format='frag')
		endif
		if invite_type in ['group', 'trusted_follower']:
			self.attr.frag_url = h.url('member', action='show', id=d['id'], invite=d['invite'], format='frag')
		endif
	%>
</%def>

<%def name="invite()">
	<%include file="/frag/invite/index.mako"/>
</%def>

<%def name="frag()">
	<!--#include file="${self.attr.frag_url}"-->
</%def>