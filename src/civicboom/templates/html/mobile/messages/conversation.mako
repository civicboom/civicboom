<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%namespace name="message_includes" file="/html/mobile/messages/show.mako" />

<%def name="body()">
    <%
        conversation_with = d['list']['kwargs']['conversation_with']
        messages = d['list']['items']
        messages.reverse()
    %>
    
    <div data-role="page" id="conversation-with-${conversation_with}">
        
        ${self.header(title = _('Conversation with %s') % conversation_with, link_back=h.url('messages', list='to'))}
        
        <div data-role="content" class="conversation">
            <ul>
                ##data-role="listview"
            % for message in messages:
                <% bar_theme = "c" if message['type']=='sent' else "b" %>
                <li class="${message['type']} ui-bar ui-bar-${bar_theme} ui-corner-all">
                    <img src="${message['source']['avatar_url']}" class="ui-corner-all"/>
                    <p>${message['content']}</p>
                    <p class="timestamp">${_('%s ago') % h.time_ago(message['timestamp'])}</p>
                </li>
            % endfor
            </ul>
            
            ${message_includes.reply(conversation_with)}
            <a name="conversation_end"></a> 
        </div>
        
        ${self.footer()}
        
    </div>
    
    <%doc>
    ## AllanC - Attempt at auto scroll to bottom ... failed
    <script type="text/javascript">
    $("#conversation-with-${conversation_with}").live('pageinit', function() {
        ##$.mobile.changePage("#conversation_end");
        $.mobile.silentScroll(1000);
    });
    </script>
    </%doc>
    
</%def>