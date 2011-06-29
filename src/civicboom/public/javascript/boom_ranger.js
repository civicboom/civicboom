if (typeof window.boom == 'undefined') {
	// Civicboom stays in the boom object
	window.boom = {
		// Base host to load content from
		base_host: 'https://www.civicboom.com',
		// Callback id counter
		counter: 0,
		// Find elements by class name :)
		getElementsByClassName: function (node,classname) {
			if (node.getElementsByClassName) { // use native implementation if available
				return node.getElementsByClassName(classname);
			} else {
				return (function getElementsByClass(searchClass,node) {
					if ( node == null )
						node = document;
					var classElements = [],
					els = node.getElementsByTagName("*"),
					elsLen = els.length,
					pattern = new RegExp("(^|\\s)"+searchClass+"(\\s|$)"), i, j;
					for (i = 0, j = 0; i < elsLen; i++) {
						if ( pattern.test(els[i].className) ) {
							classElements[j] = els[i];
							j++;
						}
					}
					return classElements;
				})(classname, node);
			}
		},
		// Default plugins for the Boom Ranger!
		plugins: {
			// Default error plugin, more plugins defined below.
			error:
				function (counter, type, div) {
					div.innerHTML = 'Apologies, it seems an error has occured loading this content...';
				}
		},
		// The Boom Ranger! Find divs to transform into content items & run the associated plugin.
		ranger: function () {
			var arr = window.boom.getElementsByClassName(document, "civicboom-ranger");
			for (var i = 0; i < arr.length; i++) {
				var counter   = window.boom.counter * 1;
				var container = arr[i];
				var div       = arr[i].getElementsByTagName("div")[0];
				if (div.getAttribute('boom:status') == 'loaded')
					continue;
				var type      = container.getAttribute('boom:type');
				var type_call = type;
				if (typeof window.boom.plugins[type] == 'undefined') {
					type_call = 'error';
				}
				window.boom.plugins[type_call](counter, type, div, container);
				window.boom.counter += 1;
			}
		}
	}
}
// Plugins:
// Load plugins using attribute boom:type="plugin-name"
//
// Content Plugin:
// Plugin to load and format content. Takes arguments:
//		boom:id  		- the id of the content
//		boom:img		- the height of the image to be displayed - if not included does not show image, if 0 shows image full size
//		boom:responses	- the number of responses to display - if not included does not show responses & count, if 0 shows count only
if (typeof window.boom.plugins.content == 'undefined')
	window.boom.plugins.content = 
		function (counter, type, div, container) {
			var id        = container.getAttribute('boom:id');
	    	var img       = container.getAttribute('boom:img');
	    	var responses = container.getAttribute('boom:responses');
	    	var host      = container.getAttribute('boom:host');
	    	if (host == null) host = window.boom.base_host;
	        window['boom_callback_'+window.boom.counter] = function (data) {
	            div.innerHTML = '';
	            if (img !== null)
	                div.innerHTML += '<img style="float:left;" '+(img>0?'height="'+img+'"':'')+' src="'+data.data.content.thumbnail_url+'" />'
	            //div.innerHTML += '<div>';
	            div.innerHTML += '<h3>'+data.data.content.title+'</h3>';
	            div.innerHTML += '<p class="content">'+data.data.content.content+'</p>';
	            if (responses !== null && (data.data.content.num_responses * 1) > 0) {
	                num_responses = data.data.content.num_responses * 1;
	                responses = responses * 1;
	                div.innerHTML += '<p class="responses">'+num_responses+' response'+(num_responses>1?'s':'')+'<br />';
	                if (responses > data.data.content.num_responses)
	                    responses = num_responses;
	                if (responses > data.data.responses.limit*1)
	                    responses = data.data.responses.limit*1;
	                if (responses > 0) {
	                    div.innerHTML += '<ul>';
	                    for (j = 0; j < responses; j++) {
	                        response = data.data.responses.items[j];
	                        div.innerHTML += '<li><a href="'+host+'/contents/'+response.id+'">By '+response.creator.name+'</a></li>';
	                    }
	                    div.innerHTML += '</ul>';
	                }
	                div.innerHTML += '</p>';
	            }
	            div.setAttribute('boom:status', 'loaded');
	            delete window['boom_callback_'+counter];
	        }
	        document.write('<script src="'+host+'/contents/'+id+'.json?callback=boom_callback_'+window.boom.counter+'" type="text/javascript">\<\/script>');
		}
// Finally... run the Boom Ranger!
window.boom.ranger();