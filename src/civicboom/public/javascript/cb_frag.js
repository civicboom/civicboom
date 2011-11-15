// JQUERY PLUGIN: I append each jQuery object (in an array of
// jQuery objects) to the currently selected collection.
jQuery.fn.appendEach = function(arrayOfWrappers) {

  // Map the array of jQuery objects to an array of
  // raw DOM nodes.
  var rawArray = jQuery.map(arrayOfWrappers, function(value, index) {

    // Return the unwrapped version. This will return
    // the underlying DOM nodes contained within each
    // jQuery value.
    return (value.get() );

  });
  // Add the raw DOM array to the current collection.
  this.append(rawArray);

  // Return this reference to maintain method chaining.
  return (this );

};

if(!('boom' in window))
  boom = {};

if(!('boom_development' in window) || !('console' in window) || !console.log)
  console = {
    log: function () {}
  }

boom.init_foot = [];

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
      add : function(content, onClose) {
        $('body').delay(0)// Needed to trigger the queue
        .queue(function(next) {
          // Queue the modal, onClose trigger next queue item
          var body = $(this);
          $.modal(content, {
            onClose : function() {
              if(onClose)
                onClose();
              $.modal.close();
              next();
            },
            onShow : function() {
              $.modal.update();
              // this.d.data.find('.event_load').each(function() {
              // var evented = $(this);
              // console.log(evented, evented.length);
              // evented.trigger('boom_load');
              // })
              this.d.data.find('.event_load').trigger('boom_load');
            }
          })
        }).delay(100);
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
        $('#flash_message, .flash_message_data').live('boom_load', function() {
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
          if(replace) {
            history.replaceState(state_object, "Civicboom", current_url);
          } else {
            history.pushState(state_object, "Civicboom", current_url);
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
          $('.validate_field' + selector).live('keyup', function() {
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
    }
  }
}
boom.init_foot.push(boom.util.modal_queue.init);
boom.util.flash_message.init();
boom.util.message_indicators.init();
boom.util.validators.init();
/*
 * Civicboom Fragment System
 * Use the following for most of your fragment work, there are loads of events available to use!
 * boom.frags.*
 */
if(!('frags' in boom)) {
  boom.frags = {
    // Prefix for each frag's id
    prefix : 'frag_',
    // Populated with #frag_containers
    container : null,
    classes : {
      // HTML classes for key components
      container : 'frag_container',
      source : 'frag_source',
      data : 'frag_data',
      help : 'frag_help',
    },
    vars : {
      auto_save_time : 60000,
      scroll_duration : 600,
      default_frags : ['/profile.frag', '/misc/featured.frag'],
    },
    /*
     * Templates take varying arguments and return a jquery element containing dom elements that are not within the document.
     */
    templates : {
      /*
       * Returns the default frag loading placeholder
       */
      loading_holder : function() {
        return $('' +
          // Loading placeholder holder for frags
          '    <div class="frag_bars">' +
          '        <div class="title_bar"></div>' +
          '        <div class="action_bar"></div>' +
          '        <div style="clear: both;"></div>' +
          '    </div>' +
          '    <div class="frag_data frag_content" style="overflow-y: hidden;">' + 
          '   <table style="height: 100%; text-align: center; margin: auto;"><tbody><tr><td>' + 
          '     Loading' + '     <br>&nbsp;<br><img src="/images/ajax-loader.gif">' + 
          '   </td></tr></tbody></table>' + 
          ' </div>'
        );
      },
      /*
       * Returns modal popup content with added title, message, and confirm_type class
       */
      modal_data : function(title, message, confirm_type) {
        return $('<div />')
          .addClass('popup-modal')
          .append(
            $('<div />')
            .addClass(confirm_type || 'information')
            .append(
              $('<div />')
              .addClass('popup-title')
              .append(title)
              .append(
                $('<a />')
                .addClass('fr simplemodalClose')
                .append('&nbsp;x&nbsp;')
              )
            )
            .append(
              $('<div />')
              .addClass('popup-message')
              .append(message)
            )
          )
      },
      /*
       * Returns modal popup content to confirm an action, taking values from a link's data.
       * settings = link.data()
       * originalLink = link
       * The link can have data-*:
       *  confirm-type:   class for confirm box
       *  confirm-avatar: if true display current persona avatar above title
       *  confirm-icon:   if true take icon from original link and make 32x32
       *  confirm:        html message to display
       *  confirm-yes:    text to display on yes link
       *  confirm-no:     text to dispkay on no link
       *  confirm-secure-options: array of objects used to create yes links that change the secure link, instead of yes / no buttons.
       *    e.g. [ {confirm: "Text of the secure link", json: "/new/json/url/for?secure=link"}, {confirm: "Repeat here, leave json out to use original json url"} ]
       */
      modal_confirm : function(settings, originalLink) {
        if( typeof settings == 'string')
          settings = JSON.parse(settings.replace(/\'/g, '\"'));
        console.log(settings.confirmSecureOptions);
        if( typeof settings.confirmSecureOptions == 'string')
          settings.confirmSecureOptions = JSON.parse(settings.confirmSecureOptions.replace(/\'/g, '\"'));
        // Return modal content as jQuery object
        // Popup jQuery, begin with outer layer, work in. popup-modal:
        return $('<div />').addClass('popup-modal').append(
        // popup_content
        $('<div />').addClass('popup_content').append(
        // information/alert/etc.
        $('<div />').addClass(settings.confirmType || 'information').append(
        // popup-title
        $('<div />').addClass('popup-title')
        // If confirm-avatar copy avatar from top right of site & re-style
        .append(settings.confirmAvatar ? $('<div />').addClass('popup-persona').append($('#persona_avatar').children('img').clone()).append($('#persona_details').clone().text())
        //                    $('#persona_holder').clone().attr('id','').addClass('popup-persona')
        : '')
        // If icon set icon else take icon name from link clicked
        .append(settings.icon ? $('<span />').addClass('icon32').addClass('i_' + settings.icon) : originalLink.children('.icon32, .icon16').first().clone(false).removeClass('icon16').addClass('icon32'))
        // If confirm-title set it as the title, otherwise use the original link's text
        .append(settings.confirmTitle || originalLink.text() || '').append($('<a />').addClass('fr simplemodalClose').append('&nbsp;x&nbsp;'))).append(
        // popup-message
        $('<div />').addClass('popup-message').append(settings.confirm || '')).append(
        // popup-actions
        $('<div />').addClass('popup-actions').append((settings.confirmSecureOptions && originalLink.hasClass('link_secure')) ? (
          // secure options
          $('<ul />').appendEach($.map(settings.confirmSecureOptions, function(value) {
            return $('<li />').append(value.title ? $('<h3 />').append(value.title) : '').append(value.content).append($('<a />').addClass('button').append(originalLink.text()).data('original', originalLink).data('json', value.json).click(function() {
              var link = $(this);
              var original = link.data('original');
              console.log(link, link.data());
              console.log(original, original.data());
              original.data('confirmed', 'true');
              console.log(1, original.siblings('form').data('json'));
              original.siblings('form').data('json', link.data('json'));
              //original.data('json', link.data('json'));
              console.log(2, original.siblings('form').data('json'));
              console.log(original, original.data());
              original.click();
              $.modal.close();
            }));
          }))
        ) : (
          // buttons
          $('<a />').addClass('button').data('original', originalLink).html(settings.confirmYes || 'Yes').click(function() {
            var link = $(this);
            console.log('click', this, link);
            var original = link.data('original');
            original.data('confirmed', 'true');
            original.click();
            $.modal.close();
          }).after(originalLink.hasClass('link_dummy') ? '' : $('<a />').addClass('button').html(settings.confirmNo || 'No').click($.modal.close))
        )))));
      }
    },
    // Frag counter (ensures frags are unique)
    counter : 0,
    /*
     * Events
     * The Fragment system fires events to allow code to run when things happen.
     * Events are split into two categories:
     * "frag" events:
     *    load:         triggered when a frag loads dynamically.
     *    load_static:  triggered when a frag loads dynamically or statically (you can check if the dynamic argument is true)
     * "live" events:
     *    These trigger based on selector and event type. e.g.
     *  {'a': {
     *   'click': function () {
     *     // Triggered on clicking a link
     *   }
     *  }}
     */
    events : {
      frag : {
        'load' : function(event, from_history) {
          var current_frag = $(this);
          var current_frag_data = boom.frags.getFragmentData(current_frag);
          // current_frag.find('.'+boom.frags.classes.data).data();
          console.log('frag_load', this);
          if(!from_history)
            // Push current frag's url (preferably html_url, else frag_url) to google analytics
            _gaq.push(['_trackPageview', current_frag_data.html_url || current_frag_data.frag_url]);

          // Call static frag load event with current event arguments & context
          boom.frags.events.frag.load_static.call(this, event, from_history, true);
          return false;
        },
        'load_static' : function(event, from_history, dynamic) {
          var current_frag = $(this);
          console.log('frag_load_static', this);
          // Push history, only if not loaded from history & current frag is last loaded!
          if(!from_history && current_frag.is(boom.frags.container.children().last())) {
            var history_state = boom.frags.getHistoryState();
            console.log('history.saveState', history_state, !dynamic)
            boom.util.history.saveState(history_state, !dynamic);
            // replace current history if not dynamic!
          }
          // Trigger any load events for event_load elements
          current_frag.find('.event_load').trigger('boom_load');
          // TinyMCE
          boom.util.tinymce.init(current_frag);
          // html5ize new fragment (datetime boxes etc.)
          html5ize(current_frag);
          // convert yes/no dropdowns to checkboxes
          boom.util.convertYesNoCheckboxes(current_frag);
          // Set up auto save
          current_frag.find('form.auto_save').each(function() {
            boom.frags.setAutoSave(this);
          });
          // Set up Uploadify
          current_frag.find('.file_upload_uploadify').each(function() {
            var element = $(this);
            element.uploadify({
              'uploader' : '/flash/uploadify.swf',
              'script' : '/media',
              'scriptData' : {
                'content_id' : element.data('content_id'),
                'member_id' : element.data('member_id'),
                'key' : element.data('key'),
              },
              'cancelImg' : '/images/cancel.png',
              'folder' : '/uploads',
              'multi' : true,
              'auto' : true,
              'fileDataName' : 'file_data',
              'removeCompleted' : true,
              'onComplete' : function(event, id, fileObj, response, data) {
                console.log(event, id, fileObj, response, data);
                var form = $(event.target).parents('form');
                // Boom_load event triggers refresh or media listing
                $(event.target).parents('ul.media_files').trigger('boom_load');
              }
            });
          });
          // Uploadify end
          return false;
        },
        'closed' : function(event, from_history) {
          if(!from_history) {
            var history_state = boom.frags.getHistoryState();
            console.log('history.saveState', history_state);
            boom.util.history.saveState(history_state);
          }
          return false;
        }
      },
      live : {
        // Any live events need to be set here
        // Define events by selector then by eventType
        '.disabled_filter' : {
          'click' : function(event) {
            // Don't process any events on elements with class "disabled_filter"
            event.stopImmediatePropagation();
            return false;
          }
        },
        '*[data-confirm]' : {
          'click' : function(event) {
            // Any elements with data-confirm need to display the confirm modal popup
            console.log('a[data-confirm] click');
            var link = $(this);
            if(link.data('confirmed')) {
              link.removeData('confirmed');
              // The link may not be removed & when clicked again will skip modal if we don't remove this
              return true;
              // Continue
            }
            // Add modal_confirm to queue
            boom.util.modal_queue.add(boom.frags.templates.modal_confirm(link.data(), link));
            event.stopImmediatePropagation();
            return false;
          }
        },
        'a.link_new_popup' : {
          'click' : function() {
            console.log('a.link_new_popup click');
            var link = $(this);
            var frag_href = $(this).data('frag');
            if(frag_href) {
              $.get(frag_href, function(data, status, res) {
                boom.util.modal_queue.add(boom.frags.templates.modal_data(link.attr('title'), data));
              });
              return false;
            }
            return true;
          }
        },
        'a.link_new_frag' : {
          'click' : function() {
            console.log('a.link_new_frag click');
            var frag_href = $(this).data('frag');
            if(frag_href) {
              boom.frags.create(this, frag_href);
              return false;
            }
            return true;
          },
        },
        'a.link_update_frag' : {
          'click' : function() {
            console.log('a.link_refresh click');
            var frag_href = $(this).data('frag') || undefined;
            boom.frags.update(this, frag_href);
            return false;
          }
        },
        'a.link_remove_frag' : {
          'click' : function() {
            console.log('a.link_remove click');
            boom.frags.remove(this);
            return false;
          }
        },
        'input[type="submit"][name]' : {
          'click' : function() {
            console.log('input[type="submit"][name] submit')
            var submit_button = $(this);
            $(this).parents('form').data('json-submit-field', submit_button);
            return true;
          }
        },
        'form.search[method="get"]' : {
          'submit' : function() {
            console.log('form.search[method="get"] submit');
            var form = $(this);
            var frag_href = form.data('frag');
            boom.frags.create(form, frag_href + '?' + form.serialize());
            event.stopImmediatePropagation();
            return false;
          }
        },
        'form[method="post"]' : {
          'submit' : function() {
            // Form submit events, will submit normally if no data-json defined
            console.log('form[method="post"] submit');
            var form = $(this);
            boom.util.tinymce.save(form);
            var json_href = form.data('json');
            if(json_href) {
              // If data-json defined, ajax submit to data-json
              var data = form.serializeArray();
              var data_submit_field = form.data('json-submit-field');
              if(data_submit_field && data_submit_field.attr('name') && data_submit_field.attr('value')) {
                data.push({
                  name : data_submit_field.attr('name'),
                  value : data_submit_field.val()
                });
                form.removeData('json-submit-field');
              }
              // if (form.data)
              $.post(json_href, data, function(res, status, req) {
                boom.util.flash_message.show(res);
                if(res.status == 'ok') {
                  console.log(form.data());
                  var json_complete = ( data_submit_field ? data_submit_field.data('json-complete') : false) || form.data('json-complete');
                  if(json_complete) {
                    // data-json_complete contains a json array of actions to complete
                    // e.g.
                    //    "[ ['update',null,'/contents/10.frag'], ['update',['/contents/10','contents/8']] ]"
                    //       update    current frag, with new url. update, frags with these urls, no new url so refresh
                    // Actions are always arrays, first parameter is the method (boom.frags.*) second can be null if the current form is to be passed, the rest are passed with no processing.
                    // THIS MEANS: If you just pass a method, it must be in an array, and the method will have the current form passed as first parameter
                    // Also: update and create have a magical 2nd parameter, if you pass a url containing "{json_id}" e.g. "/contents/{json_id}/edit.frag" {json_id} will be replaced with the value of result.data.id
                    console.log('Running json-complete', json_complete)
                    if( typeof json_complete == 'string') {
                      json_complete = JSON.parse(json_complete.replace(/\'/g, '\"'));
                    }
                    for(var i = 0; i < json_complete.length; i++) {
                      var params = json_complete[i];
                      var func = params.shift();
                      if( func in boom.frags) {
                        params[0] = params[0] || form;
                        if((func == 'update' || func == 'create') && typeof params[1] == 'string') {
                          params[1] = params[1].replace(/((\%7b)|\{)json_id((\%7d)|\})/i, (res.data || {}).id);
                        }
                        if(func == 'update' && params[2] === null)
                          params[2] = form;
                        boom.frags[func].apply(this, params);
                        console.log('json-complete function', func, params);
                      }
                    }
                  }
                }
              }, 'json').error(function(req) {
                if(req.status == 403)
                  form.removeClass('link_secure').submit();
              });
              return false;
            }
            console.log('returning true');
            return true;
          }
        },
        'a.link_secure' : {
          'click' : function() {
            var link = $(this);
            var container = link.parents('.secure_link');
            console.log('a.link_secure click');
            //var data = link.data();
            //if (data.confirm_text && !confirm(data.confirm_text)) return false;
            // MODAL POPUP HERE!
            // var popup = container.find('.popup-modal');
            // console.log(popup, link.parent('.secure_link'));
            // if (popup.length > 0 && link.parent('.secure_link').length > 0) {
            // // If there is a popup defined and the link clicked is not in the popup (has direct secure_link parent)
            // // Show modal popup
            // popup.modal({appendTo: container});
            // return false;
            // }
            // FIXME: BROKEN?: WHY ARE WE NOT USING JQUERIES FX?!
            link.addClass('disabled_filter');
            boom.frags.setTimeout(link, 'disabled_filter', true, function() {
              link.removeClass('disabled_filter')
            }, 1000);
            // var t = setTimeout(function(){link.removeClass('disabled_filter'); boom.frags.deleteTimer(link, 't_disabled_filter_'+t)}, 1000);
            // boom.frags.setTimer(link, 't_disabled_filter_'+t, t);
            var form = container.find('form');
            if(form.attr('onsubmit')) {
              form.onsubmit();
            } else {
              //form.trigger('submit');
              form.submit();
            }
            return false;
          }
        },
        '.toggle_section' : {
          'click' : function() {
            boom.util.toggle_section(this);
            return false;
          }
        },
        // We can initialise jQuery UI elements here too on load
        '.jqui_accordion' : {
          'boom_load' : function() {
            console.log('.jqui_accordion boom_load');
            var element = $(this);
            var data = element.data('jqui_accordion');
            if( typeof data == 'string')
              data = JSON.parse(data);
            element.accordion(data);
            return false;
          },
          'boom_resize' : function() {
            var element = $(this);
            element.accordion('resize');
            return false;
          }
        },
        '.jqui_tabs' : {
          'boom_load' : function() {
            console.log('.jqui_tabs load');
            $(this).tabs();
            return false;
          }
        },
        '.jq_simplecolor' : {
          'boom_load' : function() {
            console.log('.jq_simplecolor');
            $(this).simpleColorPicker();
            return false;
          }
        },
        '.jqui-radios' : {
          'boom_load' : function() {
            console.log('.jqui-radios')
            $(this).buttonset().removeClass('.jqui-radios');
            return false;
          }
        },
        '.get_widget' : {
          'boom_load' : function() {
            // Not completed yet...
            return false;
          }
        },
        '.limit_length' : {
          'boom_load' : function() {
            var textarea = $(this);
            var countarea = textarea.siblings('.limit_length_remaining');
            textarea.limit(countarea.text(), countarea);
            return false;
          }
        },
        '.show-new-comments' : {
          'click' : function() {
            var link = $(this);
            var frag = boom.frags.getFragment(link);
            frag.find('.new-comment').first().toggle(function() {
              $(this).filter(':visible').find('.comment-ta').focus();
            });
            return false;
          }
        },
        '.content_rating' : {
          'boom_load' : function() {
            var rating_form = $(this);
            rating_form.children().not('select').hide();
            rating_form.stars({
              inputType : "select",
              callback : function(ui, type, value) {
                $.ajax({
                  url : rating_form.data('json'),
                  type : "POST",
                  data : rating_form.serialize(),
                  dataType : "json",
                  success : function(data) {
                    boom.util.flash_message.show(data);
                  },
                  error : function(XMLHttpRequest, textStatus, errorThrown) {
                    boom.util.flash_message.show(textStatus);
                  }
                });
              }
            });
            return false;
          }
        },
        'a.link_popup_next_element' : {
          'click' : function() {
            var link = $(this);
            var popup_content = link.next('.popup_element').children().clone(true, true);
            boom.util.modal_queue.add(boom.frags.templates.modal_data('', popup_content));
            return false;
          }
        },
        '.link_janrain' : {
          'boom_load' : function() {
            var link = $(this);
            var data = link.data();
            janrain_popup_share(data.janrainUrl, data.janrainOptions, data.janrainVariables);
            return false;
          },
          'click' : function() {
            var link = $(this);
            var data = link.data();
            janrain_popup_share(data.janrainUrl, data.janrainOptions, data.janrainVariables);
            return false;
          }
        },
        'img.placeholder_media' : {
          'error' : function() {
            alert('!');
            return false;
          }
        },
        'img.placeholder_member' : {
          'error' : function() {
            alert('!');
            return false;
          }
        }
      }
    },
    init : function() {
      // Initialise frags plugin for Civicboom
      // If boom_development not set, override console.log
      console.log('boom.frag.init');
      // boom.frags.container should be set to the element that will contain the frags
      if(boom.frags.container == null) {
        boom.frags.container = $('#frag_containers');
      }
      // Set up ajax error handler
      $(document).ajaxError(function(event, req, settings, exception) {
        console.log('ajaxError', event, req, settings, exception);
        // Try and get json response
        var jsob;
        try {
          jsob = $.parseJSON(req.responseText);
        } catch (e) {
          // json parse error, fudge response and show flash message
          if(req.status == 404) {
            boom.util.flash_message.show({
              message : 'The page you requested could not be found, it may have been removed or hidden.',
              status : 'error'
            });
          } else {
            boom.util.flash_message.show({
              message : 'A server error has occurred!',
              status : 'error'
            });
          }
        }
        // If json response ok
        if(jsob) {
          if( typeof jsob.message != 'undefined' && typeof jsob.data != 'undefined' && typeof jsob.data.invalid != 'undefined') {
            jsob.message = jsob.message + ' (';
            for(var i in jsob.data.invalid) {
              jsob.message = jsob.message + i + ': ' + jsob.data.invalid[i] + ', ';
            }
            jsob.message = jsob.message + ')';
          }
          boom.util.flash_message.show(jsob);
        }
        // If 402 payment required add upgrade popup to the modal queue! (horrible, I know, but better than the previous hack)
        if(req.status == 402) {
          var holder = $('<span />');
          holder.load('/misc/upgrade_popup.frag', function() {
            boom.util.modal_queue.add(boom.frags.templates.modal_data('Upgrade plans', holder));
          });
        }
      });
      // Initialise fragment events
      for(var eventType in boom.frags.events.frag) {
        console.log('registering frag event:', eventType);
        $('.' + boom.frags.classes.container).live('frag_' + eventType, boom.frags.events.frag[eventType]);
      }
      // Initialise live events
      for(var selector in boom.frags.events.live) {
        for(var eventType in boom.frags.events.live[selector]) {
          console.log('registering event:', selector, eventType);
          $(selector).live(eventType, boom.frags.events.live[selector][eventType]);
        }
      }
      // Initialise any static events
      $(window).resize(function() {
        console.log('window resized');
        $('.event_resize').trigger('boom_resize');
        return false;
      });
      // Trigger manual boom_load event for non frag elements
      $(function () {
        $('.event_load').not('.' + boom.frags.classes.container + ' *').trigger('boom_load');
      });

      // Trigger manual frag_load_static for each fragment.
      $('.' + boom.frags.classes.container).trigger('frag_load_static');
    },
    getFragment : function(element) {
      // Get fragment in which this element exists, or if element is fragment, return itself
      // Also checks & converts current element if not a jquery object
      element = boom.util.convert_jquery(element);
      // element = (element.jquery) ? element : $(element);
      return element.hasClass(boom.frags.classes.container) ? element : element.parents('.' + boom.frags.classes.container);
    },
    getFragmentData : function(element) {
      element = boom.frags.getFragment(element);
      return element.children('.' + boom.frags.classes.data).data()
    },
    setAutoSave : function(form) {
      // Setup auto save for form
      console.log('setAutoSave', form);
      form = boom.util.convert_jquery(form);
      boom.frags.setInterval(form, 'auto_save', false, function() {
        boom.util.tinymce.save(form);
        var data = form.find('.auto_save:input,[name="_authentication_token"]:input,[name="_method"]:input').serialize();
        $.ajax({
          type : 'POST',
          dataType : 'json',
          url : form.data('json'),
          data : data,
          success : function(data) {
            boom.util.flash_message.show(data);
          },
          error : function(data) {
            boom.util.flash_message.show({
              status : 'error',
              message : 'Error automatically saving your content'
            });
          }
        });
      }, boom.frags.vars.auto_save_time);
    },
    setTimeout : function(element, name, dup_allowed, func, time) {
      var t;
      name = 't_' + name;
      // If not dup_allowed check timer exists and return false if it does!
      if(!dup_allowed && (boom.frags.getFragment(element).data('timers') || {})[name])
        return false;
      var wrapped_func = function() {
        func();
        boom.frags.deleteTimer(element, name);
      }
      t = setTimeout(wrapped_func, time);
      name = name + ((dup_allowed) ? ('_' + t) : '');
      boom.frags.setTimer(element, name, t);
      return name;
    },
    setInterval : function(element, name, dup_allowed, func, time) {
      var t;
      name = 'i_' + name;
      if(!dup_allowed && (boom.frags.getFragment(element).data('timers') || {})[name])
        return false;
      t = setInterval(func, time);
      name = name + ((dup_allowed) ? ('_' + t) : '');
      boom.frags.setTimer(element, name, t);
      return name;
    },
    setTimer : function(element, name, timer) {
      // Set a timer on this elements fragment
      element = boom.frags.getFragment(element);
      if(element.length == 0)
        element = $('body');
      if(!element.data('timers'))
        element.data('timers', {});
      element.data('timers')[name] = timer;
    },
    deleteTimer : function(element, name, clear) {
      // Removes a timer (reference only!) from a fragment
      element = boom.frags.getFragment(element);
      if(element.length == 0)
        element = $('body');
      var timers = element.data('timers');
      if(!timers || !timers[name])
        return;
      if(clear)
        switch (name.charAt (0)) {
          case 'i':
            clearInterval(timers[name]);
            break;
          case 't':
            clearTimeout(timers[name]);
            break;
        }
      delete element.data('timers')[name];
    },
    clearTimers : function(element) {
      element = boom.frags.getFragment(element);
      if(element.length == 0)
        element = $('body');
      var timers = element.data('timers');
      if(timers) {
        for(var key in timers) {
          switch (key.charAt(0)) {
            case 'i':
              clearInterval(timers[key]);
              break;
            case 't':
              clearTimeout(timers[key]);
              break;
          }
          delete timers[key];
        }
      }
    },
    create : function(element, new_url, list_type, from_history, callback) {
      // Creates a new fragment
      // Params:
      // element String element of or in current fragment (loads after current)
      // new_url String url to load into new fragment (can be undefined if element is an anchor element)
      // list_type String additional class to add to frag container
      // from_history Boolean skip adding to history
      // callback Function called back with success boolean as only parameter
      var url = new_url || $(element).attr('href');

      var current_frag = boom.frags.getFragment(element);
      var frag_loading = $('<div></div>').attr('id', boom.frags.prefix + (boom.frags.counter++)).addClass(boom.frags.classes.container).addClass(list_type || '').append(boom.frags.templates.loading_holder());

      if(current_frag.length > 0) {
        current_frag.after(frag_loading);
      } else {
        boom.frags.container.prepend(frag_loading)
      }

      // FIXME: Scrolling
      $(window)._scrollable().scrollTo(frag_loading, {
        duration : boom.frags.vars.scroll_duration
      });
      boom.frags.update(frag_loading, url, undefined, function(success) {
        if(success) {
          // frag_load event is triggered by update above! No need for it here...
          // TODO: Tweak animation!
          frag_loading.fadeTo(0, 0.01);
          frag_loading.animate({
            opacity : 1.0
          }, boom.frags.vars.scroll_duration, function() {
            frag_loading.removeAttr('style');
          });
          if(!from_history)
            boom.frags.remove_after(frag_loading, function() {
              // FIXME: rewrite history
              //if (!from_history) boom.frags.update_history();
            });
        } else {
          frag_loading.remove();
        }
        if( typeof callback != 'undefined')
          callback(success, frag_loading);
        // Callback with loaded frag to make chaining easier
      }, from_history);
      return frag_loading;
      // Return frag_loading as we don't have a success here!
    },
    update : function(element_hrefselector, url, exclude, callback, from_history) {
      // Updates a frag or set of frags
      // Params:
      // element_hrefselector jQuery/Array/String jQuery object of element(s) to update, array of strings to search anchor hrefs for and update parent fragments, a string to search for as before.
      // url String url to load into found frag(s), can be undefined in which case will reload frag's current content.
      // callback Function callback after all fragments updated with overall success as parameter
      // exclude jQuery jQuery object to exclude element(s) from
      if( typeof element_hrefselector == 'string') {
        element_hrefselector = [element_hrefselector];
        // We iterate over anyways to save repeated code
      }
      if($.isArray(element_hrefselector)) {
        var elements = $([]);
        for(var i = 0; i < element_hrefselector.length; i++) {
          if(!element_hrefselector[i])
            continue;
          // Skip any blank selector hrefs (content with no parent!)
          elements = elements.add($('a[href*="' + element_hrefselector[i] + '"]'));
        }
        element_hrefselector = elements.parents('.' + boom.frags.classes.container);
      } else {
        element_hrefselector = boom.frags.getFragment(element_hrefselector);
      }
      if(exclude) {
        exclude = exclude.hasClass(boom.frags.classes.container) ? exclude : exclude.parents('.' + boom.frags.classes.container);
        element_hrefselector = element_hrefselector.not(exclude);
      }
      // element_hrefselector = element_hrefselector.not(exclude)
      var success = true;
      var refreshed_elements = $([]);
      element_hrefselector.each(function(index, element) {
        element = $(element);
        var current_frag = element.hasClass(boom.frags.classes.container) ? element : element.parents('.' + boom.frags.classes.container);
        boom.frags.clearTimers(current_frag);
        // Clear any timers!
        var _url = url || current_frag.find('.' + boom.frags.classes.data).data('frag_url');
        // frag_data div has data-frag_url
        //var _url = url || current_frag.find('.'+boom.frags.classes.source).attr('href');
        current_frag.load(_url, function(res, status, req) {
          //var success = false;
          if(req.status == 200) {
            success = success && true;
            refreshed_elements.add(current_frag);
            current_frag.trigger('frag_load', [from_history]);
          } else {
            success = false;
          }
          if(index == element_hrefselector.length - 1)
            if( typeof callback != 'undefined')
              callback(success, refreshed_elements);
        });
      });
      return element_hrefselector;
    },
    remove : function(element, callback, from_history, ignore_after) {
      // Removes fragments
      // Params:
      // element jQuery jQuery element to remove (parent if not frag_container)
      // callback Function called on success with success as parameter
      // from_history Boolean stops from updating history
      // ignore_after Boolean do not run remove_after on frag (used by remove_after!)
      //element = $(element);
      var current_frag = boom.frags.getFragment(element);
      var callback_done = false;
      var function_done = false;
      var callback_return = true;
      boom.frags.clearTimers(current_frag);
      // if (current_frag.data('auto_save_timer') != 'undefined') {
      // clearInterval(current_frag.data('auto_save_timer'));
      // current_frag.removeData('auto_save_timer');
      // }

      var callback_after = function(success) {
        if(callback) {
          // run callback after this and next frags are removed
          callback();
        } else {
          current_frag.trigger('frag_closed', [from_history]);
          if(boom.frags.container.children().length == 0 && boom.frags.vars.default_frags) {
            // If we have a callback then we're probably in the middle of multiple frags being removed
            // Therefore if there is no callback and all frags have been removed, load default frags!
            var default_frags = boom.frags.vars.default_frags.slice(0);
            // Create a copy of default frags array
            var next_frag = function(success, loaded_frag) {
              // Recursive function lshifts next frag from array, loads and recurs
              if(success && default_frags.length) {
                boom.frags.create(loaded_frag, default_frags.shift(), undefined, undefined, next_frag)
              }
            }
            next_frag(true, $('body'));
            // Begin the chain of default frag loading
          }
        }
      }
      // Remove current frag
      current_frag.hide(boom.frags.vars.scroll_duration, function() {
        current_frag.remove();
        if(callback_done && !function_done)
          callback_after(true);
        function_done = true;
        // FIXME: rewrite history
        //if (!from_history) boom.frags.update_history();
      });
      // Remove next frag
      if(!ignore_after)
        boom.frags.remove_after(current_frag, function() {
          if(function_done && !callback_done)
            callback_after(true);
          callback_done = true;
        });
      // Close any modal windows
      $.modal.close();
      return false;
    },
    remove_after : function(element, callback) {
      // Removes all fragments after element's fragment
      // Params:
      // element jQuery element to remove frags from after.
      // callback Function called when all fragments closed
      element = boom.frags.getFragment(element);
      var next_frag = element.next('.' + boom.frags.classes.container);
      if(next_frag.length > 0) {
        boom.frags.remove(next_frag, function(success) {
          if( typeof callback != 'undefined')
            callback(success);
        });
      } else {
        if( typeof callback != 'undefined')
          callback(true);
      }
      return false;
    },
    close_modal : function() {
      $.modal.close();
    },
    getHistoryState : function() {
      var frags = boom.frags.container.children();
      var frags = frags.not(frags.children('.frag_ignore_history').parent());

      var frags = boom.frags.container.children().not(':has(.frag_ignore_history)');

      var fragStateArray = [];
      frags.each(function() {
        var frag_container = $(this);
        var frag_data = frag_container.children('.frag_data');
        fragStateArray.push({
          html_url : frag_data.data('html_url'),
          frag_url : frag_data.data('frag_url'),
        });
      });
      var current_url = frags.not(':has(.frag_ignore_url)').last().children('.frag_data').data('html_url');
      return {
        frags : fragStateArray,
        current_url : current_url,
      }
    },
    restoreHistoryState : function(state_object) {
      console.log('restoreHistoryState', state_object);
      var frags = boom.frags.container.children();
      var state_frags = state_object.frags.slice(0);
      // Take a copy of state_object.frags

      var load_next = function(success, prev_frag) {
        if(success && state_frags.length) {
          var state_frag = state_frags.shift();
          boom.frags.create(prev_frag, state_frag.frag_url, undefined, true, load_next);
        }
      }
      var i = 0;
      var loading_after = false;
      while(state_frags.length > 0) {
        var frag = frags.eq(i++);
        var state_frag = state_frags.shift();
        if(frag.length == 1) {
          if(frag.children('.frag_data').data('frag_url') != state_frag.frag_url)
            boom.frags.update(frag, state_frag.frag_url, undefined, undefined, true);
        } else {
          state_frags.unshift(state_frag);
          load_next(true, frags.last());
          loading_after = true;
          break;
        }
      }
      if(!loading_after && frags.eq(i).length)
        boom.frags.remove(frags.eq(i), undefined, true);
    }
  }
  // Initialise boom.frags
  $(boom.frags.init);
  window.onpopstate = function(event) {
    if(event.state) {
      boom.frags.restoreHistoryState(event.state);
    }
  }
}

// function createStateObj() {
// return;
// var stateObj = { 'blocks': []};
// $('.'+fragment_container_class).not('.'+fragment_help_class).each (function (index, element)
// {
// var s_url = $(element).find('.'+fragment_source_class).first().attr('href');
// stateObj.blocks[index] = {'url'  : s_url,
// 'classes': $(element).attr('class')
// };
// });
// return stateObj;
// }
//
// function loadStateObj(stateObj) {
// return;
// var frag_previous;
// if(stateObj !== null) {
// if (typeof stateObj.blocks == 'undefined') return;
//
// var i = 0;
//
// function load() {
// if (i < stateObj.blocks.length) {
// var frag_source = frag_previous.find('.'+fragment_source_class).first();
// var stat_href = stateObj.blocks[i].url;
// frag_previous = cb_frag(frag_source, stat_href, undefined, true, load); //$($('.'+fragment_container_class)[i-1]).find('.'+fragment_source_class)
// i ++;
// } else {
// cb_frag_remove_sibblings($($('.'+fragment_container_class)[stateObj.blocks.length-1]), undefined, true);
// return;
// }
// }
//
// for (i = 0; i < stateObj.blocks.length; i++) {
// var frag_exists = typeof $('.'+fragment_container_class)[i] != 'undefined';
// var frag_container = $($('.'+fragment_container_class)[i]);
// var frag_source = frag_container.find('.'+fragment_source_class);
// var frag_href = frag_source.attr('href');
// var stat_href = stateObj.blocks[i].url;
// if (!frag_exists) {
// load ();
// //frag_container = cb_frag(frag_previous.find('.'+fragment_source_class).first(), stat_href, undefined, true, waiter); //$($('.'+fragment_container_class)[i-1]).find('.'+fragment_source_class)
// break;
// } else if (frag_href != stat_href) {
// frag_container.removeClass().addClass(stateObj.blocks[i].classes);
// frag_container.find('.'+fragment_source_class).first().attr('href', stat_href);
// cb_frag_reload (frag_container);
// }
// frag_previous = frag_container;
// }
// if (i = (stateObj.blocks.length - 1))
// cb_frag_remove_sibblings($($('.'+fragment_container_class)[stateObj.blocks.length-1]), undefined, true);
// }
// }
//
// function update_history(url, replace) {
// return;
// if (typeof url == 'undefined' || url == null)
// var url = $('.'+fragment_container_class).not('.'+fragment_help_class).last().find('.'+fragment_source_class).first().attr('href');
// if (typeof url == 'undefined' || url == null)
// return;
// // update the URL bar to point at the latest block, and
// // store previous blocks in the history state object
// if(Modernizr.history) {
// // Note: this object is limited to 640k (which ought to be
// // enough for anyone) when saved in the browser history file
// if (replace) {
// history.replaceState(createStateObj(), "Civicboom", url.replace("?format=frag", "").replace(".frag", ""));
// } else {
// history.pushState(createStateObj(), "Civicboom", url.replace("?format=frag", "").replace(".frag", ""));
// }
// } else {
// // if (replace) {
// // if (location.hash.substr(1,3) != 'cbh') {
// // location.replace('#cbh' + encode64($.JSON.encode(createStateObj())));
// // } else {
// // $(window).hashchange();
// // }
// // } else {
// // location.hash = '#cbh' + encode64($.JSON.encode(createStateObj()));
// // }
// }
// }
//
// $(function () {
// return;
// if(Modernizr.history) {
// // Browser supports HTML5 history states
// // FIXME: jQuery-ise this, rather than using the raw window.blah
// window.onpopstate = function(popstate) { loadStateObj(popstate.state); }
// } else if(Modernizr.hashchange) {
// // Browser does not support HTML5 history states
// // Use url hash instead
// // GregM: Causing stability issues in IE, removed for now
// // $(window).hashchange(function (e) {
// //   var hash = location.hash;
// //   if (hash != '' && typeof hash != 'undefined') {
// //     if (hash.substr(1,3) == 'cbh') {
// //       try {
// //         var stateObj = $.parseJSON(decode64(hash.substr(4)));
// //         loadStateObj(stateObj);
// //       } catch (e) {}
// //     }
// //   }
// // });
// }
// update_history(location.href, true);
// })