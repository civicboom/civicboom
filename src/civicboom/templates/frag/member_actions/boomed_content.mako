<%inherit file="/frag/common/frag_lists.mako"/>

<%def name="body()"></%def>

<%def name="title()">
    ${_('Boomed Content')}
</%def>

<%def name="frag_list_call()">
    ${parent.content_list(d['list'], _('Boomed Content'), max=None, creator=True)}
</%def>