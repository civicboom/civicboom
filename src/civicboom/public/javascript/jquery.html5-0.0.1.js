// HTML5 feature emulation for older browsers

function unplacehold(container) {
	$(container).find('input').each(function(i) {
		if ($(this).val() === $(this).attr('placeholder')) {
			$(this).val('');
		}
	});
}

function html5ize (jqContainer) {
	if (typeof jqContainer == 'undefined' || jqContainer == null)
		jqContainer = $('body')

	if (!Modernizr.input.placeholder) {
		jqContainer.find('input').each(function(i) {
			if ($(this).val() =='')
				$(this).val($(this).attr('placeholder'));

			$(this).focus(function(e) {
				if ($(this).val() === $(this).attr('placeholder')) {
					$(this).val('');
				}
			});

			$(this).blur(function(e) {
				if ($(this).val() === '') {
					$(this).val($(this).attr('placeholder'));
				}
			});
		});

		jqContainer.find('form').submit(function(e) {
			$(this).find('input').each(function(i) {
				if ($(this).val() === $(this).attr('placeholder')) {
					$(this).val('');
				}
			});
		});
	}

	if (!Modernizr.inputtypes.date) {
		jqContainer.find("input[type='date']").datepicker ({
			dateFormat: 'yy-mm-dd',
			changeYear: true,
			changeMonth: true,
			yearRange: '1920:2020'
		});
	}
    
	if (!Modernizr.inputtypes.datetime) {
		jqContainer.find("input[type='datetime']").datetimepicker({
            timeFormat: 'hh:mm',
            separator: ' '
		});
	}
}

$(function () { html5ize() });


// date picker
// $(function() {
//  $("input[type='date']").datepicker ({ dateFormat: 'yy-mm-dd', changeYear: true, changeMonth: true, yearRange: '1900:2020'});
//   //, onChangeMonthYear: function (month, year, inst) {
//     // var dateSel = $(this).datepicker("getDate"); 
//     // if (typeof dateSel !== 'null') {
//     //   dateSel.setFullYear(year);
//     //   dateSel.setMonth(month);
//     //   $(this).datepicker("setDate", dateSel);
//     // }
//   //}
//   // });
// });

// Define a cross-browser window.console.log method.
// For IE and FF without Firebug, fallback to using an alert.
if (!window.console) {
	var log = window.opera ? window.opera.postError : alert;
	window.console = { log: function(str) { log(str) } };
}
