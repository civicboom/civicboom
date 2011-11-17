<%inherit file="/email/base_email_content.mako"/>

<%namespace name="member_includes" file="/html/web/common/member.mako" />

<%def name="body()"></%def>

<%def name="content()">
    <% self.target = user.to_dict() %>
    <h1>${_('Summary')}</h1>
    
    <table>
        
        <tr><th colspan=3>${_('Notification Summary')}</th></tr>
        % for message in [m for m in messages if m.__type__(user)=='notification']:
            ${show_message(message)}
        % endfor
        
        <tr><th colspan=3>${_('Message Summary')}</th></tr>
        % for message in [m for m in messages if m.__type__(user) in ['to','sent']]:
            ${show_message(message)}
        % endfor
        
    </table>
</%def>

<%def name="show_message(message)">
<tr>
    ## From
    <td>
        % if message.source_id and message.source_id != self.target['id']:
            <% source = message.source.to_dict() %>
            ${member_includes.avatar     (source, js_link_to_frag=False, qualified=True)}
            ${member_includes.member_link(source, js_link_to_frag=False, qualified=True)}
        % endif
    </td>
    ## Message
    <td>
        <p><b>${message.subject}</b> <em>(${h.time_ago(message.timestamp)} ago)</em></p>
        <p>${h.literal(message.content)}</p>
    </td>
    ## To
    <td>
        <%
            target = None
            if message.source_id:
                #target = self.target # Dont display avatar of me
                if message.target_id != self.target['id']:
                    target = message.target.to_dict()
        %>
        % if target:
            ${member_includes.avatar     (target, js_link_to_frag=False, qualified=True)}
            ${member_includes.member_link(target, js_link_to_frag=False, qualified=True)}
        % endif
    </td>
</tr>
</%def>