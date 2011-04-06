<%def name="location_picker(field_name='location', width='250px', height='250px', always_show_map=False, label_class=None, lon=None, lat=None)">
<!--<label${' class=%s' % label_class if label_class else ''} for="${field_name}_name">${_("Location name")}</label><br />-->
<input id="${field_name}_name" name="${field_name}_name" type="search" placeholder="Search for location" style="width: ${width}">
<div id="${field_name}_comp"></div>
<input id="${field_name}" name="${field_name}" type="hidden" value="${lon} ${lat}">
% if not always_show_map:
<script>
$(function() {
	$("#${field_name}_name").focus(function() {$("#${field_name}_div").slideDown();});
	$("#${field_name}_name").blur( function() {$("#${field_name}_div").slideUp();  });
});
</script>
% endif

<%
style = ""
if not always_show_map:
	style = style + " display: none; position: absolute; -webkit-box-shadow: 3px 3px 3px #666;"
%>
<div style="width: ${width}; height: ${height};${style}" id="${field_name}_div"></div>
<script type="text/javascript">
$(function() {
	map = map_picker('${field_name}', {
% if lon and lat:
		lonlat: {lon:${lon}, lat:${lat}},
% endif
	});
});
</script>
</%def>

<%def name="minimap(lon, lat, zoom=13, name='map', width='250px', height='250px', feeds=[], controls=False)">
<div style="width: ${width}; height: ${height};" id="${name}_div"></div>
<%
import json
%>
<script type="text/javascript">
$(function() {
	minimap(
		'${name}_div',
		{
			controls: ${str(controls).lower()},
			lonlat: {lon:${lon}, lat:${lat}},
			zoom: ${zoom},
		},
		${json.dumps(feeds)|n}
	);
});
</script>
</%def>
