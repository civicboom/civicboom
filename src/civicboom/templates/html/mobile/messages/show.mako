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
            ${involved()}
            <h1>${self.subject}</h1>
            <p>
                ${h.literal(self.content)}
            </p>
            
            % if config['development_mode']:
                <hr>
                <h3>Reply</h3>
                ${h.form(h.args_to_tuple('messages', format='redirect'), json_form_complete_actions="cb_frag_remove(current_element);")}
                    <table class="message_composer" style="width:100%">
                        <input type="hidden" name="target" value="${self.message['source'] if isinstance(self.message['source'],basestring) else self.message['source']['username']}"/>
                        
                        <tr>
                            <td>${_("Subject")}&nbsp;</td>
                            <td><input type="text" name="subject" value="Re: ${self.message['subject']}"></td>
                        </tr>
                        <tr>
                            <td colspan="2"><textarea name="content"></textarea></td>
                        </tr>
                        <tr>
                            <td colspan="2"><input type="submit" value="${_("Send")}"></td>
                        </tr>
                    </table>
                ${h.end_form()}
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
