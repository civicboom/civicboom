<%inherit file="/frag/common/frag_lists.mako"/>

<%def name="body()">
    ${parent.group_members_list(d['list'], _('Members'),  max=None)}
</%def>