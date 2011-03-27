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
		self.attr.frags = [invite]
		self.attr.frag_col_sizes = [2]
		if invite_type == 'assignment':
			self.attr.frags.insert(0, content)
			self.attr.frag_col_sizes.insert(0, 2)
		endif
		if invite_type in ['group', 'trusted_follower']:
			self.attr.frags.insert(0, member)
			self.attr.frag_col_sizes.insert(0, 2)
		endif
	%>
</%def>

<%def name="invite()">
	<%include file="/frag/invite/index.mako"/>
</%def>

<%def name="content()">
	<%include file="/frag/contents/show.mako"/>
</%def>

<%def name="member()">
	<%include file="/frag/members/show.mako"/>
</%def>