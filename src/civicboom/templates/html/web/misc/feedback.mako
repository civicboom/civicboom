<%inherit file="/html/web/common/frag_container.mako"/>

<%namespace name="frag"          file="/frag/common/frag.mako" />
<%namespace name="feedback_frag" file="/frag/misc/feedback.mako" />

<%def name="title()">${_("Feedback")}</%def>

<%def name="body()">
    <% self.attr.frags = feedback %>
</%def>

<%def name="feedback()">
    ${frag.frag_basic('Feedback', 'dialog', feedback_frag.feedback_form)}
    ##<!--#include virtual="/misc/feedback.frag"-->
</%def>
