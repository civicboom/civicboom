// Misc Functions

// Requires toggle_div.js functions
// MARKED FOR DEPRICATION
/*
function setSingleCSSClass(element_to_style, class_to_set, parent_id) {
    try {
        // Find all occurances of this class
        var elements = getElementByClass(class_to_set, parent_id);
        for (var element in elements) {
            // Remove the class
            removeClass(elements[element], class_to_set);
        }
        // Add the class to the specifyed element
        addClass(element_to_style, class_to_set);
    }
    catch(err) {
        Y.log("setSingleCSS failed", "warn", "misc")
    }
}
*/

function flash_message(json_message) {
	if (typeof(json_message) == "string") {json_message = {status:'ok', message:json_message};}
	if (json_message && json_message.message != "") {
		$("#flash_message").removeClass("status_error").removeClass("status_ok").addClass("status_"+json_message.status);
		$("#flash_message").text(json_message.message).fadeIn("slow").delay(5000).fadeOut("slow");
	}
}

function popup(title, url) {	
	// AllanC - TODO: need some indication to the user that this AJAX request is happening
	$('#popup .title_text'   ).html(title);
	$('#popup .popup_content').load(url,function(){
		$('#popup').modal({ onShow: function (dialog) {
		  var smc = $('.simplemodal-container');
		  var smd = $('.popup-content');
		  smc.css('width', smd.outerWidth(true));
		  smc.css('height', smd.outerHeight(true));
		}});
	});

	// AllanC - loading feedback could be:
	//           displaying the popup
	//			 adding a loading placeholder
	//           investigate jsmodal.js and find call to re-init the size and position of the window when JS load complete
	/*
	{
	onShow: function (dialog) {
		$(".popup_content", dialog.data).load(url, function(){
			Y.log('loaded: '+url);
		});
	}
	}
	*/
}

// submit buttons triggered by onclick dont submit the submit buttons name or value in the form
// we can fake that here by using jQuery to temporerally create these as hidden form fields
// Example:
//   <input type="submit" name="submit_draft"   value="Save Draft" onclick="add_onclick_submit_field($(this));" />
//   will add the field as <input type="hidden"/>
function add_onclick_submit_field(current_element) {
	$('.fake_submit').remove(); //remove all fake fields inserted by previous submits
	var field_name  = current_element.attr('name');
	var field_value = current_element.attr('value');
	current_element.closest('form').append('<input type="hidden" name="'+field_name+'" value="'+field_value+'" class="fake_submit"/>');
}



// http://bonta-kun.net/wp/2007/07/05/javascript-typeof-with-array-support/
function typeOf(obj) {
	if ( typeof(obj) == 'object' ) {
		if (obj.length) {return 'array';}
		else            {return 'object';}
	}
	else {
		return typeof(obj);
	}
}
// Other solutions could include
// http://joncom.be/code/realtypeof/
// http://snipplr.com/view/1996/typeof--a-more-specific-typeof/
// jQuery does not appear to have a nice base call for this





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

var media_thumbnail_timers = {};
var media_jquery_objects = {};

function updateMedia(id, hash, jquery_element) {
  if (typeof media_jquery_objects[id] == 'undefined')
  {
    media_jquery_objects[id] = jquery_element;
  } else {
    jquery_element = media_jquery_objects[id];
  }
  if (typeof media_thumbnail_timers[id] == 'undefined')
    media_thumbnail_timers[id] = setInterval ('updateMedia('+id+',\''+hash+'\')', 1000);
  $.getJSON(
    '/media/' + hash + '.json',
    processingStatus
  );
  function processingStatus(data) {
    _status = data.data.status;
    if(!_status) {
      Y.log ('uM got thumb');
      _thumbnail = data.data.thumbnail_url
      clearInterval(media_thumbnail_timers[id]);
      // delete media_thumbnail_timers[id]; FIXME: uncomment this line before go-live!
      jquery_element.find('img').attr('src', _thumbnail + "?" + (new Date().getTime()));
      jquery_element.find('span').text('').css('display', 'none'); 
    }
    else {
      jquery_element.find('span').css('display', 'inline').text(_status);
    }
  }
}

function appendAttr(element, name, append) {
  if (element.length == 0) return;
  if (element.attr(name)) element.attr(name, element.attr(name) + '_' + append);
}

function setAttrIf(element, name, val) {
  if (element.length == 0) return;
  if (element.attr(name)) element.attr(name, val);
}

function refreshProgress (jquery_element) {
  var url = jquery_element.parents('.'+fragment_container_class).children('.'+fragment_source_class).attr('href').replace(/\.frag$/, '.json');
  $.getJSON( url, function (data) {
    if (typeof data.data.content.attachments != 'undefined') {
      var attachments = data.data.content.attachments
      Y.log (attachments.length);
      for (var i = 0; i < attachments.length; i ++) {
        var attachment = attachments[i];
        Y.log ('#media_attachment_' + attachment.id + ' :' + $('#media_attachment_' + attachment.id).length);
        if ($('#media_attachment_' + attachment.id).length == 0) {
          Y.log ('I found a new attachment!');
          var at_element = jquery_element.find('#mediatemplate').clone(true, true).attr('id', 'media_attachment_' + attachment.id).css('display','');
          jquery_element.find('ul.media_files').children('li.media_file').last().after(at_element);
          at_element.find('#media_file').attr('value', attachment.name);
          at_element.find('#media_caption').attr('value', attachment.caption);
          at_element.find('#media_credit').attr('value', attachment.credit);
          at_element.find('*').each(function (index, element) {
            element = $(element);
            appendAttr(element, 'id', attachment.id);
            appendAttr(element, 'for', attachment.id);
            appendAttr(element, 'name', attachment.id);
          });
          updateMedia(attachment.id, attachment.hash, at_element);
        }
      }
    }
  });
}