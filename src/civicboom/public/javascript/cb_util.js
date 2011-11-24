/* Civicboom Utilities
 * These are mostly used internally by the Civicboom Frags system.
 * boom.util.*
 */
if(!('util' in boom)) {
  boom.util = {
    /*
     * If given object is jquery, return it, else convert it to jquery.
     */
    convert_jquery : function(element) {
      return (element.jquery) ? element : $(element);
    },
    /*
     * Toggles the visibility of the next element.
     */
    toggle_section : function(element) {
      element = boom.util.convert_jquery(element);
      element.next().slideToggle();
      var icon = element.find('.icon');
      var icon_more = 'icon_plus';
      var icon_less = 'icon_down';

      if(icon.hasClass(icon_more)) {
        icon.removeClass(icon_more);
        icon.addClass(icon_less);
      } else if(icon.hasClass(icon_less)) {
        icon.removeClass(icon_less);
        icon.addClass(icon_more);
      }
    },
    /*
     * TinyMCE utilities
     * boom.util.tinymce.*
     */
    tinymce : {
      /*
       * Initialise all tinymce (.editor) components within element
       */
      init : function(element) {
        element = boom.util.convert_jquery(element);
        element.find('.editor').tinymce({
          script_url : '/javascript/tiny_mce/tiny_mce.js',
          theme : 'advanced',
          mode : 'exact',
          theme_advanced_buttons1 : 'bold,italic,underline,separator,strikethrough,justifyleft,justifycenter,justifyright,justifyfull,bullist,numlist,link,unlink',
          theme_advanced_buttons2 : '',
          theme_advanced_buttons3 : '',
          theme_advanced_toolbar_location : 'top',
          theme_advanced_toolbar_align : 'left',
        });
      },
      /*
       * Save all tinymce (.editor) components within element
       */
      save : function(element) {
        element = boom.util.convert_jquery(element);
        var tmce = element.find('.editor').tinymce();
        if(tmce && tmce.save)
          return tmce.save();
      }
    },
    /*
     * Modal Queue Utility
     * boom.util.modal_queue.*
     */
    modal_queue : {
      /*
       * Initialise jQuery Modal
       */
      init : function() {
        $.modal.defaults.closeClass = "simplemodalClose";
        $.modal.defaults.autoResize = true;
        $.modal.defaults.zIndex = 2000;
        /* OSM bits are 1000-1100 */
        $.modal.defaults.onOpen = function(dialog) {
          dialog.overlay.fadeIn('slow');
          dialog.container.fadeIn('slow');
          dialog.data.fadeIn('slow');
        };
        $.modal.defaults.onClose = function(dialog) {
          dialog.overlay.fadeOut('slow');
          dialog.container.fadeOut('slow');
          dialog.data.fadeOut('slow', function() {
            $.modal.close();
          });
        };
      },
      /*
       * Add content to the modal queue, ready to display at the next available opportunity
       */
      add : function(content, parent, onClose) {
        var content_body, content_title, content_buttons;
        if (typeof content == 'object') {
          content_body = content.body;
          content_title = content.title;
          content_buttons = content.buttons;
        } else {
          content_body = content;
        }
        
        content_body = $('<div />').addClass('resizeThis').append(boom.util.convert_jquery(content_body));
        
        
        $('body').delay(0)// Needed to trigger the queue
        .queue(function(next) {
          // Queue the modal, onClose trigger next queue item
          var body = $(this);
          //parent = parent
          var dialog = boom.util.convert_jquery(content_body)
            .dialog({
              //autoOpen: false,
              title: content_title,
              buttons: content_buttons,
              modal: true,
              position: {
                of: parent,
                at: 'center top',
                my: 'center top',
                collision: 'none'
              },
              draggable: false,
              resizable: false,
              show: {
                effect: 'slide',
                direction: 'up'
              },
              hide: {
                effect: 'slide',
                direction: 'up'
              },
              width: 'auto',
              minWidth: '300 px',
              height: 'auto',
              open: function (event, ui) {
                //if (parent) $(this).parent().appendTo(parent);
                $(this).find('.event_load').trigger('boom_load');
                console.log('open', ui);
                console.log('open', $(this).dialog('option', 'position'));
              },
              beforeClose: function () {
                // For some reason close does not trigger on x clicked / esc pressed
                console.log('dialog.beforeClose');
                if (onClose) onClose();
                next();
                return true; // Must return true otherwise close never triggered
              },
              close: function (event, ui) {
                console.log('dialog.close');
                $(this).dialog('destroy');
                return false;
              },
              resize: function (event, ui) {
                console.log('resize', $(this).dialog('option', 'position'));
              },
              resizeStop: function (event, ui) {
                console.log('resizeStop', $(this).dialog('option', 'position'));
                var position = $(this).dialog('option', 'position');
                $(this).dialog('option', 'position');
              }
            });
            //dialog.dialog('open');
          // $.modal(content, {
            // onClose : function() {
              // if(onClose)
                // onClose();
              // $.modal.close();
              // next();
            // },
            // onShow : function() {
              // $.modal.update();
              // // this.d.data.find('.event_load').each(function() {
              // // var evented = $(this);
              // // console.log(evented, evented.length);
              // // evented.trigger('boom_load');
              // // })
              // this.d.data.find('.event_load').trigger('boom_load');
            // }
          // })
        }).delay(150);
        // Next queue item always 100ms delay between popups
      },
      /*
       * Clear the modal queue
       */
      clear : function() {
        $('body').clearQueue('modal');
      }
    },
    /*
     * Display a Civicboom flash message, takes either a string message or an object returned from the api
     */
    flash_message : {
      show : function(json_message) {
        if( typeof json_message == "string")
          json_message = {
            status : 'ok',
            message : json_message
          };
        if(json_message && typeof json_message.message == 'string' && json_message) {
          $('#flash_message').removeClass('status_error status_ok').addClass('status_' + json_message.status).text(json_message.message).fadeIn('slow').delay(5000).fadeOut('slow').mouseover(function() {
            $(this).stop(true).fadeOut('fast');
          });
        }
      },
      init : function() {
        $('body').on('boom_load', '#flash_message, .flash_message_data', function () {
        //$('#flash_message, .flash_message_data').live('boom_load', function() {
          var element = $(this);
          var json = element.data('message-json');
          if (json) {
            console.log(json);
            boom.util.flash_message.show(json);
          }
        });
      }
    },
    history : {
      saveState : function(state_object, replace) {
        var current_url = state_object.current_url;
        if(Modernizr.history) {
          // Note: this object is limited to 640k (which ought to be
          // enough for anyone) when saved in the browser history file
          try {
            if(replace) {
              history.replaceState(state_object, "Civicboom", current_url);
            } else {
              history.pushState(state_object, "Civicboom", current_url);
            }
          } catch (e) {
            console.log('history state save error', state_object, replace, e);
          }
        } else {

        }
      },
    },
    desktop_notification : {
      has_support : function() {
        return !!window.webkitNotifications;
      },
      has_permission : function() {
        return window.webkitNotifications.checkPermission() == 0
      },
      request_permission : function(callback) {
        console.log('desktop_notification.request_permission');
        window.webkitNotifications.requestPermission(function() {
          console.log('desktop_notification.request_permission.callback');
          var has_permission = window.webkitNotifications.checkPermission() == 0;
          if(has_permission)
            $('.desktop_notifications').hide();
          if(callback)
            callback(has_permission);
        });
      },
      notify : function(icon, body, title, timeout) {
        console.log('notify');
        if(window.webkitNotifications.checkPermission() == 0) {
          console.log('has permission');
          var popup = window.webkitNotifications.createNotification(icon, body, title);
          popup.show();
          if(timeout)
            setTimeout(function() {
              popup.cancel()
            }, timeout);
          return true;
        }
        return false;
      }
    },
    message_indicators : {
      key_icon_map : {
        num_unread_messages : '.msg_c_m',
        num_unread_notifications : '.msg_c_n',
        _total : '.msg_c_o'
      },
      last_check : {
        last_message_timestamp : null,
        last_notification_timestamp : null
      },
      messages : {
        last_message_timestamp : 'New message',
        last_notification_timestamp : 'New notification'
      },
      update : function() {
        $.getJSON('/profile/messages.json', function(res) {
          if('data' in res) {
            var message = $([]);
            var _total = 0;
            for(key in boom.util.message_indicators.key_icon_map) {
              if( key in res.data) {
                var jQe = $(boom.util.message_indicators.key_icon_map[key]);
                var val = res.data[key];
                jQe.html('&nbsp;' + val + '&nbsp;');
                if(val == 0) {
                  jQe.hide();
                } else {
                  jQe.show();
                }
                _total += (res.data[key] * 1);
              }
            }
            if('_total' in boom.util.message_indicators.key_icon_map) {
              var jQe = $(boom.util.message_indicators.key_icon_map['_total']);
              jQe.html('&nbsp;' + _total + '&nbsp;');
              if(_total == 0) {
                jQe.css('display', 'none');
              } else {
                jQe.css('display', 'inline');
              }
            }
            if(!boom.util.desktop_notification.has_support())
              return;
            var body = '';
            var body_content = false;
            for(key in boom.util.message_indicators.last_check) {
              if( key in res.data) {
                var val = res.data[key];
                if(boom.util.message_indicators.last_check[key] && boom.util.message_indicators.last_check[key] < val) {
                  // Display things
                  if(body_content)
                    body += '<br />&amp;<br />';
                  body += boom.util.message_indicators.messages[key]
                  body_content = true;
                }
                boom.util.message_indicators.last_check[key] = val;
              }
            }
            if(body_content)
              boom.util.desktop_notification.notify('', 'Civicboom', body, 5000);
          }
        });
      },
      init : function() {
        console.log('message_indicators.init');
        if (! $('body').hasClass('u-user')) return;
        console.log('user logged in');
        setInterval(boom.util.message_indicators.update, 120000);
        $(function() {
          if(boom.util.desktop_notification.has_support() && !boom.util.desktop_notification.has_permission())
            $('.desktop_notifications').show();
        })
      }
    },
    register_flash_callback : function(name, func) {
      var name_time;
      do {
        name_time = name + (new Date().getTime())
      } while (name_time in window)
      window[name_time] = func;
      return name_time;
    },
    convertYesNoCheckboxes : function(element) {
      element = boom.util.convert_jquery(element);
      //return;
      var selects = element.find('select.yesno').filter(':visible');
      if(selects.length == 0)
        return;
      selects.after('<input type="checkbox" class="yesnocheck unproc" />');
      selects.hide();
      var checks = element('input.yesnocheck').filter('.unproc');
      checks.each(function(index) {
        var value = $(this).prev('select.yesno').val();
        $(this).attr('checked', !(value == '' || value == 'no'));
      });
      checks.unbind().change(function() {
        var yesno = $(this).prev('select.yesno');
        var yes = yesno.children('.yes').val();
        var no = yesno.children('.no').val();
        yesno.val(this.checked ? yes : no);
      });
      checks.removeClass('unproc');
    },
    validators : {
      init : function() {
        for(selector in boom.util.validators.validators) {
          console.log('Initialising validator .validate_field' + selector)
          $('body').on('keyup', '.validate_field' + selector, function () {
          //$('.validate_field' + selector).live('keyup', function() {
            var element = $(this);
            element.removeClass('invalid').removeClass('valid');
            clearTimeout(element.data('validator_timeout'));
            element.data('validator_timeout', setTimeout(function() {
              boom.util.validators.validators[selector](element);
            }, 500));
            return false;
          });
        }
      },
      validators : {
        '.username_register' : function(element) {
          console.log('username_register validator triggered');
          var status = element.parents('form').find('.validation-result').css("display", "table-row").find('.urldemo');
          var val = element.val();
          if(val.length < 4) {
            status.html("Username must be at least 4 characters");
            element.addClass("invalid");
          } else {
            var username = val.toLowerCase().replace(/[^a-z0-9_-]/g, '-').replace(/^-+|-+$/g, '');
            $.ajax("/members.json?username=" + username, {
              "success" : function(result) {
                if(result.data.list.count == 0) {
                  status.html("Your profile page will be https://www.civicboom.com/members/" + username);
                  element.addClass("valid");
                } else {
                  status.html("The username " + val + " is already taken")
                  element.addClass("invalid");
                }
              }
            });
          }
        },
        '.email_register' : function(element) {
          console.log('email_register validator triggered');
          var val = element.val();
          if(val.match(/.+@.+\..+/)) {
            element.addClass("valid");
          } else {
            element.addClass("invalid");
          }
        }
      }
    },
    formArrayNoPlaceholders : function(form) {
      var formArray = form.serializeArray();
      var placeheld = form.find('input[placeholder]');
      if(placeheld.length > 0)
        for(var i = 0; i < placeheld.length; i++) {
          var elemjq = $(placeheld[i]);
          if( typeof elemjq.attr('placeholder') != 'undefined') {
            for(var j = 0; j < formArray.length; j++) {
              if(formArray[j].name == elemjq.attr('name')) {
                if(formArray[j].value == elemjq.attr('placeholder'))
                  formArray[j].value = '';
                break;
              }
            }
          }
        }
      return formArray;
    },
    mouseCursor: function(style) {
      $('body').css('cursor', style);
    }
  }
  boom.init_foot.push(boom.util.modal_queue.init);
  boom.util.flash_message.init();
  $(boom.util.message_indicators.init);
  boom.util.validators.init();
}