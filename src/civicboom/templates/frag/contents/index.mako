<%inherit file="/frag/common/frag_lists.mako"/>

<%def name="body()"></%def>

<%def name="title()">
    <%
        args, kwargs = c.web_params_to_kwargs
        list_title = 'List'
        if 'list' in kwargs:
            list_title = kwargs['list'].capitalize()
    %>
    ${list_title}
</%def>

<%def name="frag_list_call()">
    <%
        args, kwargs = c.web_params_to_kwargs
        creator = True
        if 'creator' in kwargs:
            creator = False
    %>
    ${parent.content_list(d['list'], title(), max=None, creator=creator)}
</%def>