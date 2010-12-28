<%inherit file="/frag/common/frag_lists.mako"/>

<%def name="body()"></%def>

<%def name="title()">
    ${_('Members')}
</%def>

<%def name="frag_list_call()">
    ${parent.group_members_list(d['list'], _('Members'),  max=None)}
</%def>