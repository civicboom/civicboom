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

// var media_thumbnail_timers = {};
// var media_jquery_objects = {};
// 
// 
// 
// function updateMedia(id, hash, jquery_element) {
  // if (typeof media_jquery_objects[id] == 'undefined')
  // {
    // media_jquery_objects[id] = jquery_element;
  // } else {
    // jquery_element = media_jquery_objects[id];
  // }
  // if (typeof media_thumbnail_timers[id] == 'undefined')
    // media_thumbnail_timers[id] = setInterval ('updateMedia('+id+',"'+hash+'")', 1000);
  // function processingStatus(data) {
    // _status = false;
    // try {
      // _status = data.data.media.processing_status;
    // } catch (e) {}
    // if(!_status) {
      // _thumbnail = data.data.media.thumbnail_url;
      // clearInterval(media_thumbnail_timers[id]);
      // delete media_thumbnail_timers[id];
      // jquery_element.find('img').attr('src', _thumbnail + "?" + (new Date().getTime()));
      // jquery_element.find('span').text('').css('display', 'none'); 
    // }
    // else {
      // jquery_element.find('span').css('display', 'inline').text(_status);
    // }
  // }
  // $.getJSON(
    // '/media/' + hash + '.json',
    // processingStatus
  // );
// }
// 
// function appendAttr(element, name, append) {
  // if (element.length == 0) return;
  // if (element.attr(name)) element.attr(name, element.attr(name) + '_' + append);
// }
// 
// function setAttrIf(element, name, val) {
  // if (element.length == 0) return;
  // if (element.attr(name)) element.attr(name, val);
// }
// 
// function removeMedia(jquery_element) {
  // var id = jquery_element.attr('name').split('_')[2];
	// var url = "/media/"+id+".json";
	// var post = [
	      // {name: "id", value: id},
				// {name: "_method", value: "DELETE"},
				// {name: "_authentication_token", value: jquery_element.parents('form').find('#_authentication_token').val()}
	   // ];
	// $.post( url, post, function(data) {
		// jquery_element.parents('li').remove();
		// if (typeof media_thumbnail_timers[id] != 'undefined') {
      // clearInterval(media_thumbnail_timers[id]);
      // delete media_thumbnail_timers[id];
    // }
	// });
	// return false;
// }
// 
// function refreshProgress (jquery_element) {
  // var url = jquery_element.parents('.'+fragment_container_class).find('.'+fragment_source_class).attr('href').replace(/\.frag$/, '.json');
  // $.getJSON( url, function (data) {
    // if (typeof data.data.content.attachments != 'undefined') {
      // var attachments = data.data.content.attachments
      // //Y.log (attachments.length);
      // for (var i = 0; i < attachments.length; i ++) {
        // var attachment = attachments[i];
        // //Y.log ('#media_attachment_' + attachment.id + ' :' + $('#media_attachment_' + attachment.id).length);
        // if ($('#media_attachment_' + attachment.id).length == 0) {
          // //Y.log ('I found a new attachment!');
          // var at_element = jquery_element.find('#mediatemplate').clone(true, true).attr('id', 'media_attachment_' + attachment.id).css('display','');
          // jquery_element.find('ul.media_files').children('li.media_file').last().after(at_element);
          // at_element.find('#media_file').attr('value', attachment.name);
          // at_element.find('#media_caption').attr('value', attachment.caption);
          // at_element.find('#media_credit').attr('value', attachment.credit);
          // at_element.find('*').each(function (index, element) {
            // element = $(element);
            // appendAttr(element, 'id', attachment.id);
            // appendAttr(element, 'for', attachment.id);
            // appendAng ttr(element, 'name', attachment.id);
          // });
          // updateMedia(attachment.id, attachment.hash, at_element);
        // }
      // }
    // }
  // });
// }

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

function convertYesNoCheckbox() {
  //return;
	var selects = $('select.yesno').filter(':visible');
	if (selects.length == 0) return;
	selects.after('<input type="checkbox" class="yesnocheck unproc" />');
	selects.hide();
	var checks = $('input.yesnocheck').filter('.unproc');
	checks.each(function(index) {
	    var value = $(this).prev('select.yesno').val();
	    $(this).attr('checked', !(value == '' || value == 'no'));
	});
	checks.unbind().change(function() {
	    var yesno = $(this).prev('select.yesno');
	    var yes = yesno.children('.yes').val();
	    var no  = yesno.children('.no' ).val();
	    yesno.val(this.checked ? yes:no);
	});
	checks.removeClass('unproc');
}

$(convertYesNoCheckbox);

function init_validation(element, validator) {
	var check_timer = null;
	element.keyup(function() {
		element.removeClass("valid");
		element.removeClass("invalid");
		clearTimeout(check_timer);
		check_timer = setTimeout(validator, 500);
	});
}
