//------------------------------------------------------------------------------
// Civicboom Fragment AJAX Mangment
//------------------------------------------------------------------------------

// Example: <a href="http://localhost:5000/test/frag" onclick="cb_frag($(this), 'http://localhost:5000/test/frag'); return false;">Link of AJAX</a>

var frag_id_name                      = 'frag_';
var fragment_containers_id            = '#frag_containers';
var fragment_container_class          = 'frag_container';  // container for a full JSON object 500px
//var fragment_col_class                = 'frag_col_1';      // container for a bridge list 250px (half width)
var fragment_source_class             = 'frag_source';
var fragment_div_loading_placeholder  = '<div class="title_bar gradient">Loading...</div>'+
                                        '<div class="action_bar"></div>'+
                                        '<p class="loading_placeholder">loading</p>';
var fragment_help_class               = 'frag_help';
var scroll_duration = 600;

var frag_count      = 0;
var frag_loading    = null;
var frags_to_remove = null;

//------------------------------------------------------------------------------
//                               Create Frag
//------------------------------------------------------------------------------

// current_element = JQuery element object
// url             = String
function cb_frag(current_element, url, list_type, from_history, callback) {
	// Take the url from the current <A> element (hence the name url_a)
	var url_a = current_element.attr('href');
	
	if (url  ==undefined || url  ==null) {url = url_a;}
	if (url  ==undefined || url  ==null) {return;}
	
	// Set the class for this new fragment (bridge list or full container)
	var new_fragment_class = fragment_container_class;
	if (typeof list_type == 'string') {new_fragment_class += ' '+list_type}
	//if (list_type=='frag_col_1') {new_fragment_class += " "+fragment_col_class;}
	//else                         {}
	
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
	
	function frag_update_history() {
  	// Call update history with fragment URL
  	if (! from_history) update_history();
  }

	// AJAX load html fragment
	frag_loading.load(url,
		function(response, status, request){ // When AJAX load complete
		  var frag_loading = $(this);
		    if (request.status != 200) {
		    	frag_loading.remove();
		    	if (typeof callback != 'undefined') callback(false);
		    }
		    if (frag_loading) {
  				frag_loading.fadeTo(0, 0.01); // Set opacity to 0.01 with a delay of 0, this could be replaced with a setOpacity call? I think this is creating animtion headaches
  				//frag_loading.width(0); // animating width buggers up scrolling
  				//frag_loading.animate({width: '500px', opacity: 1.0}, scroll_duration);
  				frag_loading.animate({opacity: 1.0}, scroll_duration);
  				//frag_loading.fadeIn(scroll_duration);
  				//frag_loading.toggle(scroll_duration);
  				
  				if (! from_history) cb_frag_remove_sibblings(frag_loading, frag_update_history);
  
  				// remove the "opacity" setting, as IE doesn't antialias filtered stuff
  				frag_loading.animate({opacity: null}, 0);
  				
  				frag_loading = null;
  				if (typeof callback != 'undefined') callback(true);
  				// These are unneeded because the playholder is the correct width, so the scroll above will be scrolling to the correct place as the AJAX loads
  				//$(window)._scrollable().scrollTo(frag_loading, {duration: scroll_duration});
  				//$(window)._scrollable().scrollTo('100%',0, {duration: scroll_duration});
  				//$.scrollTo(frag_loading, {duration: scroll_duration}); //(fragment_containers_id)
  				//$(fragment_containers_id).scrollTo('100%', 0 , {duration: scroll_duration});	
  			 }
  		}
  	);
  return frag_loading;
}

//------------------------------------------------------------------------------
//                               Load Frag
//------------------------------------------------------------------------------


function cb_frag_load(jquery_element, url) {
	// Register this page view with Google analytics. - see cb_frag() for more info
	// AllanC - this is not ideal as it will have the.frag and not record the actual pageview ... but it's better than nothing for now
	_gaq.push(['_trackPageview', url]);
	
	var frag_container = jquery_element.parents('.'+fragment_container_class)
	frag_container.load(url);
}


//------------------------------------------------------------------------------
//                               Remove Frag
//------------------------------------------------------------------------------

