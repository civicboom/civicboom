<%def name="location_picker(field_name='location', width='250px', height='250px', lon=1.08, lat=51.28, zoom=13, always_show_map=False)">
<input id="${field_name}_name" name="${field_name}_name" type="text" style="width: ${width}">
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

<%
style = ""
if not always_show_map:
	style = "display: none; position: absolute; -webkit-box-shadow: 3px 3px 3px #666;"
%>
<div style="width: ${width}; height: ${height}; border: 1px solid black; ${style}" id="${field_name}_div">
	<script type="text/javascript" src="http://maps.google.com/maps?file=api&amp;v=2&amp;sensor=false&amp;key=ABQIAAAAIi6se4J7Z6hKgcsUhgiErRQS76dJNGDaz2wU_zf_o-LlW8DpkhThfgwBtV5bzJz31JYsXf4OsNuZZw"></script>
	<script type="text/javascript" src="/javascript/mxn/mxn.js"></script>
	<script type="text/javascript" src="/javascript/mxn/mxn.core.js"></script>
	<script type="text/javascript" src="/javascript/mxn/mxn.google.core.js"></script>
	<script type="text/javascript">
$(function() {
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

	$('#${field_name}_name').autocomplete({
		source: function(req, respond) {
			$.getJSON("/search/location.json?", req, function(response) {
				// translate from CB-API formatted data ('response')
				// to jQueryUI formatted ('suggestions')
				var suggestions = [];
				$.each(response.data.locations, function(i, val) {
					suggestions.push({"label": val.name, "value": val.location});
				});
				respond(suggestions);
			});
		},
		select: function(event, ui) {
			var typelonlat = ui.item.value.split(/[ ()]/);
			var lon = typelonlat[1];
			var lat = typelonlat[2];

			$('#${field_name}').val(lon+","+lat);
			$('#${field_name}_name').val(ui.item.label);
			${field_name}_map.setCenterAndZoom(new mxn.LatLonPoint(Number(lat), Number(lon)), 13);
			return false;
		}
	});
});
	</script>
</div>
</%def>

<%def name="minimap(name='map', width='250px', height='250px', lon=None, lat=None, zoom=13, feeds=[], controls=False)">
<div style="width: ${width}; height: ${height}; border: 1px solid black;" id="${name}_div"></div>
<script src="http://openlayers.org/api/OpenLayers.js"></script>
<script src="/javascript/gears_init.js"></script>
<script src="/javascript/geo.js"></script>
<script type="text/javascript">
$(function() {
% if controls:
	${name} = new OpenLayers.Map('${name}_div', {maxResolution:'auto'});
% else:
	${name} = new OpenLayers.Map('${name}_div', {maxResolution:'auto', controls:[]});
% endif
	${name}.addLayer(new OpenLayers.Layer.OSM("OpenLayers OSM"));
% if lon and lat:
	${name}.setCenter(
		new OpenLayers.LonLat(${lon}, ${lat}).transform(
			new OpenLayers.Projection("EPSG:4326"),
			${name}.getProjectionObject()
		),
		${zoom}
	);
% else:
	function show_map(position) {
		var latitude = position.coords.latitude;
		var longitude = position.coords.longitude;
		${name}.setCenter(
			new OpenLayers.LonLat(longitude, latitude).transform(
				new OpenLayers.Projection("EPSG:4326"),
				${name}.getProjectionObject()
			)
		);
		// FIXME: setCenterAndZoom(position.coords.accuracy)
	}
	if(geo_position_js.init()){
	   geo_position_js.getCurrentPosition(show_map);
	}
% endif
	/* ${name}.addControl(new OpenLayers.Control.LayerSwitcher()); */
% for feed in feeds:
	var pin  = new OpenLayers.Icon("/images/pins/${feed['pin']}.png", new OpenLayers.Size(21,25));
	var newl = new OpenLayers.Layer.GeoRSS( 'GeoRSS', '${feed['url']}', {'icon': pin});
	${name}.addLayer(newl);
% endfor
});
</script>
</%def>
