$(document).ajaxError(function(event, request, settings, exception) {
	try {
		jsob = jQuery.parseJSON(request.responseText);
	} catch (e) {
		if (request.status == 404) {
			flash_message('The page you requested could not be found, it may have been removed or hidden.');
		} else {
			flash_message('A server error has occurred!');
		}
	}
	
	if (typeof jsob != 'undefined') {
		if (typeof jsob.message != 'undefined' && typeof jsob.data != 'undefined' && typeof jsob.data.invalid != 'undefined') {
			window.console.log('!');
			jsob.message = jsob.message + ' (';
			for (var i in jsob.data.invalid) {
				jsob.message = jsob.message + i + ': ' + jsob.data.invalid[i] + ', ';
			}
			jsob.message = jsob.message + ')';
		}
		window.console.log (jsob);
		flash_message(jsob);
	}
	
	try {
		//flash_message(jQuery.parseJSON(request.responseText));
	} catch (e) {
		if (request.status == 404) {
			flash_message('The page you requested could not be found, it may have been removed or hidden.');
		} else {
			flash_message('A server error has occurred!');
		}
	}

	// GregM: Upgrade Required
	if (request.status == 402) {
		popup('Upgrade plans', '/misc/upgrade_plans.frag');
	}

    /**
    // AllanC: Depricated - no longer requires client site cookies to perform remebered operations - however, requires upgrade to jQuery 1.5.0
	// GregM: Login Required
	if (request.status == 403) {
		// settings.url has the last ajax settings including url :D
		$.cookie('login_redirect', 'https://' + document.location.hostname + settings.url.replace(/json$/, 'redirect'), { expires: new Date((new Date()).getTime() + 5*60000), path: '/' });
		// Need to set this to stop "Hold It!" message...
		var login_redirect_action = '{}';
		if (settings.type == 'POST') {
			login_redirect_action = "{'" + settings.data.replace("&", "','").replace("=", "':'") + "'}";
		}
		$.cookie('login_redirect_action', login_redirect_action, { expires: new Date((new Date()).getTime() + 5*60000), path: '/' });
		//$.cookie('login_action_referer', 
		// Redirect User
		window.location.href = '/account/signin';
	}
    */
});
