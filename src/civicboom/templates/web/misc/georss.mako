<%inherit file="/web/common/html_base.mako"/>
<%namespace name="loc" file="/web/common/location.mako" />
<%def name="title()">${_("GeoRSS Viewer")}</%def>

<%
try:
	location = [float(n) for n in request.params.get("location").split(",")]
	if len(location) != 3:
		raise ValueError("location needs 3 parts")
except:
	location = [-1.0, 53.0, 5.0]
%>

${loc.minimap(
	width="100%", height="600px",
	lon = location[0],
	lat = location[1],
	zoom = location[2],
	feeds = [
		dict(pin='red', url=request.params.get('feed', '/search/content.rss'), focus=True)
	],
	controls = True
)}
