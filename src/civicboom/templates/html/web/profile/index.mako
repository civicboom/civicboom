<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="title()">${_("Profile")}</%def>

<%def name="body()">
	<%
        self.attr.frags = [profile, help]
        self.attr.frag_col_sizes = [2,1]
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


