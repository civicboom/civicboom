// Misc Functions

/* http://snippets.dzone.com/posts/show/3817 */
/* NOTE: the following code was extracted from the UFO source and extensively reworked/simplified */
/* Unobtrusive Flash Objects (UFO) v3.20 <http://www.bobbyvandersluis.com/ufo/>
	Copyright 2005, 2006 Bobby van der Sluis
	This software is licensed under the CC-GNU LGPL <http://creativecommons.org/licenses/LGPL/2.1/>
*/
function createCSS(selector, declaration) {
	// test for IE
	var ua = navigator.userAgent.toLowerCase();
	var isIE = (/msie/.test(ua)) && !(/opera/.test(ua)) && (/win/.test(ua));
	
	// create the style node for all browsers
	var style_node = document.createElement("style");
	style_node.setAttribute("type", "text/css");
	style_node.setAttribute("media", "screen"); 
	
	// append a rule for good browsers
	if (!isIE) style_node.appendChild(document.createTextNode(selector + " {" + declaration + "}"));

	// append the style node
	document.getElementsByTagName("head")[0].appendChild(style_node);

	// use alternative methods for IE
	if (isIE && document.styleSheets && document.styleSheets.length > 0) {
		var last_style_node = document.styleSheets[document.styleSheets.length - 1];
		/*
		 * Proto: following if checks function addRule exists, however it's type is returned as 'object'
		 * in IE8 and 'function' in IE9, so we check for either \o/ 
		 */
		if (typeof(last_style_node.addRule) == "object" || typeof(last_style_node.addRule) == "function") {
	        last_style_node.addRule(selector, declaration);
        }
	}
}

if (!('boom' in window))
  boom = {}
// if (!('frags' in boom))
  // throw 'cb_frag should be loaded before misc.head.js!';

if (!('media_update' in boom)) {
  boom.media_update = {
    init: function () {
      console.log('boom.media_update.init');
      // Boom_load on ul.media_files will get current frag's attachments & add any new media to the list, calling boom_load on each li it adds to update media items status
      $('ul.media_files').live('boom_load', function () {
        console.log('ul.media_files boom_load');
        var list = $(this);
        var frag = boom.frags.getFragment(list);
        // Set media_update interval, false = no duplicates allowed
        console.log(boom.frags.getFragmentData(list)['json_url']);
        $.getJSON(boom.frags.getFragmentData(list)['json_url'], function (res) {
          var attachments;
          try {
            attachments = res.data.content.attachments;
          } catch (e) {}
          console.log(attachments);
          if (attachments && attachments.length)
            for (var i = 0; i < attachments.kength; i++) {
              var attachment = attachments[i];
              if (list.children('li[data-id="' + attachment.id + '"]').length == 0) {
                var new_media = list.children('#mediatemplate').clone(true, true).attr('id', 'media_attachment_' + attachment.id).css('display', '');
                new_media.data('id', attachment.id).data('hash', attachment.hash).data('json_url', '/media/'+attachment.hash+'.json');
                list.children('li.media_file').last().after(new_media);
                new_media.find('#media_file').attr('value', attachment.name);
                new_media.find('#media_caption').attr('value', attachment.caption);
                new_media.find('#media_credit').attr('value', attachment.credit);
                new_media.find('*').each(function (index, element) {
                  element = $(element);
                  if (element.attr('id'))
                    element.attr('id', element.attr('id')+'_'+attachment.id);
                  if (element.attr('for'))
                    element.attr('for', element.attr('for')+'_'+attachment.id);
                  if (element.attr('name'))
                    element.attr('name', element.attr('name')+'_'+attachment.id);
                });
                new_media.trigger('boom_load');
              }
            }
        });
        return false;
      });
      // Clicking a media remove button triggers ajax remove, on success removes element from list.
      $('ul.media_files li.media_file input.file_remove').live('click', function () {
        console.log('ul.media_files li.media_file input.file_remove click');
        var input = $(this);
        var li = input.parents('li');
        var id = li.data('id');
        var json_url = li.data('json_url');
        $.post(
          json_url,
          [{name:'id', value:id}, {name:'_method', value:'DELETE'}, {name:'_authentication_token', value:li.parents('form').find('#_authentication_token').val()}],
          function (res) {
            boom.frags.deleteTimer(li, 't_media_update_'+id, true);
            li.remove();
          }
        );
        return false;
      })
      // Boom_load on li.media_file triggers ajax status update, if status is still processing sets interval to refresh (will not add duplicate interval timers), else, doesn't.
      $('ul.media_files li.media_file').live('boom_load', function () {
        console.log('ul.media_files li.media_file boom_load');
        var li = $(this);
        var id = li.data('id');
        $.getJSON(li.data('json_url'), function(res) {
          var status;
          try {
            status = res.data.media.processing_status;
          } catch (e) {}
          if (status) {
            li.children('.status').text(status).css('display', 'inline');
            // the third param=false stops duplicate intervals being created!
            boom.frags.setInterval(li, 'media_update_'+id, false, function () {
              li.trigger('boom_load');
            }, 10000);
          } else {
            var thumbnail;
            try {
              thumbnail = res.data.media.thumbnail_url;
            } catch (e) {}
            if (thumbnail) {
              boom.frags.deleteTimer(li, 't_media_update'+id, true);
              li.find('img').attr('src', thumbnail+'?'+(new Date().getTime()));
              li.children('.status').text('').css('display', 'none');
            }
          }
        });
        return false;
      });
    }
  }
  $(function() {
    boom.media_update.init();
  });
}

