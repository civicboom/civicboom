<%inherit file="/html/web/common/html_base.mako"/>

<%def name="title()">${_("_Widget Preview")}</%def>

<%def name="body()">
    <div style="padding: 1em;">
    <%include file="/frag/misc/get_widget.mako"/>
    </div>
</%def>