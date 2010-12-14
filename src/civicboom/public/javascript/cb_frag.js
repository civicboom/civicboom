//------------------------------------------------------------------------------
// Civicboom Fragment AJAX Mangment
//------------------------------------------------------------------------------

// Example: <a href="http://localhost:5000/test/frag" onclick="cb_frag($(this), 'http://localhost:5000/test/frag'); return false;">Link of AJAX</a>

var fragment_containers_id            = '#frag_containers';
var fragment_container_class          = 'frag_container';
var fragment_div_loading_placeholder = '<p>loading</p>';


// current_element = JQuery element object
// url             = String
function cb_frag(current_element, url) {
	// Take the url from the current <A> element
	var url_a = current_element.attr('href');
	if (url_a==undefined || url_a==null) {return;}
	if (url  ==undefined || url  ==null) {url = url_a;}
	
	// Register this page view with Google analytics.
	// http://code.google.com/apis/analytics/docs/tracking/asyncMigrationExamples.html#VirtualPageviews
	_gaq.push(['_trackPageview', url_a]);

	// Get this parent fragment name
	var frag_div    = current_element.parents('.'+fragment_container_class) // go up the chain looking for '.frag' class to id the master parent
	var frag_div_id = frag_div.attr('id');

	// Remove all element inserted after this element
	frag_div.nextAll().remove(); 
	
	// Generate new div name
	var frag_div_id_next = frag_div_id+'1'; // AllanC - I know this only appends one to the end, but it works
	
	// Create new div with loading placeholder
	$(fragment_containers_id).append('<div id="'+frag_div_id_next+'">'+fragment_div_loading_placeholder+'</div>'); // Append new '.frag' div populated with with load placeholder data
	var frag_div_next = $('#'+frag_div_id_next);
	frag_div_next.addClass(fragment_container_class);
	
	// AJAX load html fragment
	frag_div_next.load(url, scroll_fragment_containers_right);
}

function scroll_fragment_containers_right() {
	// Scroll (smoothly) to the right max
	// http://plugins.jquery.com/project/ScrollTo
	// http://demos.flesler.com/jquery/scrollTo/
	$(fragment_containers_id).scrollTo('100%', 0 , {duration:400});
}
