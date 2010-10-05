<%inherit file="/web/common/layout_2cols.mako"/>
<%namespace name="loc" file="/web/design09/includes/location.mako"/>
<%namespace name="prof" file="/web/design09/includes/profile.mako"/>
<%def name="col_side()">${prof.sidebar()}</%def>

##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------
<%def name="body()">
<form action="${url.current(action='save_location', id=c.viewing_user.username)}" method="POST">
	<input type="hidden" name="_authentication_token" value="${h.authentication_token()}">
	${loc.location_picker(width='100%', height='300px', always_show_map=True)}
	<input type="submit" value="Save">
</form>
</%def>
