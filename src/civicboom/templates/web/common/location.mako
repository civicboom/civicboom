<%def name="location_picker(field_name='location', width='250px', height='250px', always_show_map=False)">
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
	style = style + " display: none; position: absolute; -webkit-box-shadow: 3px 3px 3px #666;"
%>
<div style="width: ${width}; height: ${height}; border: 1px solid black; ${style}" id="${field_name}_div"></div>
<%
if config['development_mode']:
	scripts_end.extend([
		'<script src="/javascript/OpenLayers.js"></script>',
		'<script src="/javascript/gears_init.js"></script>',
		'<script src="/javascript/geo.js"></script>',
		'<script src="/javascript/minimap.js"></script>',
	])
else:
	scripts_end.append(
		'<script src="/javascript/_combined.maps.js"></script>'
	)
%>
<script type="text/javascript">
$(function() {
	map = minimap(
		'${field_name}_div',
		{
			controls: true,
		}
	);

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
			 var p = map.getLonLatFromViewPortPx(e.xy);
			 p = new OpenLayers.LonLat(p.lon, p.lat).transform(
				 map.getProjectionObject(),
				 new OpenLayers.Projection("EPSG:4326")
			 );

			 namebox = document.getElementById("${field_name}_name");
			 if(namebox.value == "" || namebox.value.match(/^[\d\., ]+$/)) {
				 namebox.value = Math.round(p.lon*10000)/10000+", "+Math.round(p.lat*10000)/10000;
			 }
		 }
	});

	var click = new OpenLayers.Control.Click();
	map.addControl(click);
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
			map.setCenter(
				new OpenLayers.LonLat(Number(lon), Number(lat)).transform(
					new OpenLayers.Projection("EPSG:4326"),
					map.getProjectionObject()
				),
				13
			);
			return false;
		}
	});
});
</script>
</%def>

<%def name="minimap(name='map', width='250px', height='250px', lon=None, lat=None, zoom=13, feeds=[], controls=False)">
<div style="width: ${width}; height: ${height}; border: 1px solid black;" id="${name}_div"></div>
<%
import json

if config['development_mode']:
	scripts_end.extend([
		'<script src="/javascript/OpenLayers.js"></script>',
		'<script src="/javascript/gears_init.js"></script>',
		'<script src="/javascript/geo.js"></script>',
		'<script src="/javascript/minimap.js"></script>',
	])
else:
	scripts_end.append(
		'<script src="/javascript/_combined.maps.js"></script>'
	)
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
