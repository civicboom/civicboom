<%inherit file="/html/web/common/html_base.mako"/>
<%namespace name="loc" file="/html/web/common/location.mako" />
<%def name="title()">${_("GeoRSS Viewer")}</%def>

<%
try:
	location = [float(n) for n in request.params.get("location").split(",")]
	if len(location) != 3:
		raise ValueError("location needs 3 parts")
except:
	location = [-1.0, 53.0, 5.0]
%>

<div style="position: fixed; top: 52px; left: 10px; right: 10px; bottom: 26px;">
${loc.minimap(
	width="100%", height="100%",
	lon = location[0],
	lat = location[1],
	zoom = location[2],
	feeds = [
		dict(pin='red', url=request.params.get('feed', '/contents.rss?location=%f,%f' % (location[0], location[1])), focus=True)
	],
	controls = True
)}
</div>
