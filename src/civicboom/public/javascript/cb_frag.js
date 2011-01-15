//------------------------------------------------------------------------------
// Civicboom Fragment AJAX Mangment
//------------------------------------------------------------------------------

// Example: <a href="http://localhost:5000/test/frag" onclick="cb_frag($(this), 'http://localhost:5000/test/frag'); return false;">Link of AJAX</a>

var frag_id_name                      = 'frag_';
var fragment_containers_id            = '#frag_containers';
var fragment_container_class          = 'frag_container';  // container for a full JSON object 500px
var fragment_bridge_class             = 'frag_bridge';     // container for a bridge list 250px (half width)
var fragment_source_class             = 'frag_source';
var fragment_div_loading_placeholder  = '<div class="title_bar gradient">Loading...</div>'+
                                        '<div class="action_bar"></div>'+
                                        '<p class="loading_placeholder">loading</p>';
var scroll_duration = 600;

var frag_count      = 0;
var frag_loading    = null;
var frags_to_remove = null;

//------------------------------------------------------------------------------
//                               Create Frag
//------------------------------------------------------------------------------

// current_element = JQuery element object
// url             = String
function cb_frag(current_element, url, list_type) {
	// Take the url from the current <A> element (hence the name url_a)
	var url_a = current_element.attr('href');
	
	if (url  ==undefined || url  ==null) {url = url_a;}
	if (url  ==undefined || url  ==null) {return;}
	
	// Set the class for this new fragment (bridge list or full container)
	var new_fragment_class = fragment_container_class;
	if (list_type=='bridge') {new_fragment_class += " "+fragment_bridge_class;}
	
	// Register this page view with Google analytics.
	// http://code.google.com/apis/analytics/docs/tracking/asyncMigrationExamples.html#VirtualPageviews
	_gaq.push(['_trackPageview', url_a]);

	// Get this parent fragment name
	var frag_div    = current_element.parents('.'+fragment_container_class) // go up the chain looking for '.frag' class to id the master parent
	var frag_div_id = frag_div.attr('id');
	
	// Generate new div name
	var frag_div_id_next = frag_id_name + frag_count++; //frag_div_id+'1'; // AllanC - I know this only appends one to the end, but it works
	
	// Create new div with loading placeholder
	frag_div.after('<div id="'+frag_div_id_next+'" class="'+new_fragment_class+'">'+fragment_div_loading_placeholder+'</div>'); // Append new '.frag' div populated with with load placeholder data //$(fragment_containers_id).append 
	frag_loading = $('#'+frag_div_id_next);
	
	// Start scrolling to new element
	// Scroll (smoothly)
	//  - http://plugins.jquery.com/project/ScrollTo
	//  - http://demos.flesler.com/jquery/scrollTo/
	$(window)._scrollable().scrollTo(frag_loading, {duration: scroll_duration}); //(fragment_containers_id)
	//$(window)._scrollable().scrollTo('100%',0, {duration: scroll_duration});
	//$(fragment_containers_id).scrollTo('100%', 0 , {duration: scroll_duration});
	
	// update the URL bar to point at the latest block, and
	// store previous blocks in the history state object
	if(Modernizr.history && false) {
		// FIXME: save the actual state of the app; this is just an
		// example of how I imagine it would work, with a list of
		// currently loaded blocks and their states.
		// Note: this object is limited to 640k (which ought to be
		// enough for anyone) when saved in the browser history file
		var stateObj = {
			blocks: [
				{ url: "/contents/1", scrollpos: 50 },
				{ url: "/members/2", blockmode: "pie" },
				{ url: "/members/2/followers" }
			]
		};
		history.pushState(stateObj, "Civicboom", url.replace("?format=frag", "").replace(".frag", ""));
	}

	// AJAX load html fragment
	frag_loading.load(url,
		function(){ // When AJAX load complete
			if (frag_loading) {
				frag_loading.fadeTo(0, 0.01); // Set opacity to 0.01 with a delay of 0, this could be replaced with a setOpacity call? I think this is creating animtion headaches
				//frag_loading.width(0); // animating width buggers up scrolling
				//frag_loading.animate({width: '500px', opacity: 1.0}, scroll_duration);
				frag_loading.animate({opacity: 1.0}, scroll_duration);
				//frag_loading.fadeIn(scroll_duration);
				//frag_loading.toggle(scroll_duration);
				
				cb_frag_remove_sibblings(frag_loading);

				// remove the "opacity" setting, as IE doesn't antialias filtered stuff
				frag_loading.animate({opacity: null}, 0);
				
				frag_loading = null;
				
				// These are unneeded because the playholder is the correct width, so the scroll above will be scrolling to the correct place as the AJAX loads
				//$(window)._scrollable().scrollTo(frag_loading, {duration: scroll_duration});
				//$(window)._scrollable().scrollTo('100%',0, {duration: scroll_duration});
				//$.scrollTo(frag_loading, {duration: scroll_duration}); //(fragment_containers_id)
				//$(fragment_containers_id).scrollTo('100%', 0 , {duration: scroll_duration});	
			}
		}
	);
}

