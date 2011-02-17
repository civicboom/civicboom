<%def name="location_picker(field_name='location', width='250px', height='250px', always_show_map=False, label_class=None, lon=None, lat=None)">
<label${' class=%s' % label_class if label_class else ''} for="${field_name}_name">${_("Location name")}</label><br />
<input id="${field_name}_name" name="${field_name}_name" type="text" style="width: ${width}">
<div style="padding-top: 6px" id="${field_name}_comp"></div>
<input id="${field_name}" name="${field_name}" type="hidden">
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
<div style="width: ${width}; height: ${height}; border: 1px solid black; ${style}" id="${field_name}_div"></div>
<script type="text/javascript">
$(function() {
	map = map_picker('${field_name}', {
		lonlat: {lon:${lon}, lat:${lat}},
	});
});
</script>
</%def>

<%def name="minimap(name='map', width='250px', height='250px', lon=None, lat=None, zoom=13, feeds=[], controls=False)">
<div style="width: ${width}; height: ${height}; border: 1px solid black;" id="${name}_div"></div>
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
