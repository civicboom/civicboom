<%def name="location_picker(field_name='location', size='250px', lon=1.08, lat=51.28, zoom=13)">
<div style="width: ${size}; padding-bottom: 2em;">
	<input id="${field_name}_name" name="${field_name}_name" type="text" onfocus="show_${field_name}()" onblur="hide_${field_name}()">
	<div id="${field_name}_comp"></div>
	<input id="${field_name}" name="${field_name}" type="hidden">
</div>

<div style="width: ${size}; height: ${size}; border: 1px solid black; display: none; position: absolute; -webkit-box-shadow: 3px 3px 3px #666;
" id="${field_name}_div">
	<script type="text/javascript" src="http://maps.google.com/maps?file=api&amp;v=2&amp;sensor=false&amp;key=ABQIAAAAIi6se4J7Z6hKgcsUhgiErRQS76dJNGDaz2wU_zf_o-LlW8DpkhThfgwBtV5bzJz31JYsXf4OsNuZZw"></script>
	<script type="text/javascript" src="/javascript/mxn/mxn.js?(google)"></script>
	<script type="text/javascript">
${field_name}_map = new mxn.Mapstraction("${field_name}_div", "google");
${field_name}_map.setCenterAndZoom(new mxn.LatLonPoint(${lat}, ${lon}), ${zoom});
${field_name}_map.addControls({pan: false, zoom: false, map_type: false});

${field_name}_map_marker = new mxn.Marker(new mxn.LatLonPoint(${lat}, ${lon}));
${field_name}_map.addMarker(${field_name}_map_marker);
${field_name}_map.click.addHandler(function(event_name, event_source, event_args) {
	var p = event_args.location;
	${field_name}_map.removeMarker(${field_name}_map_marker); // no marker.setLocation()?
	${field_name}_map_marker = new mxn.Marker(p);
	${field_name}_map.addMarker(${field_name}_map_marker);
	document.getElementById("${field_name}").value = p.lon+","+p.lat;
});

autocomplete_location("${field_name}", ${field_name}_map);

// FIXME: YUI shinyness
function show_${field_name}() {
	document.getElementById("${field_name}_div").style.display = "block";
}
function hide_${field_name}() {
	document.getElementById("${field_name}_div").style.display = "none";
}
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
