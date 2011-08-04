<%inherit file="/frag/common/frag.mako"/>

<%namespace name="member_includes" file="/html/web/common/member.mako" />

<%!
    title               = 'Message'
    icon_type           = 'message'

    rss_url             = False
%>

<%def name="body()">
    <%
        message = c.result['data']['message']
    %>
    <div class="frag_list_contents">
        <div class="messages" style="padding: 3px;">
            ${show_message(message)}
            <div style="clear:both"></div>
            % if message.get('source_id') and not (message['source_id']==c.logged_in_persona.id or message['source_id']==c.logged_in_persona.username):
            <h3 class="subject">${_('Reply')}</h3>
            ${reply_message(message)}
            % endif
        </div>
    </div>
</%def>


<%def name="show_message(message)">

% if message.get('source'):
    <div style="float:left;margin: 3px;">${member_includes.avatar(message['source'], class_="thumbnail source")}</div>
% else:
    <div class="icon32 i_notification" style="float: left; margin: 3px;"><span>Notification</span></div>
% endif
<div style="padding-left:50px;">
	<div class="subject">${message["subject"]}</div>
	<div class="content">${message["content"] | n}</div>
</div>
<p class="timestamp">${_('%s ago') % h.time_ago(message['timestamp'])}</p>
</%def>

<%def name="reply_message(message)">
	${h.form(h.args_to_tuple('messages', format='redirect'), json_form_complete_actions="cb_frag_remove(current_element);")}
		<table class="message_composer" style="width:100%">
	        
	        <input type="hidden" name="target" value="${message['source'] if isinstance(message['source'],basestring) else message['source']['username']}"/>]
            
			<tr>
				<td>${_("Subject")}&nbsp;</td>
				<td><input type="text" name="subject" value="Re: ${message['subject']}"></td>
			</tr>
			<tr>
				<td colspan="2"><textarea name="content"></textarea></td>
			</tr>
			<tr>
				<td colspan="2"><input type="submit" value="${_("Send")}"></td>
			</tr>
		</table>
	${h.end_form()}
</%def>