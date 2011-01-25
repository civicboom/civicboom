<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="title()">${_('Edit')}</%def>


<%def name="body()">
	<%
		if d['content']['parent']:
			self.attr.frags = [content_edit, parent, help]  # If the content being edited has a parent, place the parent beside it for reference
		else:
			self.attr.frags = [content_edit, help]
	%>
</%def>


<%def name="content_edit()">
	<%include file="/frag/contents/edit.mako"/>
</%def>

<%def name="parent()">
	<!--#include file="${url('content', id=d['content']['parent']['id'], format='frag')}"-->
</%def>

<%def name="help()">
	<!--#include file="/help/create_assignment"-->
</%def>