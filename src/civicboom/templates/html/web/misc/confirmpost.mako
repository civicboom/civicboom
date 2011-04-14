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
	<p>${_("You are about to <b>%s</b> on _site_name; is this what you want to do?") % action_description}</p>
    
	${h.form(c.target_url)}
% for k, v in c.post_values.items():
		<input type="hidden" name="${k}" value="${v}">
% endfor
		<input type="submit" value="${_("Yes")}" class="button">
        <a class="button" href="/profile">${_("No")}</a>
	${h.end_form()}
    <p style="font-style: italic;">${_("(We are double checking because you could have been tricked into performing an action that you did not want to do)")}</p>
</center>
