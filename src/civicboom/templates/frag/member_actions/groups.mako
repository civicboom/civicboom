<%inherit file="/frag/common/frag_lists.mako"/>

<%def name="body()"></%def>

<%def name="title()">
    ${_('Groups')}
</%def>

<%def name="frag_list_call()">
    ${parent.member_list(d['list'], _('Groups'), max=None)}
</%def>