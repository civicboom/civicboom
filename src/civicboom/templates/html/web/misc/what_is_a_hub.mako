<%inherit file="/html/web/common/html_base.mako"/>

<%namespace name="components" file="/html/web/common/components.mako" />

<%def name="html_class_additions()">blank_background</%def>
<%def name="title()">${_("What is a _Group")}</%def>

<%def name="body()">
    <div style="padding: 1em;">
        <%include file="/frag/misc/what_is_a_hub.mako"/>
    </div>
    ${components.misc_footer()}
</%def>