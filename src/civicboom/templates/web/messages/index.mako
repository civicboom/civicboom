<%inherit file="/web/common/html_base.mako"/>
<%namespace name="private_profile" file="/web/profile/index.mako"/>

<%def name="col_left()">${private_profile.col_left()}</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">

    <% frag_url_messages = url('messages', format='frag') %>
    ${h.frag_div( "messages", frag_url_messages)}
    ${h.frag_link("messages", frag_url_messages, "refresh messages")}

</%def>
