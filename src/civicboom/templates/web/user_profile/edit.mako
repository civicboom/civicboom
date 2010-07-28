<%inherit file="/web/html_base.mako"/>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
	<img src="${c.viewing_user.avatar_url}">
	${c.viewing_user.name}
	(${c.viewing_user.username})

	<form action="${url.current(action='save', id=c.viewing_user.username)}" method="POST">
		<input type="hidden" name="_authentication_token" value="${h.authentication_token()}">
		<fieldset>
			<legend>${_("General Info")}:</legend>
			Height: <input name="height" value="${c.viewing_user.config["height"]}">
			<br>Width: <input name="width" value="${c.viewing_user.config["width"]}">
			<input type="submit" value="Save">
		</fieldset>
	</form>
</%def>
