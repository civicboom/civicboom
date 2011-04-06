
// mobile safari does weird things with position:fixed
if(navigator.platform == 'iPad' || navigator.platform == 'iPhone' || navigator.platform == 'iPod') {
	//$("footer").css("position", "static");
	//$("#app").css("width", "100%").css("height", "100%").css("overflow", "scroll");
};

var r = $(document).getUrlParam("r");
/*
if(r) {
	$.cookie('r', r, { expires: new Date((new Date()).getTime() + 60*60*1000), path: '/' });
}
*/
if(r && r == "qr") {
	var uagent = navigator.userAgent.toLowerCase();
	if(uagent.search("android") > -1) {
		var url = "market://details?id=com.civicboom.mobile2";
		window.location = url;
	}
}
