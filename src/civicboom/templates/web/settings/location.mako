<%inherit file="/web/common/html_base.mako"/>
<%namespace name="loc" file="/web/common/location.mako"/>
<%namespace name="prof" file="/web/common/profile.mako"/>
<%def name="col_left()">${prof.sidebar()}</%def>

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
