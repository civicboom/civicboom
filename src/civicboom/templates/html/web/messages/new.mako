<%inherit file="/html/web/common/frag_container.mako"/>

<%!
    ##frag_container_css_class  = 'frag_bridge'
    frag_col_sizes = [2]
%>

<%def name="body()">
    <% self.attr.frags = new %>
</%def>

<%def name="new()">
    <%include file="/frag/messages/new.mako"/>
</%def>

