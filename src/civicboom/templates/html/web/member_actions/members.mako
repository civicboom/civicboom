<%inherit file="/html/web/common/frag_container.mako"/>

<%!
    ##frag_container_css_class  = 'frag_bridge' # bit of a hack here to get the search box half width to start with
    frag_col_sizes = [1]
%>

<%def name="body()">
    <% self.attr.frags = list %>
</%def>

<%def name="list()">
    <%include file="/frag/member_actions/members.mako"/>
</%def>