<%def name="location_picker(field_name='location', width='250px', height='250px', lon=1.08, lat=51.28, zoom=13, always_show_map=False)">
<div style="width: ${width}; padding-bottom: 2em;">
	<input id="${field_name}_name" name="${field_name}_name" type="text">
	<div id="${field_name}_comp"></div>
	<input id="${field_name}" name="${field_name}" type="hidden">
	% if not always_show_map:
	<script>
	$(function() {
		$("#${field_name}_name").focus(function() {$("#${field_name}_div").slideDown();});
		$("#${field_name}_name").blur( function() {$("#${field_name}_div").slideUp();  });
	});
	</script>
	% endif
</div>

<%
style = ""
if not always_show_map:
	style = "display: none; position: absolute; -webkit-box-shadow: 3px 3px 3px #666;"
%>
<div style="width: ${width}; height: ${height}; border: 1px solid black; ${style}" id="${field_name}_div">
	<script type="text/javascript" src="http://maps.google.com/maps?file=api&amp;v=2&amp;sensor=false&amp;key=ABQIAAAAIi6se4J7Z6hKgcsUhgiErRQS76dJNGDaz2wU_zf_o-LlW8DpkhThfgwBtV5bzJz31JYsXf4OsNuZZw"></script>
	<script type="text/javascript" src="/javascript/mxn/mxn.js?(google)"></script>
	<script type="text/javascript">
${field_name}_map = new mxn.Mapstraction("${field_name}_div", "google");
${field_name}_map.setCenterAndZoom(new mxn.LatLonPoint(${lat}, ${lon}), ${zoom});
${field_name}_map.addLargeControls();

${field_name}_map_marker = new mxn.Marker(new mxn.LatLonPoint(${lat}, ${lon}));
${field_name}_map.addMarker(${field_name}_map_marker);
${field_name}_map.click.addHandler(function(event_name, event_source, event_args) {
	var p = event_args.location;
	${field_name}_map.removeMarker(${field_name}_map_marker); // no marker.setLocation()?
	${field_name}_map_marker = new mxn.Marker(p);
	${field_name}_map.addMarker(${field_name}_map_marker);
	document.getElementById("${field_name}").value = p.lon+","+p.lat;

	namebox = document.getElementById("${field_name}_name")
	if(namebox.value == "" || namebox.value.match(/^[\d\., ]+$/)) {
		namebox.value = Math.round(p.lon*10000)/10000+", "+Math.round(p.lat*10000)/10000;
	}
});

autocomplete_location("${field_name}", ${field_name}_map);
	</script>
</div>
</%def>

<%def name="minimap(name='map', width='250px', height='250px', lon=1.08, lat=51.28, zoom=13)">
<div style="width: ${width}; height: ${height}; border: 1px solid black;" id="${name}_div"></div>
<script type="text/javascript" src="http://openlayers.org/api/OpenLayers.js"></script>
<script type="text/javascript" src="/javascript/mxn/mxn.js?(openlayers)"></script>
<script type="text/javascript">
	${name} = new mxn.Mapstraction("${name}_div", "openlayers");
	${name}.setCenterAndZoom(new mxn.LatLonPoint(${lat}, ${lon}), ${zoom});
	${name}.addControls({pan: false, zoom: false, map_type: false});
</script>
</%def>
