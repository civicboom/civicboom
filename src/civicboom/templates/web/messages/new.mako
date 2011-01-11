<%inherit file="/web/common/frag_container.mako"/>

<%!
    frag_container_css_class  = 'frag_bridge'
%>

<%def name="body()">
    <% self.attr.frags = new %>
</%def>

<%def name="new()">
    <%include file="/frag/messages/new.mako"/>
</%def>

