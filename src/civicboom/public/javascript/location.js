function autocomplete_location(location_box, completions_box, gis_box) {
	// Data Source setup
    var oDS = new YAHOO.util.XHRDataSource("/search/location.txt");
    oDS.responseType = YAHOO.util.XHRDataSource.TYPE_TEXT;
    oDS.responseSchema = {
        recordDelim: "\n",
        fieldDelim: "\t",
		fields: ["name", "location", "type"]
    };
    oDS.maxCacheEntries = 5;

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
			document.getElementById(gis_box).value = oData.location;
		}
	});
};