function cb_frag_remove(jquery_element, callback, from_history) {
	var parent = jquery_element.parents('.'+fragment_container_class); // find parent
  if (typeof cb_frag_get_variable(jquery_element, 'autosavedrafttimer') != 'undefined')
    clearInterval(cb_frag_get_variable(jquery_element, 'autoSaveDraftTimer'));
	parent.toggle(scroll_duration, function(){
		parent.remove();
		// If no fragments on screen redirect to default page
		if ($('.'+fragment_container_class).length == 0) {
			window.location.replace("/profile");
		}
		if (typeof callback != 'undefined') callback();
		if (! from_history) update_history( $('.'+fragment_container_class).not('.'+fragment_help_class).last().find('.'+fragment_source_class).first().attr('href') );
	});
	cb_frag_remove_sibblings(parent);
	
	$.modal.close(); // Aditionaly, if this is in a popup then close the popup
}

function cb_frag_remove_sibblings(jquery_element, callback, ignorehelp) {
  var parent_siblings;
  if (ignorehelp) {
    parent_siblings = jquery_element.nextAll('.'+fragment_container_class+':not(.'+fragment_help_class+')');
  } else {
    parent_siblings = jquery_element.nextAll();
  }
	parent_siblings.toggle(scroll_duration, function()
	  {
	    parent_siblings.remove();
	    if (typeof callback != 'undefined') callback();
	    callback = undefined;
	  });
	if (parent_siblings.length == 0 && typeof callback != 'undefined') callback();
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
		// Remove auto-save timer if refreshing fragment! GM
    if (typeof cb_frag_get_variable(jquery_element, 'autosavedrafttimer') != 'undefined')
      clearInterval(cb_frag_get_variable(jquery_element, 'autoSaveDraftTimer'));
		frag_element.load(frag_source);
	}

	function reload_frags_containing(array_of_urls) {
		// Look through all <A> tags in every frgament for the string
		// if the link contains this string
		// add the <A>'s parent frag to a refresh list (preventing duplicates)
		// go through the frag list refreshing
		
		var frags_to_refresh = {};
		$(fragment_containers_id+' a').each(function(index) {
			var link_element = $(this);
			for (var url_part in array_of_urls) {
				url_part = array_of_urls[url_part];
				link_element_href = link_element.attr('href');
				if (link_element_href!=undefined && link_element_href.indexOf(url_part) != -1) {
					var elem_source_pair = get_parent_container_element_source(link_element);
					var frag_element = elem_source_pair[0];
					var frag_source  = elem_source_pair[1];
					// Remove auto-save timer if refreshing fragment! GM
          if (typeof cb_frag_get_variable(link_element, 'autosavedrafttimer') != 'undefined')
            clearInterval(cb_frag_get_variable(link_element, 'autoSaveDraftTimer'));
					frags_to_refresh[frag_source] = frag_element;
				}
			}
		});
		// Go though all frags found reloading them
		for (var key in frags_to_refresh) {
		  var title = frags_to_refresh[key].find('.title_text').first();
		  title.html(title.html() + ' <img src="/images/ajax-loader.gif" />');
			frags_to_refresh[key].load(key);
		}
	}

	if      (typeof param == 'string') {reload_frags_containing([param]);}
	else if (typeOf(param) == 'array') {reload_frags_containing( param );}
	else                               {reload_element(param);}

}

function cb_frag_set_source(jquery_element, url) {
	jquery_element.parents('.'+fragment_container_class).children('.'+fragment_source_class).attr('href', url);
}

function cb_frag_get_source(jquery_element) {
  jquery_element.parents('.'+fragment_container_class).children('.'+fragment_source_class).attr('href');
}

function cb_frag_set_variable(jquery_element, variable, value) {
  var valueClean = (typeof value == 'undefined')?(''):(value);
  jquery_element.parents('.'+fragment_container_class).children('.'+fragment_source_class).attr('cb'+variable, valueClean);
}

function cb_frag_get_variable(jquery_element, variable) {
  return jquery_element.parents('.'+fragment_container_class).children('.'+fragment_source_class).attr('cb'+variable);
}

