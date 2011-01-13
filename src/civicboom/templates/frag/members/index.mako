##<%namespace name="member_includes"  file="/web/common/member.mako"/>
##${member_includes.member_list(d['list'])}
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
    ${parent.member_list(d['list'], list_title, icon=kwargs.get('list'), max=None)}
</%def>
