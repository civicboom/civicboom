/*
----------------------------------------------------------------------------
 JQuery SimpleModel Setup
----------------------------------------------------------------------------
 http://www.ericmmartin.com/projects/simplemodal/
*/
$.modal.defaults.closeClass = "simplemodalClose";
$.modal.defaults.autoResize = true;
$.modal.defaults.onOpen = function (dialog) {
	dialog.overlay.fadeIn('slow');
	dialog.container.fadeIn('slow');
	dialog.data.fadeIn('slow');
};
$.modal.defaults.onClose = function (dialog) {
	dialog.overlay.fadeOut('slow');
	dialog.container.fadeOut('slow');
	dialog.data.fadeOut('slow', function () {$.modal.close();});
};
