<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="body()">
    <% self.attr.frags = flag %>
</%def>

<%def name="flag()">
    <%include file="/frag/content_actions/flag.mako"/>
</%def>