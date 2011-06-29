##<%namespace name="member_includes"  file="/html/web/common/member.mako"/>
##${member_includes.member_list(d['list'])}
<%inherit file="/frag/common/frag_lists.mako"/>

<%!
    rss_url = True
%>


<%def name="init_vars()">
    ${parent.init_vars()}
    <%
        args, kwargs = c.web_params_to_kwargs
        
        title = ''
        if kwargs.get('type'):
            title = _('_' + kwargs.get('type') + 's').capitalize()
        icon  = 'user'
        
        if 'followed_by' in kwargs:
            title = _('Following')
            icon  = 'follow'
        if 'follower_of' in kwargs:
            title = _('Followers')
            icon  = 'follow'
        
        self.attr.title     = "%s (%s)" % (title, d['list']['count'] )
        self.attr.icon_type = icon
    %>
</%def>


<%def name="body()">
    <%
        args, kwargs = c.web_params_to_kwargs
        
        list_title = 'List'
        if 'list' in kwargs:
            list_title = kwargs['list'].capitalize()
    %>
    ## <div class="frag_list">
        ${parent.member_list(d['list'], list_title, show_heading=False, paginate=True, icon=kwargs.get('list'))}
    ## </div>
</%def>
