//------------------------------------------------------------------------------
// Civicboom Fragment AJAX Mangment
//------------------------------------------------------------------------------

// Example: <a href="http://localhost:5000/test/frag" onclick="cb_frag($(this), 'http://localhost:5000/test/frag'); return false;">Link of AJAX</a>

var fragment_containers_id            = '#frag_containers';
var fragment_container_class          = 'frag_container';
var fragment_div_loading_placeholder = '<p>loading</p>';
var scroll_duration = 1000;

var frag_loading    = null;
var frags_to_remove = null;

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

	// Flag elements after this one for removal
	frags_to_remove = frag_div.nextAll();
	frags_to_remove.remove();
	frags_to_remove = null;
	//frags_to_remove.fadeOut(500);
	//if (frags_to_remove.length > 0) {
	//	Y.log('scroll back frags '+ frags_to_remove.length);
	//	$(fragment_containers_id).scrollTo(frag_div, {duration: scroll_duration});
	//}
	
	// Generate new div name
	var frag_div_id_next = frag_div_id+'1'; // AllanC - I know this only appends one to the end, but it works
	
	// Create new div with loading placeholder
	$(fragment_containers_id).append('<div id="'+frag_div_id_next+'">'+fragment_div_loading_placeholder+'</div>'); // Append new '.frag' div populated with with load placeholder data
	var frag_div_next = $('#'+frag_div_id_next);
	frag_div_next.addClass(fragment_container_class);
	
	frag_loading = frag_div_next;
	$(fragment_containers_id).scrollTo('100%', 0 , {duration: scroll_duration});
	
	// AJAX load html fragment
	frag_div_next.load(url, scroll_fragment_containers_right);
}

function scroll_fragment_containers_right() {	
	// Scroll (smoothly) to the right max
	// http://plugins.jquery.com/project/ScrollTo
	// http://demos.flesler.com/jquery/scrollTo/
	if (frags_to_remove) {
		Y.log('removing frags '+ frags_to_remove.length);
		frags_to_remove.remove();
		frags_to_remove = null;
	}
	if (frag_loading) {
		frag_loading.hide();
		frag_loading.fadeIn(scroll_duration);
		frag_loading = null;
	}
	$(fragment_containers_id).scrollTo('100%', 0 , {duration: scroll_duration});
}