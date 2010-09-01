// Misc Functions

function confirm_before_follow_link(link_element, message) {
  var confirmation = confirm(message);
  if !(confirmation) {break;}
  else {
    //window.location = link_element;
  }
}


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