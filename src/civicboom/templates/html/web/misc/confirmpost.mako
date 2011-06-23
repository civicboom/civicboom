<%inherit file="/html/web/common/html_base.mako"/>

<%!
    from civicboom.lib.civicboom_lib import get_action_objects_for_url
%>

<%def name="html_class_additions()">blank_background</%def>
<%def name="title()">${_("Confirm action")}</%def>

<%
    action_objects     = get_action_objects_for_url()
    action_description = action_objects.get('description') or _('perform an action')
%>

<style>
    .accept_action {
        font-size: 175%;
    }
    .accept_action h1 {
        font-size: 200%;
    }
    .accept_action .button {
        font-size: 80%;
        vertical-align: top;
    }
</style>

<center class="accept_action">
    ${h.form(c.target_url)}
        <br /><h1>${_("Great! You're nearly there...")}</h1>
        <br /><p>${_("You are about to <b>%s</b>, to continue click ") % action_description |n} <input type="submit" value="${_("continue!")}" class="button"></p>
        % for k, v in c.post_values.items():
            <input type="hidden" name="${k}" value="${v}">
        % endfor
        <br /><p>Or to go to your profile click <a class="button" href="/profile">${_("profile")}</a>
    ${h.end_form()}
    ## <p style="font-style: italic;">${_("(We are double checking because you could have been tricked into performing an action that you did not want to do)")}</p>
</center>
