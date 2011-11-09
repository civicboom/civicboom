if (!('boom' in window))
  boom = {}
if (!('invite' in window.boom)) {
  boom.invite = {
    init: function () {
      var container = '.frag_data.c-invite ';
      $(container+'.invite_click').live('click', function () {
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
      $(container+'.invite_post').live('click', function () {
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