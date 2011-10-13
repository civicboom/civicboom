<%inherit file="/html/mobile/common/mobile_base.mako"/>

<%namespace name="member_includes" file="/html/mobile/common/member.mako" />


<%def name="title()">${d['message']['subject']}</%def>


<%def name="body()">
    <% message =  d['message'] %>

    <div data-role="page" data-theme="b" id="message_dialog">
        
        <div data-role="header" data-position="inline" data-id="page_header" data-theme="b">
            <h1>Message</h1>
        </div>
        
        <div data-role="content" data-theme="c">

            <h1>${message['subject']}</h1>
            
            % if message.get('target_id') != c.logged_in_persona.id):
                <p>To: ${member_includes.member_link(message.get('target')}</p>'
            % endif
            % if message.get('source'):
                <p>From: ${member_includes.member_link(message.get('source'))}</p>
            % endif
            
            <p>${h.literal(message.get('content'))}</p>
            
            ## If this is my message, allow deletes
            % if message.get('target_id') == c.logged_in_persona.id):
                ${h.secure_link(
                    h.args_to_tuple('message', id=self.message['id'], format='redirect') ,
                    method="DELETE",
                    value_formatted=h.literal("<button>%s</button>" % "Delete"),
                    title=_("Delete"),
                    json_form_complete_actions = "" ,
                )}
            % endif
            
            ## If this is from another member, show reply
            % if message.get('source_id'):
                <div data-role="collapsible" data-collapsed="true" class="search_form">
                    <h3>Reply</h3>
                    ${h.form(h.args_to_tuple('messages', format='redirect'), json_form_complete_actions="$('.ui-dialog').dialog('close');)")}
                        <div data-role="fieldcontain">
                            <input type="hidden" name="target" value="${self.message['source'] if isinstance(self.message['source'],basestring) else self.message['source']['username']}"/>
                            <label for="subject">${_("Subject")}</label>
                            <input type="text" name="subject" value="Re: ${self.message['subject']}">
                            <br />
                            <label for="content">Content</label>
                            <textarea name="content"></textarea>
                            <input type="submit" value="${_("Send")}">
                        </div>
                    ${h.end_form()}
                </div>
            % endif
        </div>
    
    </div>
</%def>

