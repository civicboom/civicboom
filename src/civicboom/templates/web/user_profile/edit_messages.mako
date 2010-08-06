<%inherit file="/web/html_base.mako"/>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
<form action="${url.current(action='edit_settings', id=c.viewing_user.username)}" method="POST">
	<input type="hidden" name="_authentication_token" value="${h.authentication_token()}">
	<input type="submit" value="Save" style="width: 100%">
</form>
</%def>
