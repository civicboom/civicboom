// $(document).ajaxError(function(event, request, settings, exception) {
	// try {
		// jsob = jQuery.parseJSON(request.responseText);
	// } catch (e) {
		// if (request.status == 404) {
			// flash_message({message: 'The page you requested could not be found, it may have been removed or hidden.', status: 'error'});
		// } else {
			// flash_message({message: 'A server error has occurred!'                                                  , status: 'error'});
		// }
        // console.log(request.status);
        // console.log(exception);
	// }
// 	
	// if (typeof jsob != 'undefined') {
		// if (typeof jsob.message != 'undefined' && typeof jsob.data != 'undefined' && typeof jsob.data.invalid != 'undefined') {
			// jsob.message = jsob.message + ' (';
			// for (var i in jsob.data.invalid) {
				// jsob.message = jsob.message + i + ': ' + jsob.data.invalid[i] + ', ';
			// }
			// jsob.message = jsob.message + ')';
		// }
		// flash_message(jsob);
	// }
// 
	// // GregM: Upgrade Required
	// if (request.status == 402) {
	  // setTimeout(function() {
      // $.modal.close()
      // popup('Upgrade plans', '/misc/upgrade_popup.frag');
	  // }, 500);
// 
	// }
// });
