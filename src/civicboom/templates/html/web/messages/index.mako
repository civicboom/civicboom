<%inherit file="/html/web/common/frag_container.mako"/>

<%doc>
<%!
    ##frag_container_css_class  = 'frag_bridge' # bit of a hack here to get the search box half width to start with
    frag_col_sizes = [1]
%>
</%doc>

<%def name="title()">${_('Messages')}</%def>

<%def name="body()">
    <%  
        self.attr.frags          = [profile , messages]
        self.attr.frag_col_sizes = [      2 ,        2]
        self.attr.frag_classes   = [   None ,     None]
    %>
</%def>

<%def name="profile()">
    <!--#include virtual="${h.url(controller='profile', action='index', format='frag')}"-->
	##<%include file="/frag/members/show.mako"/>
</%def>


<%def name="messages()">
    <%include file="/frag/messages/index.mako"/>
</%def>

<%doc>
<% frag_url_messages = url('messages', format='frag') %>
${h.frag_div( "messages", frag_url_messages)}
${h.frag_link("messages", frag_url_messages, _("refresh messages"))}
</%doc>
