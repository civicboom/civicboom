<%inherit file="/web/html_base.mako"/>

<%def name="body()">
<center>
	<h1>${_("Hold it!")}</h1>
	${_("You are about perform an action on _site_name, but it looks like you've come from another web site; can you confirm that you want to interact now? Click 'no' if you're just browsing.")}
	${h.form(c.target_url)}
% for k, v in c.post_values.items():
		<input type="hidden" name="${k}" value="${v}">
% endfor
		<input type="submit" value="${_("Yes")}">
		<input type="button" value="${_("No")}" onclick="go_to_front_page()"> <!-- FIXME -->
	${h.end_form()}
</center>
</%def>
