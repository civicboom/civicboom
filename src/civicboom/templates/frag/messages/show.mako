<%inherit file="/frag/common/frag.mako"/>

<%namespace name="member_includes" file="/web/common/member.mako" />

<%!
    title               = 'Message'
    icon_type           = 'message'

    rss_url             = False
%>

<%def name="body()">
    ${show_message(c.result['data']['message'])}    
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
