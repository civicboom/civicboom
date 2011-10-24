<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%namespace name="message_includes" file="/html/mobile/messages/show.mako" />

<%def name="body()">
    <%
        conversation_with = d['list']['kwargs']['conversation_with']
        messages = d['list']['items']
        messages.reverse()
    %>

    <%doc>
    <div data-role="page" data-theme="b" id="member-details-${id}" class="member_details_page">
        
        <div data-role="content">
            hi
        </div>
        
        ${self.footer()}
    </div>
    </%doc>


    <div data-role="page" id="conversation-with-${conversation_with}" >
        
        ${self.header(title = _('Conversation with %s') % conversation_with)}
        
        <div data-role="content" class="conversation">
            <ul>
                ##data-role="listview"
            % for message in messages:
                <li class="${message['type']}">
                    <%doc>
                        % if message['type'] == 'sent':
                            data-theme="b"
                        % else:
                            data-theme="d"
                        % endif
                    >
                    </%doc>
                    <img src="${message['source']['avatar_url']}"/>
                    <p>${message['content']}</p>
                    <p class="timestamp">${_('%s ago') % h.time_ago(message['timestamp'])}</p>
                </li>
            % endfor
            </ul>
            
            ${message_includes.reply(conversation_with)}
        </div>
        
        ${self.footer()}
        
    </div>
    

</%def>