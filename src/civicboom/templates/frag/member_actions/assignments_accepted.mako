<%inherit file="/frag/common/frag_lists.mako"/>

<%def name="body()">
    ${parent.content_list(d['list'], _('Accepted Assignments'), max=None, creator=True)}
</%def>