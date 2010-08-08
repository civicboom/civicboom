function autocomplete_location(location_box, completions_box, gis_box) {
	// Data Source setup
    var oDS = new YAHOO.util.XHRDataSource("/search/location.json");
    oDS.responseType = YAHOO.util.XHRDataSource.TYPE_JSON;
    oDS.maxCacheEntries = 5;
	oDS.responseSchema = {
		resultsList: "ResultSet.Results",
		fields: ["name", "location", "type"]
	};

    // AutoComplete setup
    var oAC = new YAHOO.widget.AutoComplete(location_box, completions_box, oDS);
	oAC.maxResultsDisplayed = 20;
	oAC.resultTypeList = false;
	oAC.formatResult = function(oResultData, sQuery, sResultMatch) {
		return (sResultMatch + " (" +  oResultData.type + ")");
	};
	oAC.itemSelectEvent.subscribe(function(sType, aArgs) {
		var oMyAcInstance = aArgs[0]; // your AutoComplete instance
		var elListItem = aArgs[1]; // the <li> element selected in the suggestion container
		var oData = aArgs[2]; // object literal of data for the result
		if(gis_box) {
			var typelonlat = oData.location.split(/[ ()]/);
			document.getElementById(gis_box).value = typelonlat[1]+","+typelonlat[2];
		}

		var map = document.getElementById(gis_box+"_map");
		if(map) {
			var typelonlat = oData.location.split(/[ ()]/);
			lonlat = new OpenLayers.LonLat(typelonlat[1], typelonlat[2]).transform(
				new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984 (lon/lat)
				new OpenLayers.Projection("EPSG:900913") // to Spherical Mercator Projection (OSM uses this)
			);
			map.setCenter(lonlat, 13);
		}
	});
};
