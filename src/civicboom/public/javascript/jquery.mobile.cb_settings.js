$(document).bind("mobileinit", function(){
    // Sets defaults for jquery mobile
    $.mobile.page.prototype.options.degradeInputs.date = 'text';
    $.mobile.defaultDialogTransition    = 'fade';
    // $.mobile.ajaxEnabled = false;
    $.mobile.selectmenu.prototype.options.nativeMenu = false;
});

$(document).bind("pagecreate", function() {
    // Little hacky, tell any forms created not to ajax submit
    $('form').attr('data-ajax', 'false');
});