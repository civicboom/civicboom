<%inherit file="../common/widget_border.mako"/>

<%namespace name="content_list" file="../contents/index.mako"/>

<%
    contents = []
    for list in d.values():
        if isinstance(list, dict) and 'type' in list and list['type'] == 'contents':
            contents = contents + list['items']
            
    # TODO
    # sort list by date?
%>

${content_list.content_list(contents)}