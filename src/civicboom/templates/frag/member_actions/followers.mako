<%inherit file="/frag/common/frag_lists.mako"/>

<%def name="body()"></%def>

<%def name="title()">
    ${_('Followers')}
</%def>

<%def name="frag_list_call()">
    ${parent.member_list(d['list'], '',  max=None)}
</%def>