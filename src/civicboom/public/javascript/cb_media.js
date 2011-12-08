if (!('media_update' in boom)) {
  boom.media_update = {
    init: function () {
      console.log('boom.media_update.init');
      // Boom_load on ul.media_files will get current frag's attachments & add any new media to the list, calling boom_load on each li it adds to update media items status
      $('body').on('boom_load', 'table.media_files', function () {
      //$('ul.media_files').live('boom_load', function () {
        console.log('table.media_files boom_load');
        var table = $(this);
        var frag = boom.frags.getFragment(table);
        // Set media_update interval, false = no duplicates allowed
        console.log(boom.frags.getFragmentData(table)['json_url']);
        $.getJSON(boom.frags.getFragmentData(table)['json_url'], function (res) {
          var attachments;
          try {
            attachments = res.data.content.attachments;
          } catch (e) {}
          console.log('got attachments', attachments, attachments.length);
          if (attachments && attachments.length)
            for (var i = 0; i < attachments.length; i++) {
              var attachment = attachments[i];
              console.log('attachment', i, attachment);
              if (table.children('tbody.file[data-id="' + attachment.id + '"]').length == 0) {
                var new_media = table.children('tbody.file.template').clone(true, true)
                  .removeClass('template')
                  //.attr('id', 'media_attachment_' + attachment.id)
                  .css('display', '')
                  .data('id', attachment.id)
                  .data('hash', attachment.hash)
                  .data('json_url', '/media/'+attachment.hash+'.json')
                  .attr('data-id', attachment.id);
                console.log('new_element', new_media);
                console.log('append after', table.children('tbody.file').last());
                table.children('tbody.file').last().after(new_media);
                new_media.find('#media_file').val(attachment.name);
                new_media.find('#media_caption').val(attachment.caption);
                new_media.find('#media_credit').val(attachment.credit);
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
      $('body').on('click', 'table.media_files tbody.file input.file_remove', function () {
      //$('ul.media_files li.media_file input.file_remove').live('click', function () {
        console.log('table.media_files tbody.file input.file_remove click');
        var input = $(this);
        var container = input.parents('tbody');
        var id = container.data('id');
        var json_url = container.data('json_url');
        $.post(
          json_url,
          [{name:'id', value:id}, {name:'_method', value:'DELETE'}, {name:'_authentication_token', value:container.parents('form').find('#_authentication_token').val()}],
          function (res) {
            boom.frags.deleteTimer(container, 't_media_update_'+id, true);
            container.remove();
          }
        );
        return false;
      })
      // Boom_load on li.media_file triggers ajax status update, if status is still processing sets interval to refresh (will not add duplicate interval timers), else, doesn't.
      $('body').on('boom_load', 'table.media_files tbody.file', function () {
      //$('ul.media_files li.media_file').live('boom_load', function () {
        console.log('table.media_files tbody.file boom_load');
        var tbody = $(this);
        var id = tbody.data('id');
        $.getJSON(tbody.data('json_url'), function(res) {
          console.log(res);
          var status;
          try {
            status = res.data.media.processing_status;
          } catch (e) {}
          if (status) {
            tbody.find('.status').text(status).css('display', 'inline');
            // the third param=false stops duplicate intervals being created!
            boom.frags.setInterval(tbody, 'media_update_'+id, false, function () {
              tbody.trigger('boom_load');
            }, 10000);
          } else {
            var thumbnail;
            try {
              thumbnail = res.data.media.thumbnail_url;
            } catch (e) {}
            if (thumbnail) {
              boom.frags.deleteTimer(tbody, 't_media_update'+id, true);
              tbody.find('img.media_preview').attr('src', thumbnail+'?'+(new Date().getTime()));
              tbody.children('.status').text('').css('display', 'none');
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
      $('body').on('boom_load', 'div.media_recorder', function () {
      //$('div.media_recorder').live('boom_load', function () {
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
          classid: 'clsid:D27CDB6E-AE6D-11cf-96B8-444553540000',
          codebase: 'http://macromedia.com/cabs/swflash.cab#version=6,0,0,0',
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