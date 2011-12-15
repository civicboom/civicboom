<%inherit file="/html/web/common/html_base.mako"/>
<%def name="title()">${_("New Feed")}</%def>

${h.form(url('feeds'), method="post")}
	Name: <input type="text" name="name" placeholder="e.g. Sport in Whitstable">
	<p><input type="submit">
${h.end_form()}
