<%inherit file="/frag/common/frag_lists.mako"/>

<%def name="body()">
    ${parent.member_list(d['list']['items'], _('Groups'), max=None)}
</%def>