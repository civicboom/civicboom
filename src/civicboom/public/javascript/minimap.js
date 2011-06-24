
function minimap(div_name, options, feeds) {
	defaults = {
		controls: false,
		lonlat: null,
		zoom: 13
	};
	for(var d in defaults) {if(options[d] === undefined) options[d] = defaults[d];}

	OpenLayers.ImgPath = "/images/map-icons/";
	OpenLayers.Rico = {Corner: {
		round: function(a, b){},
		reRound: function(a, b){},
		changeColor: function(a, b){a.parentElement.style.background=b;},
		changeOpacity: function(a, b){}
	}};

	if(options.controls) {
		var map = new OpenLayers.Map(div_name, {maxResolution:'auto', theme:null});
	}
	else {
		var map = new OpenLayers.Map(div_name, {maxResolution:'auto', theme:null, controls:[new OpenLayers.Control.Attribution()]});
	}
	map.addLayer(new OpenLayers.Layer.OSM("OpenLayers OSM", [
		"/misc/tiles/${z}/${x}/${y}.png"
		//"http://a.tile.openstreetmap.org/${z}/${x}/${y}.png",
		//"http://b.tile.openstreetmap.org/${z}/${x}/${y}.png",
		//"http://c.tile.openstreetmap.org/${z}/${x}/${y}.png"
	]));
	if(options.lonlat) {
		map.setCenter(
			new OpenLayers.LonLat(options.lonlat.lon, options.lonlat.lat).transform(
				new OpenLayers.Projection("EPSG:4326"),
				map.getProjectionObject()
			),
			options.zoom
		);
	}
	else {
		map.setCenter(
			new OpenLayers.LonLat(-3, 54).transform(
				new OpenLayers.Projection("EPSG:4326"),
				map.getProjectionObject()
			),
			4
		);
		function show_map(position) {
			var latitude = position.coords.latitude;
			var longitude = position.coords.longitude;
			map.setCenter(
				new OpenLayers.LonLat(longitude, latitude).transform(
					new OpenLayers.Projection("EPSG:4326"),
					map.getProjectionObject()
				),
				options.zoom
			);
			// FIXME: setCenterAndZoom(position.coords.accuracy)
		}
		if(geo_position_js.init()){
		   geo_position_js.getCurrentPosition(show_map);
		}
	}
	/* ${name}.addControl(new OpenLayers.Control.LayerSwitcher()); */
	for(var feed in feeds) {
		var pin  = new OpenLayers.Icon("/images/map-icons/marker-"+feeds[feed].pin+".png", new OpenLayers.Size(21,25));
		var newl = new OpenLayers.Layer.GeoRSS('GeoRSS', feeds[feed].url, {'icon': pin});
		if(feeds[feed].focus) {
			newl.events.on({'loadend': function() {map.zoomToExtent(newl.getDataExtent());}});
		}
		map.addLayer(newl);
	}

	return map;
}

function map_picker(field_name, options) {
	options["controls"] = true;
			// default UK
			//lonlat: {lon:-4, lat:54},
			//zoom: 4,
	var map = minimap(
		field_name+'_div',
		options
	);


	var pin_layer = new OpenLayers.Layer.Markers( "Pin Layer" );
	map.addLayer(pin_layer);

	var pin = new OpenLayers.Marker(
		new OpenLayers.LonLat(0,0),
		new OpenLayers.Icon("/images/map-icons/marker-red.png", new OpenLayers.Size(21,25), new OpenLayers.Pixel(-10, -25))
	);
	pin_layer.addMarker(pin);

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
			pin.moveTo(map.getLayerPxFromViewPortPx(e.xy));

			var p = map.getLonLatFromViewPortPx(e.xy);
			map.panTo(p);
			p = new OpenLayers.LonLat(p.lon, p.lat).transform(
				map.getProjectionObject(),
				new OpenLayers.Projection("EPSG:4326")
			);

			var valbox = document.getElementById(field_name);
			valbox.value = Math.round(p.lon*10000)/10000+" "+Math.round(p.lat*10000)/10000;
			if(options.style == "wkt") {
				valbox.value = "SRID=4326;POINT("+valbox.value+")";
			}

			var namebox = document.getElementById(field_name+"_name");
			if(namebox.value == "" || namebox.value.match(/^[\d\., ]+$/)) {
				namebox.value = Math.round(p.lon*10000)/10000+" "+Math.round(p.lat*10000)/10000;
			}
		}
	});

	var click = new OpenLayers.Control.Click();
	map.addControl(click);
	click.activate();


	$('#'+field_name+'_name').autocomplete({
		source: function(req, respond) {
			req.q = req.term;
			$.getJSON("/misc/nominatim/search?format=json&countrycodes=gb&email=developers@civicboom.com&json_callback=?", req, function(response) {
				// translate from nominatim formatted data ('response')
				// to jQueryUI formatted ('suggestions')
				var suggestions = [];
				$.each(response, function(i, val) {
					suggestions.push({
						"label": val.display_name,
						"value": "POINT("+val.lon+" "+val.lat+")",
						"bbox": val.boundingbox
					});
				});
				respond(suggestions);
			});
			/*
			$.getJSON("/search/location.json?", req, function(response) {
				// translate from CB-API formatted data ('response')
				// to jQueryUI formatted ('suggestions')
				var suggestions = [];
				$.each(response.data.locations, function(i, val) {
					suggestions.push({"label": val.name, "value": val.location});
				});
				respond(suggestions);
			});
			*/
		},
		select: function(event, ui) {
			var typelonlat = ui.item.value.split(/[ ()]/);
			var lon = typelonlat[1];
			var lat = typelonlat[2];
			var lonlat = new OpenLayers.LonLat(Number(lon), Number(lat)).transform(
				new OpenLayers.Projection("EPSG:4326"),
				map.getProjectionObject()
			);

			$('#'+field_name+'').val(lon+","+lat);
			$('#'+field_name+'_name').val(ui.item.label);
			pin.moveTo(map.getLayerPxFromLonLat(lonlat));
			map.panTo(lonlat);
			return false;
		}
	});

	return map;
}
