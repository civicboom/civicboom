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
		$('#popup').modal();
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
