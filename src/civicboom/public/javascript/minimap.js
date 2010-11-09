
function minimap(div_name, options, feeds) {
	defaults = {
		controls: false,
		lonlat: null,
		zoom: 13
	};
	for(var d in defaults) {if(!options[d]) options[d] = defaults[d];}

	OpenLayers.ImgPath = "/images/map-icons/";
	if(options.controls) {
		var map = new OpenLayers.Map(div_name, {maxResolution:'auto', theme:null});
	}
	else {
		var map = new OpenLayers.Map(div_name, {maxResolution:'auto', theme:null, controls:[new OpenLayers.Control.Attribution()]});
	}
	map.addLayer(new OpenLayers.Layer.OSM("OpenLayers OSM", [
		"http://a.tile.openstreetmap.org/${z}/${x}/${y}.png",
		"http://b.tile.openstreetmap.org/${z}/${x}/${y}.png",
		"http://c.tile.openstreetmap.org/${z}/${x}/${y}.png"
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
		var pin  = new OpenLayers.Icon("/images/pins/"+feeds[feed].pin+".png", new OpenLayers.Size(21,25));
		var newl = new OpenLayers.Layer.GeoRSS('GeoRSS', feeds[feed].url, {'icon': pin});
		if(feeds[feed].focus) {
			newl.events.on({'loadend': function() {map.zoomToExtent(newl.getDataExtent());}});
		}
		map.addLayer(newl);
	}

	return map;
}
