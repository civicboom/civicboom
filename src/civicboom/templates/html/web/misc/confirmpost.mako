<%inherit file="/html/web/common/html_base.mako"/>

<%!
    from civicboom.lib.civicboom_lib import get_action_objects_for_url
%>


<%def name="title()">${_("Confirm action")}</%def>

<%
    action_objects     = get_action_objects_for_url()
    action_description = action_objects.get('description') or _('perform an action')
%>

<center>
	<h1>${_("Just checking ...")}</h1>
	${_("You are about to %s on _site_name, but it looks like you've come from another web site; do you want to continue?") % action_description}
	${h.form(c.target_url)}
% for k, v in c.post_values.items():
		<input type="hidden" name="${k}" value="${v}">
% endfor
		<input type="submit" value="${_("Yes")}">
		<input type="button" value="${_("No")}" onclick="go_to_front_page()"> <!-- FIXME -->
	${h.end_form()}
</center>
