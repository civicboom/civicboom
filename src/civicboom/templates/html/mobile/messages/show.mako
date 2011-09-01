<%inherit file="/html/mobile/common/mobile_base.mako"/>

## includes
<%namespace name="components"      file="/html/mobile/common/components.mako" />
<%namespace name="member_includes" file="/html/mobile/common/member.mako" />
<%namespace name="list_includes"   file="/html/mobile/common/lists.mako" />

<%def name="page_title()">
    ${d['message']['subject']}    
</%def>

## page structure defs
<%def name="body()">
    <%
        self.message =  d['message']
        self.read =     self.message['read']
        self.subject =  self.message['subject']
        self.content =  self.message['content']
        self.source =   self.message['source']
        self.target =   self.message['target']
    %>
    <div data-role="page" data-theme="b" id="message_dialog" class="">
        <div data-role="header">
            <h1>Message</h1>
        </div>
        
        <div data-role="content" data-theme="c">
            <h1>${self.subject}</h1>
            ${involved()}
            <p>
                ${h.literal(self.content)}
            </p>
            
            % if config['development_mode']:
                % if self.message.get('source_id') and not (self.message['source_id']==c.logged_in_persona.id or self.message['source_id']==c.logged_in_persona.username):
                    <hr>
                    <h3>Reply</h3>
                    ${h.form(h.args_to_tuple('messages', format='redirect'), json_form_complete_actions="$('.ui-dialog').dialog('close');)")}
                        <div data-role="fieldcontain">
                            <input type="hidden" name="target" value="${self.message['source'] if isinstance(self.message['source'],basestring) else self.message['source']['username']}"/>
                            <label for="subject">${_("Subject")}</label>
                            <input type="text" name="subject" value="Re: ${self.message['subject']}">
                            <textarea name="content"></textarea>
                            <input type="submit" value="${_("Send")}">
                        </div>
                    ${h.end_form()}
                % endif
            % endif
        </div>
    </div>
</%def>

<%def name="involved()">
    <%doc>
    % if self.target:
        <p>To: ${member_includes.member_link(self.target)}</p>
    % endif
    </%doc>
    
    % if self.source:
        <p>From: ${member_includes.member_link(self.source)}</p>
    % endif
</%def>
