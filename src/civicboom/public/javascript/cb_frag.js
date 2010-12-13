//------------------------------------------------------------------------------
// Civicboom Fragment AJAX Mangment
//------------------------------------------------------------------------------

//-------------
// Variables
//-------------
var fragment_div_identifier = "frag_";
var fragment_div_loading_placeholder = "";

//----------------------
// Support Functions
//----------------------
function ajax_analytics(url) {
	//trigger Google analitics for this AJAX call
}

function get_next_div_name(div_name) {
	var div_name_next = div_name;
	//TODO: fragment_div_identifier + 1
	return div_name_next;
}

function create_frag_div(div_name) {
	var div_name_next = get_next_div_name(div_name);
	clear_frag_div_from(div_name_next);
}

function get_parent_frag_id() {
	// go up the chain looking for fragment_div_identifier
	child = self;
	while (child.parent != null) {
		child = child.parent;
		if (fragment_div_identifier in child.id) {
			return child.id;
		}
	}
	return null;
}

function scroll_right() {
	//http://flesler.blogspot.com/2007/10/jqueryscrollto.html
	$.scrollTo.max;
}

//---------------------
// Master Call
//---------------------

function cb_frag(url) {
	ajax_analytics(url);
	var div_name      = get_parent_frag_id();
	var div_name_next = get_next_div_name(div_name);
	create_frag_div(div_name_next);
	div_name_next.fill(fragment_div_loading_placeholder)
	div_name_next.load(url); //requires Blocking operation
	scroll_right();
}
