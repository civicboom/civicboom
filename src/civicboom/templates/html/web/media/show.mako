<%inherit file="/html/web/common/html_base.mako"/>
<%def name="title()">${_("Media Viewer")}</%def>

<div style="position: fixed; top: 52px; left: 10px;">
	<img src="${d['media']['media_url']}">
</div>
