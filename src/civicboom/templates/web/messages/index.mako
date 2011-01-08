<%inherit file="/web/common/frag_container.mako"/>

<%!
    frag_container_css_class  = 'frag_bridge' # bit of a hack here to get the search box half width to start with
%>


##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------

<%def name="title()">${_('Messages')}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------


<%def name="body()">

    <%include file="/frag/messages/index.mako"/>

    <%doc>
    <% frag_url_messages = url('messages', format='frag') %>
    ${h.frag_div( "messages", frag_url_messages)}
    ${h.frag_link("messages", frag_url_messages, _("refresh messages"))}
    </%doc>

</%def>
