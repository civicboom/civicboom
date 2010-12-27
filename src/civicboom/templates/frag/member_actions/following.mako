<%inherit file="/frag/common/frag_lists.mako"/>

<%def name="body()"></%def>

<%def name="title()">
    ${_('Following')}
</%def>

<%def name="frag_list_call()">
    ${parent.member_list(d['list'], '', max=None)}
</%def>