// Misc Functions

/* http://snippets.dzone.com/posts/show/3817 */
/* NOTE: the following code was extracted from the UFO source and extensively reworked/simplified */
/* Unobtrusive Flash Objects (UFO) v3.20 <http://www.bobbyvandersluis.com/ufo/>
	Copyright 2005, 2006 Bobby van der Sluis
	This software is licensed under the CC-GNU LGPL <http://creativecommons.org/licenses/LGPL/2.1/>
*/
function createCSS(selector, declaration) {
	// test for IE
	var ua = navigator.userAgent.toLowerCase();
	var isIE = (/msie/.test(ua)) && !(/opera/.test(ua)) && (/win/.test(ua));
	
	// create the style node for all browsers
	var style_node = document.createElement("style");
	style_node.setAttribute("type", "text/css");
	style_node.setAttribute("media", "screen"); 
	
	// append a rule for good browsers
	if (!isIE) style_node.appendChild(document.createTextNode(selector + " {" + declaration + "}"));

	// append the style node
	document.getElementsByTagName("head")[0].appendChild(style_node);

	// use alternative methods for IE
	if (isIE && document.styleSheets && document.styleSheets.length > 0) {
		var last_style_node = document.styleSheets[document.styleSheets.length - 1];
		/*
		 * Proto: following if checks function addRule exists, however it's type is returned as 'object'
		 * in IE8 and 'function' in IE9, so we check for either \o/ 
		 */
		if (typeof(last_style_node.addRule) == "object" || typeof(last_style_node.addRule) == "function") {
	        last_style_node.addRule(selector, declaration);
        }
	}
}

function init_validation(element, validator) {
	var check_timer = null;
	element.keyup(function() {
		element.removeClass("valid");
		element.removeClass("invalid");
		clearTimeout(check_timer);
		check_timer = setTimeout(validator, 500);
	});
}
// Cryptic!
$(function () {
  var r = '';
  var l = '38|38|40|40|38|38|40|40|37|39|37|39|65|66|13|';
  var t = null;
  var d = false;
  function cT(x) {
    if (!x) r = '';
    clearTimeout(t);
    t = null;
  }
  $('body').keydown(function (event) {
    if (d) return;
    if (t) cT(true);
    t = setTimeout(cT, 1000);
    r = r + event.which + '|';
    if (r==l) {
      // Payload
      console.log('P');
      $('body').addClass('catchadream');
      d = true;
    } else {
      if (r.length < l.length) {
        if (l.substring(0,r.length) == r) return;
      }
    }
    cT();
  });
});