if (!('media_recorder' in boom)) {
  boom.media_recorder = {
    init: function () {
      $('div.media_recorder').live('boom_load', function () {
        var div = $(this);
        
        var callback_resize = boom.util.register_flash_callback('cbflashmediaresize', function (height, width) {
          console.log('callback_flash_resize', height, width);
          aHeight = (height*1)+5; 
          aWidth  = (width*1)+14;
          div.css('width', aWidth).css('height', aHeight);
        });
        
        var callback_uploadcomplete = boom.util.register_flash_callback('cbflashmediauploadcomplete', function () {
          console.log('media_upload_flash');
          // Trigger boom_load on ul.media_files within the same form (updates file previews)
          div.parents('form').find('ul.media_files').trigger('boom_load');
        });
        
        div.flash({
          swf: div.data('swf_url') || 'https://bm1.civicboom.com:9443/api_flash_server/cbFlashMedia.swf',
          flashvars: {
            type: "v",
            host: "bm1.civicboom.com",
            user: div.data('member_id'),
            id:   div.data('content_id'),
            key:  div.data('key'),
            callback_resize: callback_resize,
            callback_uploadcomplete: callback_uploadcomplete
          },
          allowscriptaccess: 'always',
          width: '100%',
          height: '100%',
        });
        
      });
    }
  }
  $(function() {
    boom.media_recorder.init();
  })
}

function limitInputLength (event, textElement, maxLength) {
	var textLength = $(textElement).val().length;
	if (event.keyCode < 1)
		if ( ($(textElement).val().length >= maxLength) || ($(textElement).text().length >= maxLength) )
			return false;
	return true;
}

function countInputLength (event, textElement, maxLength, statusElement) {
	var textLength = $(textElement).val().length;
	if (typeof statusElement != 'undefined') statusElement.text(maxLength - (textLength));
}

// function convertYesNoCheckbox() {
  // //return;
	// var selects = $('select.yesno').filter(':visible');
	// if (selects.length == 0) return;
	// selects.after('<input type="checkbox" class="yesnocheck unproc" />');
	// selects.hide();
	// var checks = $('input.yesnocheck').filter('.unproc');
	// checks.each(function(index) {
	    // var value = $(this).prev('select.yesno').val();
	    // $(this).attr('checked', !(value == '' || value == 'no'));
	// });
	// checks.unbind().change(function() {
	    // var yesno = $(this).prev('select.yesno');
	    // var yes = yesno.children('.yes').val();
	    // var no  = yesno.children('.no' ).val();
	    // yesno.val(this.checked ? yes:no);
	// });
	// checks.removeClass('unproc');
// }

//$(convertYesNoCheckbox);

function init_validation(element, validator) {
	var check_timer = null;
	element.keyup(function() {
		element.removeClass("valid");
		element.removeClass("invalid");
		clearTimeout(check_timer);
		check_timer = setTimeout(validator, 500);
	});
}
