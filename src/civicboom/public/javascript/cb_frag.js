//------------------------------------------------------------------------------
// Civicboom Fragment AJAX Mangment
//------------------------------------------------------------------------------

// Example: <a href="http://localhost:5000/test/frag" onclick="cb_frag($(this), 'http://localhost:5000/test/frag'); return false;">Link of AJAX</a>

var frag_id_name                      = 'frag_';
var fragment_containers_id            = '#frag_containers';
var fragment_container_class          = 'frag_container';
var fragment_div_loading_placeholder = '<p>loading</p>';
var scroll_duration = 1000;

var frag_count      = 0;
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
	frags_to_remove.remove(); frags_to_remove = null;
	// AllanC - we want to keep the old elements taking there space for a while to allow the client browser to scroll to the correct position then remove the unneeded elements
	//frags_to_remove.animate({width: 'toggle', opacity: 'toggle'}, 500, function(){frags_to_remove.remove(); frags_to_remove = null;});
	//frags_to_remove.fadeOut(scroll_duration/2, function(){frags_to_remove.remove(); frags_to_remove = null;});
	
	// Generate new div name
	var frag_div_id_next = frag_id_name + frag_count++; //frag_div_id+'1'; // AllanC - I know this only appends one to the end, but it works
	
	// Create new div with loading placeholder
	frag_div.after('<div id="'+frag_div_id_next+'" class="'+fragment_container_class+'">'+fragment_div_loading_placeholder+'</div>'); // Append new '.frag' div populated with with load placeholder data //$(fragment_containers_id).append 
	frag_loading = $('#'+frag_div_id_next);
	
	// Start scrolling to new element
	// Scroll (smoothly)
	//  - http://plugins.jquery.com/project/ScrollTo
	//  - http://demos.flesler.com/jquery/scrollTo/
	$(fragment_containers_id).scrollTo(frag_loading, {duration: scroll_duration});
	
	// AJAX load html fragment
	frag_loading.load(url,
		function(){ // When AJAX load complete
			// Fade in loaded segment
			if (frag_loading) {
				frag_loading.hide();
				//frag_loading.width(0);
				//frag_loading.animate({width: 'toggle', opacity: 'toggle'}, scroll_duration);
				frag_loading.fadeIn(scroll_duration);
				frag_loading = null;
				//$(fragment_containers_id).scrollTo('100%', 0 , {duration: scroll_duration});
			}
	});
}
