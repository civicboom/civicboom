/*
 DIV toggle/hide tools - AllanC
 
 Base Concept:
  - See The Essential Guide to CSS and HTML Web Design - By Craig Grannell - page 190
  - Additions by AllanC
 
 HTML reminder
 if you want a div hidden by default
 in CSS:
   .hideable {display: none;}
 or in HTML:
  <div id="name_thing" style="display: none;">
  
  The above is bad practice, because javascriptless browsers cant turn the divs back on.


  -Use-

  After <BODY> run this
  
   
  <script type="text/javascript">
    createCSS(".hideable","display: none;")
    // Old way, incompatable with IE
    //var sheet = document.createElement('style')
    //sheet.innerHTML = ".hideable {display: none;}";
    //document.body.appendChild(sheet);
  </script>

 
 any element with a class 'hideable' will be hidden by default. e.g.
 
 <div class="thing other_thing hideable">
   I will be hidden on page load
 </div>
 
  -OLD-
  used to have this at the bottom of the HTML but it was messey because elements were visuable during load
    
   But! dont do the above, because javascriptless browsers will never be able to reveal the content
   so just put this javascript at the bottom of you html to hide the elements dynamicly.
   For accessability we only want to hide the divs if javascript is enabled. 
   
   <script type="text/javascript">
     hide_all_hideable();
   </script>
   
  -Notes-
  
  (Grannell is a god ... but his javascript-overrides.css is overkill and fiddly.)
   
   
   
  -- Crude Example --
  
  <script type="text/javascript">
    var sheet = document.createElement('style')
    sheet.innerHTML = ".hideable {display: none;}";
    document.body.appendChild(sheet);
  </script>
  
  <a class="button_small button_small_style_1" href="#" title="Test" onclick="hide_all_except('test'); return false;">Test</a>
  <div id="test" class="hideable">
    <h2>test</h2>
    <a class="button_small button_small_style_1" href="#" onclick="show_all_hideable('test'); return false;">Show in testers</a>
    <a class="button_small button_small_style_1" href="#" onclick="hide_all_except('test_inside2','test'); return false;">Test</a>
    <div id="test_inside1" class="hideable">Archie</div>
    <div id="test_inside2" class="hideable">Bobbie</div>
    <div id="test_inside3" class="hideable">Chester</div>
  </div>
  
*/

//------------------------------------------------------------------------------
// Swap animatied
//------------------------------------------------------------------------------
var height_oringinal = new Array();

var animation_hide_function = function(elementId) {
  var b = new YAHOO.util.Anim(YAHOO.util.Dom.get(elementId));
  YAHOO.util.Dom.setStyle(elementId,'overflow','hidden');
  
  var element_region = YAHOO.util.Dom.getRegion(elementId);
  height_oringinal[elementId] = element_region.bottom - element_region.top;
  //height_oringinal[elementId] = document.getElementById(elementId).offsetHeight;
  //YAHOO.log("original height " + height_oringinal[elementId]);
  
  //b.attributes.opacity  = {to: 0};
  b.duration            = 0.5;
  b.attributes.height   = {to: 0};
  b.onComplete.subscribe(function() {
    YAHOO.util.Dom.setStyle(elementId,'display','none');
  });
  b.animate();
}

var animation_show_function = function(elementId) {
  YAHOO.util.Dom.setStyle(elementId,'display','block');
  
  if (elementId in height_oringinal) {
    var b = new YAHOO.util.Anim(YAHOO.util.Dom.get(elementId));
    b.duration            = 0.5;
    var padding_top    = parseInt(YAHOO.util.Dom.getStyle(elementId, 'padding-top'   ).replace("px",""));
    var padding_bottom = parseInt(YAHOO.util.Dom.getStyle(elementId, 'padding-bottom').replace("px",""));
    b.attributes.height   = {to: height_oringinal[elementId]-padding_top-padding_bottom};
    //b.onComplete.subscribe(function() { });
    b.animate();
  }
}

function swap_animated(targetId) {
  if   (YAHOO.util.Dom.getStyle(targetId,'display') == "block") {animation_hide_function(targetId);}
  else                                                          {animation_show_function(targetId);}
}

