function autocomplete_location(name, map) {
	gis_box = name;
	location_box = name+"_name";
	completions_box = name+"_comp";

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

		var typelonlat = oData.location.split(/[ ()]/);
		var lon = typelonlat[1];
		var lat = typelonlat[2];
		if(gis_box) {
			document.getElementById(gis_box).value = lon+","+lat;
		}

		if(map) {
			map.setCenterAndZoom(new mxn.LatLonPoint(lon, lat), 10);
		}
	});
};
