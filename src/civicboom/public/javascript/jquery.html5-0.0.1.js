// HTML5 feature emulation for older browsers

$(function() {

// http://borderstylo.com/posts/213-html5-feature-detection-and-adding-support-for-the-placeholder-attribute
if (!Modernizr.input.placeholder){
  $('input').each(function(i){
    $(this).val($(this).attr('placeholder'));

    $(this).focus(function(e){
      if ($(this).val() === $(this).attr('placeholder')) {
        $(this).val('');
      }
    });

    $(this).blur(function(e){
      if ($(this).val() === '') {
        $(this).val($(this).attr('placeholder'));
      }
    });
  });

  $('form').submit(function(e){
    $(this).find('input').each(function(i){
      if ($(this).val() === $(this).attr('placeholder')) {
        $(this).val('');
      }
    });
  });
}

// date picker
$(function() {$("input[type='date']").datepicker({ dateFormat: 'yy-mm-dd' });});

});
