<%inherit file="/web/common/html_base.mako"/>
<%namespace name="loc" file="/web/common/location.mako" />
<%def name="title()">${_("GeoRSS Viewer")}</%def>

% try:
	<% location = request.params.get("location", "0,53,4").split(",") %>
	<p>${loc.minimap(
		width="100%", height="600px",
		lat = location[0],
		lon = location[1],
		feeds = [
			dict(pin='red', url='/search/content.rss')
		]
	)}</p>
% except:
	<span class="error">${_("Error decoding location")} "${request.params.get("location", "")}"</span>
% endtry
