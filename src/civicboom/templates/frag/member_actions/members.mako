<%inherit file="/frag/common/frag_lists.mako"/>

<%def name="body()">
    <%
        # OH JESUS!!! WHAT A HACK!!!!
        # Processing in a template = BAD!!!!!
        d['actions'] = c.group.action_list_for(member=c.logged_in_persona, role=c.logged_in_persona_role)
        d['group']   = {'id':c.group.id}
    %>
    ${parent.group_members_list(d['list']['items'], _('Members'))}
</%def>