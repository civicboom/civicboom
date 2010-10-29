<%def name="location_picker(field_name='location', width='250px', height='250px', lon=None, lat=None, zoom=13, always_show_map=False)">
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
	<script src="/javascript/OpenLayers.js"></script>
	<script src="/javascript/gears_init.js"></script>
	<script src="/javascript/geo.js"></script>
	<script type="text/javascript">
$(function() {
	var ${field_name}_map = new OpenLayers.Map('${field_name}_div', {maxResolution:'auto'});
	${field_name}_map.addLayer(new OpenLayers.Layer.OSM("OpenLayers OSM"));
% if lon != None and lat != None:
	${field_name}_map.setCenter(
		new OpenLayers.LonLat(${lon}, ${lat}).transform(
			new OpenLayers.Projection("EPSG:4326"),
			${field_name}_map.getProjectionObject()
		),
		${zoom}
	);
% else:
	function show_map(position) {
		var latitude = position.coords.latitude;
		var longitude = position.coords.longitude;
		${field_name}_map.setCenter(
			new OpenLayers.LonLat(longitude, latitude).transform(
				new OpenLayers.Projection("EPSG:4326"),
				${field_name}_map.getProjectionObject()
			),
			${zoom}
		);
		// FIXME: setCenterAndZoom(position.coords.accuracy)
	}
	if(geo_position_js.init()){
	   geo_position_js.getCurrentPosition(show_map);
	}
% endif

	OpenLayers.Control.Click = OpenLayers.Class(OpenLayers.Control, {                
		defaultHandlerOptions: {
			'single': true,
			'double': false,
			'pixelTolerance': 0,
			'stopSingle': false,
			'stopDouble': false
		},

		initialize: function(options) {
			this.handlerOptions = OpenLayers.Util.extend({}, this.defaultHandlerOptions);
			OpenLayers.Control.prototype.initialize.apply(this, arguments); 
			this.handler = new OpenLayers.Handler.Click(
				this, {
					'click': this.trigger
				}, this.handlerOptions
			);
		}, 

		trigger: function(e) {
			 var p = ${field_name}_map.getLonLatFromViewPortPx(e.xy);
			 p = new OpenLayers.LonLat(p.lon, p.lat).transform(
				 ${field_name}_map.getProjectionObject(),
				 new OpenLayers.Projection("EPSG:4326")
			 );

			 namebox = document.getElementById("${field_name}_name");
			 if(namebox.value == "" || namebox.value.match(/^[\d\., ]+$/)) {
				 namebox.value = Math.round(p.lon*10000)/10000+", "+Math.round(p.lat*10000)/10000;
			 }
		 }
	});

	var click = new OpenLayers.Control.Click();
	${field_name}_map.addControl(click);
	click.activate();


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
			${field_name}_map.setCenterAndZoom(
				new OpenLayers.LonLat(Number(longitude), Number(latitude)).transform(
					new OpenLayers.Projection("EPSG:4326"),
					${field_name}_map.getProjectionObject()
				),
				13
			);
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
	var ${name} = new OpenLayers.Map('${name}_div', {maxResolution:'auto'});
% else:
	var ${name} = new OpenLayers.Map('${name}_div', {maxResolution:'auto', controls:[new OpenLayers.Control.Attribution()]});
% endif
	${name}.addLayer(new OpenLayers.Layer.OSM("OpenLayers OSM"));
% if lon != None and lat != None:
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
	% if 'focus' in feed and feed['focus'] == True:
		newl.events.on({'loadend': function() {${name}.zoomToExtent(newl.getDataExtent());}});
	% endif
	${name}.addLayer(newl);
% endfor
});
</script>
</%def>