//------------------------------------------------------------------------------
// Swap 
//------------------------------------------------------------------------------
// Called with 
// <a href="#" title="Toggle section" onclick="swap('name'); return false;">Toggle div</a>
function swap(targetId) {
  var s = YAHOO.util.Dom.getStyle(targetId,'display');
  //YAHOO.log("Target display style is " + s);
  if (s == "block") {YAHOO.util.Dom.setStyle(targetId, 'display', 'none' );}
  else              {YAHOO.util.Dom.setStyle(targetId, 'display', 'block');}
  
  /*
  if (document.getElementById) {
    var target = document.getElementById(targetId);
    if (!(target===null)) {
      //YAHOO.log("Target style is " + target.style.display);
      if (target.style.display == "block") {target.style.display = "none";}
      else                                 {target.style.display = "block";}
    }
  }
  */
}


// Called with 
// <a href="#" title="Toggle section" onclick="toggle(this); return false;">Toggle div</a>
// Used to toggle things without needing to spoecify them by name
function toggle(toggler) {
  if (document.getElementById) {
    targetElement = toggler.parentNode.nextSibling;
    if (targetElement.className     == undefined) {targetElement = toggler.parentNode.nextSibling.nextSibling;}
    if (targetElement.style.display == "block"  ) {targetElement.style.display = "none"; }
    else                                          {targetElement.style.display = "block";}
  }
}


/*
 getElementByClass - by Allan C
 theClass    - String of class name in DOM to find
 containerId - (Optional) if present will limit the search to a particular div id
 
 Investigate needed
 YUI has a similar function
 YAHOO.util.Dom.getElementsByClassName
 http://developer.yahoo.com/yui/examples/dom/getelementsbyclassname.html
 does it do what this does? can YUI replace this.
*/
function getElementByClass(theClass,containerId) {
  var elements_found = new Array();                         //Array of elements found to return
  var allHTMLTags;
  var document_section;
  if (containerId === undefined) {document_section = document;}
  else                           {document_section = document.getElementById(containerId);}
  allHTMLTags = document_section.getElementsByTagName("*");
  for (var i=0; i<allHTMLTags.length; i++) {
    var classes = allHTMLTags[i].className.split(" ") //Split the classname by " " to target any multiclass elements
    function checkClass(element, index, array) {      //(sorry probably a better way of doing this win an inline function)
      if (element==theClass) {    //Get all tags with the specified class name.
        elements_found.push(allHTMLTags[i]);
      }
    }
    //classes.forEach(checkClass); //Not compatible it IE
    for (var c in classes) {
        checkClass(classes[c],c,classes);
    }
  }
  return elements_found;
}

function hide_all_hideable(             containerId) {all_hideable('none' ,containerId);}
function show_all_hideable(             containerId) {all_hideable('block',containerId);}
function      all_hideable(display_mode,containerId) {
  var hidden_elements = getElementByClass("hideable",containerId);
  function toggle_element(element, index, array) {
    element.style.display=display_mode;
  }
  //hidden_elements.forEach(toggle_element); //Not compatiable with IE
  for (var h in hidden_elements) {toggle_element(hidden_elements[h],h,hidden_elements);}
}

function hide_all_except(id,containerId) {
  hide_all_hideable(containerId);
  swap(id);
}



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
		if (typeof(last_style_node.addRule) == "object") last_style_node.addRule(selector, declaration);
	}
}



//http://snipplr.com/view/2181/addclass-function/
function addClass(element, value) {
    if(!element.className) {
        element.className = value;
    }
    else {
        newClassName = element.className;
        newClassName+= " ";
        newClassName+= value;
        element.className = newClassName;
    }
}

//http://wolfram.kriesing.de/blog/index.php/2008/javascript-remove-element-from-array
function removeClass(element, value) {
    if(!element.className) {return;}
    var classes = element.className.split(" ");
    var idx = classes.indexOf(value);   // Find the index of the class to remove
    if(idx!=-1) classes.splice(idx, 1); // Remove it if really found!
    element.className = ""
    for (class_name_index in classes) {
        element.className += classes[class_name_index]+" "
    }
    element.className = element.className.trim()
}


/* toggle mini - in planning */
/*
 aim - to add a single on_click function call passing "this" as the only paramiter to get cool section toggling behaviour
 
 control_element = <a href="#" onclick="toggle_mini_inverse">image</a> style: float right, pos absolute, top = - image.height
 this could be customisable but provide a default
 
 function toggle_mini(this_element) {
  get next element
  add after it the new hider control div
  
  hide current element
  show next element
 }
 
 function toggle_mini_inverse() {
  remove added control div
  hide previous elment
  show element previous 2 back (because we added one)
 }
 
*/