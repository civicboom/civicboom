<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="title()">${_('Edit')}</%def>


<%def name="body()">
	<%
		if d['content']['parent']:
			self.attr.frags          = [content_edit, parent]  # If the content being edited has a parent, place the parent beside it for reference
			self.attr.frag_col_sizes = [2,2,1]
			self.attr.frag_classes   = [None, None]
		else:
			self.attr.frags          = [content_edit]
			self.attr.frag_col_sizes = [2,1]
			self.attr.frag_classes   = [None]
	%>
</%def>


<%def name="content_edit()">
	<%include file="/frag/contents/edit.mako"/>
</%def>

<%def name="parent()">
	<!--#include file="${url('content', id=d['content']['parent']['id'], format='frag')}"-->
</%def>

<%def name="help()">
    % if   d['content']['type'] == 'assignment' or d['content'].get('target_type') == 'assignment':
	<!--#include file="/help/create_assignment"-->
    % elif d['content']['parent']:
    <!--#include file="/help/create_response"-->
    % elif d['content']['type'] == 'article'    or d['content'].get('target_type') == 'article'   :
    <!--#include file="/help/create_article"-->
    % endif
</%def>