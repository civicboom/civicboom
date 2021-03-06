if (!('invite' in window.boom)) {
  boom.invite = {
    templates: {
      'assignment': function (id, frag) {
        return {
          content: $('<div />').append($('<ul></ul>').tagged({
            appendTo: frag.children('.frag_data'),
            hiddenFieldName: 'usernames',
            placeholder: 'Search...',
            removeElement: '<a href="#" class="cb-tag-remove fr icon16 i_delete"></a>',
            tagSource: function (term, callback, self) {
              $.getJSON(
                '/members.json',
                {
                  term: term.term,
                  exclude_members: self.hiddenField.val()
                },
                function (res) {
                  if (res.status != 'ok') return callback([]);
                  var items = res.data.list.items;
                  callback(items);
                }
              )
            },
            itemNormaliser: function (item) {
              return item;
            },
            update: function () {
              var dialog = $(this).parents('.ui-dialog-content');
              var position = dialog.dialog('option', 'position');
              console.log(position);
              dialog.dialog('option', 'position', position);
            },
            itemRenderer: function (item){
              return $('<li class="member_item" />')
                .data('value', item.username)
                .append(
                  $('<a />')
                    .append(
                      $('<div class="thumbnail thumbnail_small" />').append($('<img />').attr('src', item.avatar_url))
                    ).append(
                      $('<div class="member_details" />').append(item.name).append('<br />').append('('+item.username+')')
                    )
                );
            }
          })),
          buttons: {
            'Invite': function () {
              var button = $(this);
              var frag = boom.frags.getFragment(button);
              var data = frag.children('.frag_data').data();
              var invitees = button.prev('ul').children('.cb-tag-new').children('.cb-tag-hidden').val().split(',');
              var post_vars = {'submit-invite': true, invite: 'assignment', id: data.id}
              for (var i=0; i < invitees.length; i++) {
                post_vars['inv-'+i] = invitees[i];
              }
              $.post('/invite/index/'+data.id+'.json', post_vars, function (res, status, req) {
                boom.util.flash_message.show(res);
                console.log(res, status, req);
                button.prev('ul').tagged('clear');
              });
            }
          }
        
        }
      }
    },
    init: function () {
      $('#app').on('click', '.invite_link', function (event) {
        var link = $(this);
        var frag = boom.frags.getFragment(link);
        var invite_type = link.data('invite');
        var invite_id = link.data('invite-id') || frag.data('id');
        if (! (invite_type in boom.invite.templates)) return true;
        var object = boom.invite.templates[invite_type](0, frag)
        
        var content = $('<div />').append(object.content)
        content.dialog({buttons: object.buttons, position: {of: link, my: 'right top', at: 'left top', collision:'flip'}, width: 200, draggable: false, resizable: false, title: 'Invite', open: function () { $(this).dialog('widget').appendTo(frag.children('.frag_data'))  }});
        return false;
      });
      var container = '.frag_data.c-invite ';
      $('#app').on('click', container+'.invite_click', function (event) {
      //$(container+'.invite_click').live('click', function () {
        event.stopImmediatePropagation();
        var button = $(this);
        var form = button.parents('form');
        var exclude_members = form.find('.exclude-members').val().split(',');
        var button_name = button.attr('name');
        if (button_name == 'Invite') return true;
        var button_action = button_name.split('-',1)[0];
        var button_key = button_name.substring(button_name.search('-')+1);
        
        var offset  = form.find('.invitee-offset').val();
        var limit   = form.find('.search-limit').val();
        var ul      = form.find('.invitee_ul');
        
        switch (button_action) {
          case 'add':
            if (exclude_members.contains(button_key)) {
              // Member already in invitee list!
              return false;
            }
            var li = button.parents('li').detach();
            ul.prepend(li);
            ul.children('li.none').remove();
            exclude_members.push(button_key);
            var id = (exclude_members.length - 1);
            form.find('.exclude-members').val(exclude_members.join(','));
            li.append($('<input type="hidden" class="username" />').attr('name', 'inv-'+id).val(button_key));
            button.val('Remove').attr('name', 'rem-'+id).children('div').removeClass('i_plus_blue').addClass('i_delete').children('span').html('Remove');
            boom.invite.refresh_search(button);
          break;
          case 'rem':
            var li = button.parents('li');
            var li_ul = li.parents('ul');
            var username = li.find('input.username').val();
            exclude_members = exclude_members.remove(username);
            form.find('.exclude-members').val(exclude_members.join(','));
            boom.invite.refresh_search(button);
            li.remove();
            if (ul.children('li').length == 0)
              ul.append('<li class="none">Select people to invite from the right</li>');
          break;
          case 'search':
            boom.invite.refresh_search(button, [{ 'name':button_name }]);
            return false;
          break;
          case 'invitee':
            switch (button_key) {
              case 'next':
                offset = offset + limit;
              break;
              case 'prev':
                offset = offset - limit;
                if (offset < 0) offset = 0;
              break;
            }
          break;
        }
        form.find('.invitee-offset').val(offset);
        form.find('.search-limit').val(limit);
        boom.invite.list_paginate(ul, offset, limit, form.find('input[name="invitee-prev"]'), form.find('input[name="invitee-next"]'));
        return false;
      });
      $('#app').on('click', container+'.invite_post', function () {
      //$(container+'.invite_post').live('click', function () {
        console.log('invite_post click');
        var element = $(this);
        var form = element.parents('form');
        var frag = form.parents('.frag_container');
        var frag_refresh = frag.find('.frag_refresh').val();
        var formArray = boom.util.formArrayNoPlaceholders(form);
        if (typeof element.attr('name') != 'undefined')
          formArray.push({'name': element.attr('name'), 'value': element.val()});
        $.post("/invite/index.frag", formArray, function (data) {
          if (frag_refresh) {
            cb_frag_reload(frag_refresh);
            console.log(frag_refresh);
          }
          frag.html(data);
          frag.find('.event_load').trigger('boom_load');
        });
        return false;
      });
    },
    refresh_search: function(element, extra_fields) {
      var form = element.parents('form');
      var exclude_members = form.find('.exclude-members').val().split(',');
      var ul = form.find('.invite-list');
      var formArray = boom.util.formArrayNoPlaceholders(form);
      if (extra_fields)
        formArray.concat(extra_fields);
      formArray.push({'name': 'exclude-members', 'value': exclude_members});
      $.post('/invite/search.frag', formArray, function (data) {
        ul.html(data);
        ul.children('.search-offset').val()
      });
    },
    list_paginate: function (ul, offset, limit, prev, next) {
      var visible = ul.children('li:eq('+offset+'),li:gt('+offset+')').filter('li:lt('+limit+')').css('display','inline-block');
      var hidden  = ul.children('li').not(visible).css('display','none');
      if (typeof prev != 'undefined')
        if (offset > 0) {
          prev.removeClass('disabled').attr('disabled','');
        } else {
          prev.addClass('disabled').attr('disabled','disabled');
        }
      if (typeof next != 'undefined')
        if ((offset + limit) < ul.children('li').length) {
          next.removeClass('disabled').attr('disabled','');
        } else {
          next.addClass('disabled').attr('disabled','disabled');
        }
    },
    
  }
  boom.invite.init()
}

