<%inherit file="/web/layout_2cols.mako"/>
<%namespace name="loc" file="/web/design09/includes/location.mako"/>
<%namespace name="prof" file="/web/design09/includes/profile.mako"/>
<%def name="col_side()">${prof.sidebar()}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
<form action="${url.current(action='save_location', id=c.viewing_user.username)}" method="POST">
	<input type="hidden" name="_authentication_token" value="${h.authentication_token()}">
	${loc.autocomplete_location()}
	<input type="submit" value="Save">
</form>
</%def>
