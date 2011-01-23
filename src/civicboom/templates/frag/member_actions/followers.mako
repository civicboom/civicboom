<%inherit file="/frag/common/frag_lists.mako"/>

## TO BE DEPRICATED!!

<%def name="body()">
    ${parent.member_list(d['list']['items'], 'followers', show_heading=False)}
</%def>