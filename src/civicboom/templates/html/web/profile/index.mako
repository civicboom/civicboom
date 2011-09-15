<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="title()">${_("Profile")}</%def>

<%def name="body()">
	<%
        self.attr.frags = [profile, featured]
        self.attr.frag_col_sizes = [2,2]
        self.attr.frag_classes   = [None, None]
        
        # old profile page
        #self.attr.frags = [profile, assignments, help]
        #self.attr.frag_col_sizes = [2,1,1]
        #self.attr.frag_classes   = [None, None, 'flag_help']
        %>
</%def>

<%def name="profile()">
    <!--#include virtual="/profile.frag"-->
</%def>

<%def name="help()">
    % if   d['member']['type'] == 'user':
	<!--#include virtual="/help/profile"-->
    % elif d['member']['type'] == 'group':
    <!--#include virtual="/help/group_persona"-->
    % endif
</%def>

<%def name="assignments()">
<!--#include virtual="${h.url('contents', format='frag', list='assignments_active')}"-->
</%def>

<%def name="featured()">
<%
from civicboom.model.meta import location_to_string
%>
% if c.logged_in_user and c.logged_in_user.location_current:
    <!--#include virtual="${h.url(controller='misc', action='featured', format='frag', location=location_to_string(c.logged_in_user.location_current))}"-->
% else:
    <!--#include virtual="${h.url(controller='misc', action='featured', format='frag')}"-->
% endif
</%def>
