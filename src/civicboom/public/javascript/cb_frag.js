//------------------------------------------------------------------------------
// Civicboom Fragment AJAX Mangment
//------------------------------------------------------------------------------

//-------------
// Variables
//-------------
var fragment_container_id   = '#frag_container';
var fragment_div_loading_placeholder = '<p>loading</p>';

//----------------------
// Support Functions
//----------------------
function ajax_analytics(url) {
	//trigger Google analitics for this AJAX call
}

function scroll_right() {
	
	// Scroll (smoothly) to the right max
	// This should be acomplished AFTER the .load operation has completed
	// http://flesler.blogspot.com/2007/10/jqueryscrollto.html
	// $.scrollTo.max;
	Y.log('scrolling right', "info",  "cb_frag");
}


//---------------------
// Master Call
//---------------------

// current_element = JQuery element object
// url             = String
function cb_frag(current_element ,url) {
	function l(msg) {Y.log(msg, "info",  "cb_frag");}
	// Register this page view with Google analytics.
	ajax_analytics(url);
	
	// Get this parent fragment name
	var frag_div    = current_element.parents('.frag') // go up the chain looking for '.frag' class to id the master parent
	var frag_div_id = frag_div.attr('id');

	// Remove all element inserted after this element
	frag_div.nextAll().remove(); 
	
	// Generate new div name
	var frag_div_id_next = frag_div_id+'1'; // AllanC - I know this only appends one to the end, but it works
	
	// Create new div with loading placeholder
	$(fragment_container_id).append('<div id="'+frag_div_id_next+'">'+fragment_div_loading_placeholder+'</div>'); // Append new '.frag' div populated with with load placeholder data
	var frag_div_next = $('#'+frag_div_id_next);
	frag_div_next.addClass('frag');
	
	// AJAX load html fragment
	frag_div_next.load(url, scroll_right);
}