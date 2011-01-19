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
    
    ${show_message(message)}
    
    % if message.get('source_id') and not (message['source_id']==str(c.logged_in_persona.id) or message['source_id']==c.logged_in_persona.username):
    <p>${_('Reply')}</p>
    <!--#include file="${url('new_message', format='frag', target=message.get('source_id'), subject='Re: '+message.get('subject'))}"-->
    % endif
</%def>


<%def name="show_message(message)">
<table>
	<tr>
		<th>${_("From")}</th>
		<th>${_("Subject")}</th>
		<th>${_("Date")}</th>
	</tr>
	<tr>
		<td>${member_includes.avatar(message["source"])}</td>
		<td>${message["subject"]}</td>
		<td>${message["timestamp"][0:16]}</td>
	</tr>
	<tr>
		<td colspan="3">${message["content"]}</td>
	</tr>
</table>
</%def>
