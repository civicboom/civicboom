<%def name="location_picker(field_name='location', width='250px', height='250px', always_show_map=False, label_class=None, lon=None, lat=None)">
<%
field_id = h.uniqueish_id(field_name)
%>
% if height == "fill":
<div class="fill">
% else:
<div style="position: relative;">
% endif
<!--<label${' class=%s' % label_class if label_class else ''} for="${field_name}_name">${_("Location name")}</label><br />-->
<input id="${field_id}_name" name="${field_name}_name" type="search" placeholder="${_("Search for location")}" style="width: ${width}">
<div id="${field_id}_comp"></div>
<input id="${field_id}" name="${field_name}" type="hidden" value="${lon} ${lat}">
% if not always_show_map:
<script>
$(function() {
	$("#${field_id}_name").focus(function() {$("#${field_id}_div").slideDown();});
	$("#${field_id}_name").blur( function() {$("#${field_id}_div").slideUp();  });
});
</script>
% endif

<%
style = ""
if not always_show_map:
	style = style + " display: none; position: absolute; -webkit-box-shadow: 3px 3px 3px #666;"
%>

% if height == "fill":
<div style="width: ${width}; height: 90%;${style}" id="${field_id}_div"></div>
% else:
<div style="width: ${width}; height: ${height};${style}" id="${field_id}_div"></div>
% endif
<script type="text/javascript">
$(function() {
	map = map_picker('${field_id}', {
% if lon and lat:
		lonlat: {lon:${lon}, lat:${lat}},
% endif
	});
});
</script>
</div>
</%def>

<%def name="minimap(lon, lat, zoom=11, name='map', width='250px', height='250px', feeds=[], controls=False)">
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
