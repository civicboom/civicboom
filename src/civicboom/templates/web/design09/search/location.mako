<%inherit file="/web/html_base.mako"/>

##------------------------------------------------------------------------------
## Title - Override
##------------------------------------------------------------------------------
<%def name="title()">${_("Search")}</%def>


##------------------------------------------------------------------------------
## Body
##------------------------------------------------------------------------------

<%def name="body()">
<!-- Combo-handled YUI CSS files: -->
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/combo?2.8.1/build/autocomplete/assets/skins/sam/autocomplete.css">
<!-- Combo-handled YUI JS files: -->
<script type="text/javascript" src="http://yui.yahooapis.com/combo?2.8.1/build/yahoo-dom-event/yahoo-dom-event.js&2.8.1/build/animation/animation-min.js&2.8.1/build/connection/connection-min.js&2.8.1/build/datasource/datasource-min.js&2.8.1/build/autocomplete/autocomplete-min.js"></script>

<form>
    <label for="myInput">Search our database:</label>
    <div id="myAutoComplete">
        <input id="query" name="query" type="text">
        <div id="myContainer"></div>
    </div>
    <input type="submit">
</form>

	% for row in results:
		${row.name}
	% endfor
<script>
YAHOO.example.BasicRemote = function() {
    // Use an XHRDataSource
    var oDS = new YAHOO.util.XHRDataSource("/search/location.txt");
    // Set the responseType
    oDS.responseType = YAHOO.util.XHRDataSource.TYPE_TEXT;
    // Define the schema of the delimited results
    oDS.responseSchema = {
        recordDelim: "\n",
        fieldDelim: "\t",
		fields: ["name", "type"]
    };
    // Enable caching
    oDS.maxCacheEntries = 5;

    // Instantiate the AutoComplete
    var oAC = new YAHOO.widget.AutoComplete("query", "myContainer", oDS);
	oAC.maxResultsDisplayed = 20;
	//oAC.minQueryLength = 3;
	//oAC.typeAhead = true;

	oAC.resultTypeList = false;
	oAC.formatResult = function(oResultData, sQuery, sResultMatch) {
		return (sResultMatch + " (" +  oResultData.type + ")");
	};

    return {
        oDS: oDS,
        oAC: oAC
    };
}();
</script>
</%def>
