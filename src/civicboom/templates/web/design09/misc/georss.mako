<%inherit file="/web/html_base.mako"/>
<%namespace name="loc" file="../includes/location.mako"/>

<%def name="body()">
% try:
	<% location = request.params.get("location", "1.08,51.28,13").split(",") %>
	${loc.minimap(
		width="100%", height="600px",
		lon=float(location[0]),
		lat=float(location[1]),
		zoom=int(location[2]),
		overlay=request.params.get('feed', '/search/content')
	)}
% except:
	<span class="error">Error decoding location "${request.params.get("location", "")}"</span>
% endtry
</%def>
