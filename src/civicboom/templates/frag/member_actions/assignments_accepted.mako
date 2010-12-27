<%inherit file="/frag/common/frag_lists.mako"/>

<%def name="body()"></%def>

<%def name="title()">
    ${_('Accepted Assignments')}
</%def>

<%def name="frag_list_call()">
    ${parent.content_list(d['list'], _('Accepted Assignments'), max=None, creator=creator)}
</%def>