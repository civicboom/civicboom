function autocomplete_member(member_box, completions_box, gis_box) {
	// Data Source setup
    var oDS = new YAHOO.util.XHRDataSource("/search/member.json");
    oDS.responseType = YAHOO.util.XHRDataSource.TYPE_JSON;
    oDS.maxCacheEntries = 5;
	oDS.responseSchema = {
		resultsList: "ResultSet.Results",
		fields: ["name", "username", "type"]
	};

    // AutoComplete setup
    var oAC = new YAHOO.widget.AutoComplete(member_box, completions_box, oDS);
	oAC.maxResultsDisplayed = 20;
	oAC.resultTypeList = false;
	//oAC.delimChar = ","; // multiple members
	oAC.formatResult = function(oResultData, sQuery, sResultMatch) {
		return (
			oResultData.name +
			" (" +  oResultData.username + ")" +
			"<span style='float: right; color: grey;'>" + oResultData.type + "</span>"
		);
	};
	oAC.itemSelectEvent.subscribe(function(sType, aArgs) {
		var oMyAcInstance = aArgs[0]; // your AutoComplete instance
		var elListItem = aArgs[1]; // the <li> element selected in the suggestion container
		var oData = aArgs[2]; // object literal of data for the result
		if(gis_box) {
			document.getElementById(gis_box).value = oData.username;
		}
	});
};
