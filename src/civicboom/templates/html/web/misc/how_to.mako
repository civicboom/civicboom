<%inherit file="/html/web/common/html_base.mako"/>

<%namespace name="components" file="/html/web/common/components.mako" />

<%def name="html_class_additions()">blank_background</%def>
<%def name="title()">${_("How to use your profile!")}</%def>

<%def name="body()">
    <div style="padding: 1em;">
        <%include file="/frag/misc/how_to.mako"/>
    </div>
    ${components.misc_footer()}
</%def>