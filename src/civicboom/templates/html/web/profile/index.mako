<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="title()">${_("Profile")}</%def>

<%def name="body()">
	<%
        self.attr.frags = [profile, assignments, help]
        self.attr.frag_col_sizes = [2,1,1]
        self.attr.frag_classes   = [None, None, 'flag_help']
    %>
</%def>

<%def name="profile()">
	<%include file="/frag/members/show.mako"/>
</%def>

<%def name="help()">
    % if   d['member']['type'] == 'user':
	<!--#include file="/help/profile"-->
    % elif d['member']['type'] == 'group':
    <!--#include file="/help/group_persona"-->
    % endif
</%def>

<%def name="assignments()">
<!--#include file="${h.url('contents', format='frag', list='assignments_active')}"-->
</%def>