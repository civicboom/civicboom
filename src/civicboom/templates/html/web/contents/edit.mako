<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="title()">${_('Edit')}</%def>


<%def name="body()">
    <%
        if d['content'].get('parent'):
            self.attr.frags          = [parent, content_edit]  # If the content being edited has a parent, place the parent beside it for reference
            self.attr.frag_col_sizes = [2,2]
            self.attr.frag_classes   = [None, None]
        else:
            self.attr.frags          = [content_edit]
            self.attr.frag_col_sizes = [2]
            self.attr.frag_classes   = [None]
    %>
</%def>


<%def name="content_edit()">
    <%include file="/frag/contents/edit.mako"/>
</%def>

<%def name="parent()">
    <!--#include virtual="${url('content', id=d['content']['parent']['id'], format='frag', exclude_actions='all' )}"-->
</%def>

<%doc>
<%def name="help()">
    % if   d['content']['type'] == 'assignment' or d['content'].get('target_type') == 'assignment':
	<!--#include virtual="/help/create_assignment"-->
    % elif d['content']['parent']:
    <!--#include virtual="/help/create_response"-->
    % elif d['content']['type'] == 'article'    or d['content'].get('target_type') == 'article'   :
    <!--#include virtual="/help/create_article"-->
    % endif
</%def>
</%doc>