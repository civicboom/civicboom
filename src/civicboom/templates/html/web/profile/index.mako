<%inherit file="/html/web/common/frag_container.mako"/>

<%!
    help_frag = 'profile'
%>

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
	<!--#include file="/help/profile"-->
</%def>


