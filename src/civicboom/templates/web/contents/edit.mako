<%inherit file="/web/common/frag_container.mako"/>

<%def name="title()">${_('Edit')}</%def>

## If the content being edited has a parent, place the parent beside it for reference

<%def name="body()">
    % if d['content']['parent']:
        <!--#include file="${url('content', id=d['content']['parent']['id'], format='frag')}"-->
	% else:
		<%include file="/frag/contents/edit.mako"/>
    % endif
	
</%def>

<%def name="body2()">
	% if d['content']['parent']:
		<div id="frag__" class="frag_container">
			<%include file="/frag/contents/edit.mako"/>
		</div>
	% endif
</%def>