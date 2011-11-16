// for https support and hopefully less relying on OSM's already
// stressed servers, proxy requests

// cloudfront is faster for tiles, and less fluff in web server logs
//var tiles_root = "https://d2mjgy2zzircki.cloudfront.net";
var tiles_root = "/misc/tiles";

// nominatim doesn't set caching headers, so cloudfront is little benefit;
// plus nominatim's web server is confused by the unknown vhost
//var nominatim_root = "https://d1x3grabsleh1t.cloudfront.net";
var nominatim_root = "/misc/nominatim";


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
		changeColor: function(a, b){ a.parentNode.style.background=b; },
		changeOpacity: function(a, b){}
	}};

	if(options.controls) {
		var map = new OpenLayers.Map(div_name, {maxResolution:'auto', theme:null});
	}
	else {
		var map = new OpenLayers.Map(div_name, {maxResolution:'auto', theme:null, controls:[new OpenLayers.Control.Attribution()]});
	}
	map.addLayer(new OpenLayers.Layer.OSM("OpenLayers OSM", [
		tiles_root+"/${z}/${x}/${y}.png"
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
	var focus_layer = null;
	for(var feed in feeds) {
		if(!feeds.hasOwnProperty(feed)) continue;
		var pin  = new OpenLayers.Icon("/images/map-icons/marker-"+feeds[feed].pin+".png", new OpenLayers.Size(21,25));
		var newl = new OpenLayers.Layer.GeoRSS('GeoRSS', feeds[feed].url, {'icon': pin});
		if(feeds[feed].focus) {
			focus_layer = newl;
			focus_layer.events.on({'loadend': function() {
				// even though the callback is defined here and now, newl will
				// be redefined in the next iteration of foreach(feeds), and
				// the callback will call the redefined newl o_______________O
				// wtfix: use a dedicated variable in an outer scope which
				// is specifically for the focus layer.
				//map.zoomToExtent(newl.getDataExtent());
				map.zoomToExtent(focus_layer.getDataExtent());
			}});
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

	/*
	var london = [
		[-0.5110354,51.4676356], [-0.4994147,51.4843281], [-0.4885921,51.5003407], [-0.4828843,51.5072059],
		[-0.4900512,51.5142572], [-0.490604,51.5267813], [-0.4903121,51.5326976], [-0.492621,51.5359384],
		[-0.4934201,51.5410781], [-0.4909518,51.5451977], [-0.4893562,51.547261], [-0.4871346,51.5531086],
		[-0.4842752,51.5593863], [-0.4839983,51.5709305], [-0.4951652,51.5848648], [-0.4994388,51.5952316],
		[-0.4963172,51.6024522], [-0.4984369,51.6120036], [-0.5001932,51.6234555], [-0.4941493,51.630884],
		[-0.4805543,51.623709], [-0.4677645,51.6162386], [-0.4483933,51.6154072], [-0.4265225,51.6174348],
		[-0.3905827,51.6152822], [-0.3602052,51.6240784], [-0.3330625,51.6330535], [-0.3043899,51.636215],
		[-0.2943155,51.6356541], [-0.2837346,51.6378747], [-0.2741323,51.6397666], [-0.2683362,51.6426657],
		[-0.262161,51.644318], [-0.2554189,51.643259], [-0.2509236,51.6549087], [-0.2489115,51.6559104],
		[-0.237862,51.6578918], [-0.2272864,51.6577284], [-0.2087008,51.6638723], [-0.1999551,51.6704845],
		[-0.1891893,51.6661367], [-0.169645,51.6763791], [-0.1470694,51.6857186], [-0.1064666,51.69188],
		[-0.0677141,51.6842577], [-0.0230177,51.6815037], [-0.0088771,51.6610236], [-0.0011355,51.6435786]
	];
	$.getJSON("/misc/nominatim/search?format=json&countrycodes=gb&email=developers@civicboom.com&&polygon=1&json_callback=?", {"q": "greater london"}, function(r) {
		london = r[0].polygonpoints;
		console.log("London loaded "+london.length);
	});

	//+ Jonas Raoni Soares Silva
	//@ http://jsfromhell.com/math/is-point-in-poly [v1.0]
	function isPointInPoly(poly, pt){
		for(var c = false, i = -1, l = poly.length, j = l - 1; ++i < l; j = i)
			((poly[i][1] <= pt[1] && pt[1] < poly[j][1]) || (poly[j][1] <= pt[1] && pt[1] < poly[i][1]))
				&& (pt[0] < (poly[j][0] - poly[i][0]) * (pt[1] - poly[i][1]) / (poly[j][1] - poly[i][1]) + poly[i][0])
				&& (c = !c);
		return c;
	}
	*/

	$('#'+field_name+'_name').autocomplete({
		source: function(req, respond) {
			req.q = req.term;
			$.getJSON(nominatim_root+"/search?format=json&countrycodes=gb&email=developers@civicboom.com&addressdetails=1&json_callback=?", req, function(response) {
				// translate from nominatim formatted data ('response')
				// to jQueryUI formatted ('suggestions')
				var suggestions = [];
				$.each(response, function(i, val) {
					var label_parts = [];
					for(var level in val.address) {
						var name = val.address[level];
						// there is no county of London; approximate it by replacing the
						// county with "London" if the location is within a london-sized
						// circle
						if(level == "county") {
							var dist_from_cc = Math.sqrt(
								Math.pow(Math.abs(val.lon - (-0.12)), 2) +
								Math.pow(Math.abs(val.lat -  51.5  ), 2)
							);
							//console.log(val.display_name+" ("+val.lon+", "+val.lat+") is "+dist_from_cc+" degrees from Charing Cross");
							if(dist_from_cc < 0.4) {
								name = "London";
							}
							/*
							if(isPointInPoly(london, [val.lon, val.lat])) {
								name = "London";
							}
							*/
						}
						name = name.replace(" (Ceremonial)", "");
						name = name.replace(" (ceremonial)", "");
						if(level == "state" || level == "state_district" || level == "country_code") break;
						label_parts.push(name);
					}
					suggestions.push({
						"label": label_parts.join(", "),
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
