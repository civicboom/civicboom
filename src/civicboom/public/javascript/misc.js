// Misc Functions


// References - http://stackoverflow.com/questions/247483/http-get-request-in-javascript
//              http://www.jibbering.com/2002/4/httprequest.html
function getHTML(url, get_complete_function) {
    var xmlHttp = null;
    function ProcessRequest() {
        //YAHOO.log("got the request!! State:" + xmlHttp.readyState + " status:"+xmlHttp.status);
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            get_complete_function(xmlHttp.responseText);
            //head_complete_function(xmlHttp.getAllResponseHeaders());
        }
    }
    xmlHttp = new XMLHttpRequest(); 
    xmlHttp.onreadystatechange = ProcessRequest;
    xmlHttp.open("GET", url, true);
    xmlHttp.send(null);
}

// Requires toggle_div.js functions
function setSingleCSSClass(element_to_style, class_to_set, parent_id) {
    // Find all occurances of this class
    var elements = getElementByClass(class_to_set, parent_id);
    for (var element in elements) {
        // Remove the class
        removeClass(elements[element], class_to_set);
    }
    // Add the class to the specifyed element
    addClass(element_to_style, class_to_set);
}

function flash_message(json_message) {
	if (typeof(json_message) == "string") {json_message = {status:'ok', message:json_message};}
	if (json_message.message != "") {
		$("#flash_message").removeClass("status_error").removeClass("status_ok").addClass("status_"+json_message.status);
		$("#flash_message").text(json_message.message).slideDown("slow").delay(5000).slideUp("slow");
	}
}
