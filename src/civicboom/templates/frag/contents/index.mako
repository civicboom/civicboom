<%inherit file="/frag/common/frag_lists.mako"/>

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
    ${parent.content_list(d['list'], list_title, max=None, creator=creator)}
</%def>
