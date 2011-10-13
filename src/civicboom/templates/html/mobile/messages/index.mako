<%inherit file="/html/mobile/common/lists.mako"/>

<%def name="title()">${_("Messages")}</%def>

<%def name="list_id()"     >messages</%def>
<%def name="list_class()"  >messages</%def>
<%def name="list_content()">
    <%
        title_dict = {
            'to'          : _("messages"),
            'sent'        : _("sent messages"),
            'notification': _("notifications"),
        }
        
        list  = d['list']
        title = title_dict.get(list['kwargs']['list'], 'messages')
    %>
    % if list.get('count'):
        ${parent.generate_list(list, message_li, title=title, more=None)}
    % else:
        <p>${_("You have no %s") % title}</p>
        <p><a href="${h.url(controller='profile', action='index')}" rel="external">${_('Return to profile')}</a></p>
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
                <p><b>${_("From %s") % item['source']['username']}</b></p>
            % endif
            <p>${item['content']}</p>
            <p>${item['timestamp']}</p>
        </a>
    </li>
</%def>