//------------------------------------------------------------------------------
//                               Load Frag
//------------------------------------------------------------------------------


function cb_frag_load(jquery_element, url) {
	var frag_container = jquery_element.parents('.'+fragment_container_class)
	frag_container.load(url);
}


//------------------------------------------------------------------------------
//                               Remove Frag
//------------------------------------------------------------------------------

function cb_frag_remove(jquery_element) {
	var parent = jquery_element.parents('.'+fragment_container_class); // find parent
	parent.toggle(scroll_duration, function(){
		parent.remove();
		// If no fragments on screen redirect to default page
		if ($('.'+fragment_container_class).length == 0) {
			window.location.replace("/profile/index");
		}
	});
	cb_frag_remove_sibblings(parent);
	
	$.modal.close(); // Aditionaly, if this is in a popup then close the popup
}

function cb_frag_remove_sibblings(jquery_element) {
	var parent_siblings = jquery_element.nextAll();
	parent_siblings.toggle(scroll_duration, function(){parent_siblings.remove()});
}

//------------------------------------------------------------------------------
//                               Reload Frag
//------------------------------------------------------------------------------

function cb_frag_reload(param) {
	// Can be passed a JQuery object or a String
	//  JQuery - find frag_container parent - find hidden source link for that frag - reload
	//  String - find hidden source link for all frags - dose source href contain param - reload
	
	function get_parent_container_element_source(jquery_element) {
		var container_element   = jquery_element.parents('.'+fragment_container_class);
		var frag_source_element = container_element.children('.'+fragment_source_class);
		var frag_source_href    = frag_source_element.attr('href');
		return [container_element, frag_source_href];
	}
	
	// Move up the chain from this element
	//   grab the href of the A frag_source
	//   and use that the .load the parent_frag container
	function reload_element(jquery_element) {
		var elem_source_pair = get_parent_container_element_source(jquery_element);
		var frag_element = elem_source_pair[0];
		var frag_source  = elem_source_pair[1];
		frag_element.load(frag_source);
	}

	if (typeof param == 'string') {
		// Look through all <A> tags in every frgament for the string
		// if the link contains this string
		// add the <A>'s parent frag to a refresh list (preventing duplicates)
		// go through the frag list refreshing
		
		var frags_to_refresh = {};
		$(fragment_containers_id+' a').each(function(index) {
			var link_element = $(this);
			if (link_element.attr('href').indexOf(param) != -1) {
				var elem_source_pair = get_parent_container_element_source(link_element);
				var frag_element = elem_source_pair[0];
				var frag_source  = elem_source_pair[1];
				frags_to_refresh[frag_source] = frag_element;
			}
		});
		for (var key in frags_to_refresh) {
			frags_to_refresh[key].load(key);
		}
		
		/*
		$(fragment_containers_id).children('.'+fragment_container_class).children('.'+fragment_source_class).each(function(index){
			if ($(this).attr('href').indexOf(param) != -1) {
				cb_frag_reload($(this));
			}
		});
		*/
	}
	else {
		reload_element(param);
	}

}

function cb_frag_set_source(jquery_element, url) {
	jquery_element.parents('.'+fragment_container_class).children('.'+fragment_source_class).attr('href', url);
}

//------------------------------------------------------------------------------
//                            Browser URL updating
//------------------------------------------------------------------------------

if(Modernizr.history && false) {
	// FIXME: jQuery-ise this, rather than using the raw window.blah
	window.onpopstate = function(popstate) {
		if(popstate.state) {
			// go through $state, make sure that each block in
			// the current page matches $state['blocks'][n]['url']
		}
	}
}
