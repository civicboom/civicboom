<%inherit file="/frag/common/frag_lists.mako"/>

<%def name="body()">
    ${parent.content_list(d['list']['items'], _('Accepted _Assignments'), creator=True)}
</%def>
