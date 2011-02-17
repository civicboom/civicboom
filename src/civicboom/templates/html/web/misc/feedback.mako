<%inherit file="/html/web/common/frag_container.mako"/>

<%def name="title()">${_("Feedback")}</%def>

<%def name="body()">
    <% self.attr.frags = feedback %>
</%def>

<%def name="feedback()">
    <!--#include file="/misc/feedback.frag"-->
</%def>
