<%inherit file="/html/mobile/common/lists.mako"/>

<%!
    title_dict = {
        'to'          : _("messages"),
        'sent'        : _("sent messages"),
        'notification': _("notifications"),
    }
%>

<%def name="init_vars()">
<%
    self.title      = _("Messages")
    self.page_id    = "messages"
    self.page_class = "messages"
%>
</%def>


<%def name="body()">
    <%
        list  = d['list']
        title = title_dict.get(list['kwargs']['list'], 'messages')
    %>
    % if list.get('count'):
        ${parent.generate_list(list, message_li, title=title, more=None)}
    % else:
        <p>You have no ${title}</p>
        <p><a href="${h.url(controller='profile', action='index')}" rel="external">Return to profile</a></p>
    % endif
</%def>




##------------------------------------------------------------------------------
## Generate a single li element for the given message
##------------------------------------------------------------------------------
<%def name="message_li(item)">
    <%
        item_read = 1 if item['read'] else 0
    %>
    <li onclick="$(this).attr('data-theme', 'c');"
    % if not item_read:
        data-theme="b"
    % endif    
    >
        <a href="${url('message', id=item['id'])}" data-ajax="true" data-rel="dialog" data-transition="fade">
            <h3>${item['subject']}</h3>
            % if item.get('source'):
                <p><b>From ${item['source']['username']}</b></p>
            % endif
            <p>${item['content']}</p>
            <p>${item['timestamp']}</p>
        </a>
    </li>
</%def>

