<%inherit file="/web/common/frag_container.mako"/>

<%!
    frag_container_css_class  = 'frag_bridge' # bit of a hack here to get the search box half width to start with
%>

<%def name="title()">${_('Messages')}</%def>

<%def name="body()">
    <% self.attr.frags = messages %>
</%def>

<%def name="messages()">
    <%include file="/frag/messages/index.mako"/>
</%def>

<%doc>
<% frag_url_messages = url('messages', format='frag') %>
${h.frag_div( "messages", frag_url_messages)}
${h.frag_link("messages", frag_url_messages, _("refresh messages"))}
</%doc>