<%inherit file="/frag/common/frag_lists.mako"/>

<%!
    rss_url = True
%>


<%def name="body()">
    <%
        args, kwargs = c.web_params_to_kwargs
        creator = True
        if 'creator' in kwargs:
            creator = False
        list_title = 'List'
        if 'list' in kwargs:
            list_title = kwargs['list'].capitalize()
    %>
            
    ${parent.content_list(d['list'], list_title, show_heading=False, creator=creator)}
</%def>