//------------------------------------------------------------------------------
//                            Browser URL updating
//------------------------------------------------------------------------------

function createStateObj() {
  var stateObj = { 'blocks': []};
  $('.'+fragment_container_class).not('.'+fragment_help_class).each (function (index, element)
    {
      var s_url = $(element).find('.'+fragment_source_class).first().attr('href');
      stateObj.blocks[index] = {'url'  : s_url,
                                'classes': $(element).attr('class')
                               };
    });
  return stateObj;
}

function loadStateObj(stateObj) {
  var frag_previous;
  if(stateObj !== null) {
    if (typeof stateObj.blocks == 'undefined') return;
    
    var i = 0;
    
    function load() {
      if (i < stateObj.blocks.length) {
        var frag_source = frag_previous.find('.'+fragment_source_class).first();
        var stat_href = stateObj.blocks[i].url;
        frag_previous = cb_frag(frag_source, stat_href, undefined, true, load); //$($('.'+fragment_container_class)[i-1]).find('.'+fragment_source_class)
        i ++;
      } else {
        cb_frag_remove_sibblings($($('.'+fragment_container_class)[stateObj.blocks.length-1]), undefined, true);
        return;
      }
    }

    for (i = 0; i < stateObj.blocks.length; i++) {
      var frag_exists = typeof $('.'+fragment_container_class)[i] != 'undefined';
      var frag_container = $($('.'+fragment_container_class)[i]);
      var frag_source = frag_container.find('.'+fragment_source_class);
      var frag_href = frag_source.attr('href');
      var stat_href = stateObj.blocks[i].url;
      if (!frag_exists) {
        load ();
        //frag_container = cb_frag(frag_previous.find('.'+fragment_source_class).first(), stat_href, undefined, true, waiter); //$($('.'+fragment_container_class)[i-1]).find('.'+fragment_source_class)
        break;
      } else if (frag_href != stat_href) {
        frag_container.attr('class', stateObj.blocks[i].classes);
        frag_container.find('.'+fragment_source_class).first().attr('href', stat_href);
        cb_frag_reload (frag_container);
      }
      frag_previous = frag_container;
    }
    if (i = (stateObj.blocks.length - 1))
      cb_frag_remove_sibblings($($('.'+fragment_container_class)[stateObj.blocks.length-1]), undefined, true);
  }
}

function update_history(url, replace) {
  if (typeof url == 'undefined')
    var url = $('.'+fragment_container_class).not('.'+fragment_help_class).last().find('.'+fragment_source_class).first().attr('href');
  // update the URL bar to point at the latest block, and
  // store previous blocks in the history state object
  if(Modernizr.history) {
    // Note: this object is limited to 640k (which ought to be
    // enough for anyone) when saved in the browser history file
    if (replace) {
      history.replaceState(createStateObj());
    } else {
      history.pushState(createStateObj(), "Civicboom", url.replace("?format=frag", "").replace(".frag", ""));
    }
  } else {
    if (replace) {
      if (location.hash.substr(1,3) != 'cbh') {
        location.replace('#cbh' + encode64($.JSON.encode(createStateObj())));
      } else {
        $(window).hashchange();
      }
    } else {
      location.hash = '#cbh' + encode64($.JSON.encode(createStateObj()));
    }
  }
}

$(function () {
  if(Modernizr.history) {
    // Browser supports HTML5 history states
    // FIXME: jQuery-ise this, rather than using the raw window.blah
    window.onpopstate = function(popstate) { loadStateObj(popstate.state); }
    } else if(Modernizr.hashchange) {
    // Browser does not support HTML5 history states
    // Use url hash instead
    // GregM: Causing stability issues in IE, removed for now
    // $(window).hashchange(function (e) {
    //   var hash = location.hash;
    //   if (hash != '' && typeof hash != 'undefined') {
    //     if (hash.substr(1,3) == 'cbh') {
    //       try {
    //         var stateObj = $.parseJSON(decode64(hash.substr(4)));
    //         loadStateObj(stateObj);
    //       } catch (e) {} 
    //     }
    //   }
    // });
  }
  update_history(location.href, true);
})
