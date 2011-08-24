<%inherit file="/frag/common/frag_lists.mako"/>

<%def name="init_vars()">
    ${parent.init_vars()}
    <%
        args, kwargs = c.web_params_to_kwargs
        
        title = 'Messages'
        icon = 'message'
        
        if kwargs.get('list') == 'sent':
            title = 'Sent Messages'
            icon = 'message_sent'
        if kwargs.get('list') == 'notification':
            title = 'Notifications'
            icon = 'notification'
            
        self.attr.title     = "%s (%s)" % (title, d['list']['count'])
        self.attr.icon_type = icon
    %>
</%def>

<%def name="body()">
    <%
        args, kwargs = c.web_params_to_kwargs
        list = _('Message ')
        if 'list' in kwargs:
            list += kwargs.get('list')
    %>
    ${parent.message_list(d['list'], list, list=kwargs.get('list'), show_heading=False)}
</%def>