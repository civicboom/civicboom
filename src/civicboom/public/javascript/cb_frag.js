//------------------------------------------------------------------------------
// Civicboom Fragment AJAX Mangment
//------------------------------------------------------------------------------

//-------------
// Variables
//-------------
var fragment_container_id   = '#frag_container';
var fragment_div_loading_placeholder = '';

//----------------------
// Support Functions
//----------------------
function ajax_analytics(url) {
	//trigger Google analitics for this AJAX call
}

function get_next_div_name(div_name) {
	var div_name_next = div_name;
	//TODO: fragment_div_identifier + 1
	// add class .frag
	return div_name_next;
}



function create_frag_div(div_name) {
	// Clear any fragments with this frag name and beyond
	//for n in $(fragment_container_id).children('.frag'):
	//	if (n.id > div_name) {n.remove()}
	
	// Append new '.frag' div
	$(fragment_container_id).append('<div id="'+div_name+'">'+fragment_div_loading_placeholder+'</div>');
	//unneeded as it is included in the line above //$('#'+div_name_next).html(fragment_div_loading_placeholder)
	$('#'+div_name).addClass('frag') //http://api.jquery.com/addClass/
}

function get_parent_frag_id() {
	// go up the chain looking for fragment_div_identifier
	parent_frag = $(this).parents('.frag');
	//alert(parent_frag.id)
	return parent_frag.id;
}

function scroll_right() {
	//http://flesler.blogspot.com/2007/10/jqueryscrollto.html
	//$.scrollTo.max;
}

//---------------------
// Master Call
//---------------------

function cb_frag(url) {
	ajax_analytics(url);
	var div_name      = get_parent_frag_id();
	var div_name_next = get_next_div_name(div_name);
	create_frag_div(div_name_next);
	$('#'+div_name_next).load(url);  //requires Blocking operation?
	scroll_right();
}
