if (!('boom' in window))
  boom = {};

/* Civicboom Utilities
 * These are mostly used internally by the Civicboom Frags system.
 * boom.util.*
 */
if (!('util' in boom)) {
  boom.util = {
    /*
     * If given object is jquery, return it, else convert it to jquery.
     */
    convert_jquery: function (element) {
      return (element.jquery) ? element : $(element);
    },
    /*
     * Toggles the visibility of the next element.
     */
    toggle_section: function (element) {
      element = boom.util.convert_jquery(element);
      element.next().slideToggle();
      var icon = element.find('.icon');
      var icon_more = 'icon_plus';
      var icon_less = 'icon_down';
      
      if (icon.hasClass(icon_more)) {
          icon.removeClass(icon_more);
          icon.addClass(icon_less);
      }
      else if (icon.hasClass(icon_less)) {
          icon.removeClass(icon_less);
          icon.addClass(icon_more);
      }
    },
    /*
     * TinyMCE utilities
     * boom.util.tinymce.*
     */
    tinymce: {
      /*
       * Initialise all tinymce (.editor) components within element
       */
      init: function (element) {
        element = boom.util.convert_jquery(element);
        element.find('.editor').tinymce({
          script_url: '/javascript/tiny_mce/tiny_mce.js',
          theme    : 'advanced',
          mode     : 'exact',
          theme_advanced_buttons1 : 'bold,italic,underline,separator,strikethrough,justifyleft,justifycenter,justifyright,justifyfull,bullist,numlist,link,unlink',
          theme_advanced_buttons2 : '',
          theme_advanced_buttons3 : '',
          theme_advanced_toolbar_location : 'top',
          theme_advanced_toolbar_align    : 'left',
        });
      },
      /*
       * Save all tinymce (.editor) components within element
       */
      save: function (element) {
        element = boom.util.convert_jquery(element);
        var tmce = element.find('.editor').tinymce();
        if (tmce && tmce.save) return tmce.save();
      }
    },
    /*
     * Modal Queue Utility
     * boom.util.modal_queue.*
     */
    modal_queue: {
      /*
       * Add content to the modal queue, ready to display at the next available opportunity
       */
      add: function (content, onClose) {
        $('body')
          .delay(0) // Needed to trigger the queue
          .queue(function (next) {
            // Queue the modal, onClose trigger next queue item
            var body = $(this);
            $.modal(content, {
              onClose: function () {
                if (onClose) onClose();
                $.modal.close();
                next();
              },
              onShow: function () {
                $.modal.update();
                // this.d.data.find('.event_load').each(function() {
                  // var evented = $(this);
                  // console.log(evented, evented.length);
                  // evented.trigger('boom_load');
                // })
                this.d.data.find('.event_load').trigger('boom_load');
              }
            })
          })
          .delay(100); // Next queue item always 100ms delay between popups
      },
      /*
       * Clear the modal queue
       */
      clear: function () {
        $('body').clearQueue('modal');
      }
    },
    /*
     * Display a Civicboom flash message, takes either a string message or an object returned from the api
     */
    flash_message: function(json_message) {
      if (typeof json_message == "string")
        json_message = {status:'ok', message: json_message};
      if (json_message && typeof json_message.message == 'string' && json_message) {
        $('#flash_message')
          .removeClass('status_error status_ok')
          .addClass('status_'+json_message.status)
          .text(json_message.message)
          .fadeIn('slow')
          .delay(5000)
          .fadeOut('slow')
          .mouseover(function () {
            $(this).stop(true).fadeOut('fast');
          });
      }
    },
    history: {
      saveState: function (stateObject, url, replace) {
        if(Modernizr.history) {
          // Note: this object is limited to 640k (which ought to be
          // enough for anyone) when saved in the browser history file
          if (replace) {
            history.replaceState(stateObject, "Civicboom", url);
          } else {
            history.pushState(stateObject, "Civicboom", url);
          }
        } else {
          
        }
      }
    }
  }
}
/*
 * Civicboom Fragment System
 * Use the following for most of your fragment work, there are loads of events available to use!
 * boom.frags.*
 */
if (!('frags' in boom)) {
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
    vars: {
      auto_save_time: 60000,
      scroll_duration: 600,
      default_frags: ['/profile.frag', '/misc/featured.frag'],
    },
    /*
     * Templates take varying arguments and return a jquery element containing dom elements that are not within the document.
     */
    templates: {
      /*
       * Returns the default frag loading placeholder
       */
      loading_holder: function () {
        return $(''+
        // Loading placeholder holder for frags
        '    <div class="frag_bars">'+
        '        <div class="title_bar"></div>'+
        '        <div class="action_bar"></div>'+
        '        <div style="clear: both;"></div>'+
        '    </div>'+
        '    <div class="frag_data frag_content" style="overflow-y: hidden;">'+
        '   <table style="height: 100%; text-align: center; margin: auto;"><tbody><tr><td>'+
        '     Loading'+
        '     <br>&nbsp;<br><img src="/images/ajax-loader.gif">'+
        '   </td></tr></tbody></table>'+
        ' </div>');
      },
      /*
       * Returns modal popup content with added title, message, and confirm_type class
       */
      modal_data: function (title, message, confirm_type) {
        return $('<div />').addClass('popup-modal').append(
          $('<div />').addClass(confirm_type || 'information')
          .append(
            $('<div />').addClass('popup-title')
            .append(title)
          )
          .append(
            $('<div />').addClass('popup-message')
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
       */
      modal_confirm: function (settings, originalLink) {
        if (typeof settings == 'string')
          settings = JSON.parse(settings.replace(/\'/g, '\"'));
        // Return modal content as jQuery object
        // Popup jQuery, begin with outer layer, work in. popup-modal:
        return $('<div />').addClass('popup-modal').append(
          // popup_content
          $('<div />').addClass('popup_content').append(
            // information/alert/etc.
            $('<div />').addClass(settings.confirmType || 'information')
            .append(
              // popup-title
              $('<div />').addClass('popup-title')
                // If confirm-avatar copy avatar from top right of site & re-style
                .append(
                  settings.confirmAvatar ?
                    $('<div />').addClass('popup-persona').append($('#persona_avatar').children('img').clone()).append($('#persona_details').clone().text())
//                    $('#persona_holder').clone().attr('id','').addClass('popup-persona')
                  :
                    ''
                )
                // If icon set icon else take icon name from link clicked
                .append(
                  settings.icon ? 
                    $('<span />').addClass('icon32').addClass('i_'+settings.icon)
                  :
                    originalLink.children('.icon32, .icon16').first().clone(false).removeClass('icon16').addClass('icon32')
                )
                // If confirm-title set it as the title, otherwise use the original link's text
                .append(settings.confirmTitle || originalLink.text() || '')
            )
            .append(
              // popup-message
              $('<div />').addClass('popup-message')
                .append(settings.confirm || '')
            )
            .append(
              // popup-actions
              $('<div />').addClass('popup-actions').append(
                // buttons
                $('<a />').addClass('button')
                  .data('original', originalLink)
                  .html(settings.confirmYes || 'Yes')
                  .click(function () {
                    var link = $(this);
                    console.log('click', this, link);
                    var original = link.data('original');
                    original.data('confirmed', 'true');
                    original.click();
                    $.modal.close();
                  }).after(
                    $('<a />').addClass('button').html(settings.confirmNo || 'No').click($.modal.close)
                  )
              )
            )
          )
        );
      }
    },
    // Frag counter (ensures frags are unique)
    counter: 0,
    // frags_loading: [],
    // frags_remove: [],
    /*
     * Events
     * The Fragment system fires events to allow code to run when things happen.
     * Events are split into two categories:
     * "frag" events:
     *    load:         triggered when a frag loads dynamically.
     *    load_static:  triggered when a frag loads dynamically or statically.
     * "live" events:
     *    These trigger based on selector and event type. e.g.
     *  {'a': {
     *   'click': function () {
     *     // Triggered on clicking a link
     *   }
     *  }}
     */
    events: {
      frag: {
        'load': function () {
          var current_frag = $(this);
          console.log('frag_load', this);
          // Push current frag's url to google tracker
          _gaq.push(['_trackPageview', current_frag.find('.'+boom.frags.classes.data).data('frag_url')]);
          boom.frags.events.frag.load_static.apply(this, arguments);
        },
        'load_static': function () {
          var current_frag = $(this);
          console.log('frag_load_static', this);
          // Trigger any load events for event_load elements
          current_frag.find('.event_load').trigger('load');
          // TinyMCE
          boom.util.tinymce.init(current_frag);
          // html5ize new fragment (datetime boxes etc.)
          html5ize(current_frag);
          // convert yes/no dropdowns to checkboxes
          $(convertYesNoCheckbox);
          // Set up auto save
          current_frag.find('form.auto_save').each(function() {
            boom.frags.setAutoSave(this);
          });
          // Set up Uploadify
          current_frag.find('.file_upload_uploadify').each(function() {
            var element = $(this);
            element.uploadify({
              'uploader'   : '/flash/uploadify.swf',
              'script'     : '/media',
              'scriptData' : {
                'content_id': element.data('content_id'),
                'member_id' : element.data('member_id'),
                'key'       : element.data('key'),
              },
              'cancelImg'  : '/images/cancel.png',
              'folder'     : '/uploads',
              'multi'      : true,
              'auto'       : true,
              'fileDataName':'file_data',
              'removeCompleted' : false,
              'onComplete' : function(event, id, fileObj, response, data) {
                //refreshProgress
              }
            });
          });
          // Uploadify end
        }
      },
      live: {
        // Any live events need to be set here
        // Define events by selector then by eventType
        '.disabled_filter': {
          'click': function (event) {
            // Don't process any events on elements with class "disabled_filter"
            event.stopImmediatePropagation();
            return false;
          }
        },
        '*[data-confirm]': {
          'click': function (event) {
            // Any elements with data-confirm need to display the confirm modal popup
            console.log('a[data-confirm] click');
            var link = $(this);
            if (link.data('confirmed')) {
              link.removeData('confirmed'); // The link may not be removed & when clicked again will skip modal if we don't remove this
              return true; // Continue
            }
            // Add modal_confirm to queue
            boom.util.modal_queue.add(
              boom.frags.templates.modal_confirm(link.data(), link)
            );
            event.stopImmediatePropagation();
            return false;
          }
        },
        'a.link_new_popup': {
          'click': function() {
            console.log('a.link_new_popup click');
            var link = $(this);
            var frag_href = $(this).data('frag');
            if (frag_href) {
              $.get(frag_href, function (data, status, res) {
                boom.util.modal_queue.add(
                  boom.frags.templates.modal_data(link.attr('title'),data)
                );
              });
              return false;
            }
            return true;
          }
        },
        'a.link_new_frag': {
          'click': function() {
            console.log('a.link_new_frag click');
            var frag_href = $(this).data('frag');
            if (frag_href) {
              boom.frags.create(this, frag_href);
              return false;
            }
            return true;
          },
        },
        'a.link_update_frag': {
          'click': function() {
            console.log('a.link_refresh click');
            var frag_href = $(this).data('frag') || undefined;
            boom.frags.update(this, frag_href);
            return false;
          }
        },
        'a.link_remove_frag': {
          'click': function() {
            console.log('a.link_remove click');
            boom.frags.remove(this);
            return false;
          }
        },
        'input[type="submit"][name]': {
          'click': function() {
            console.log('input[type="submit"][name] submit')
            var submit_button = $(this);
            $(this).parents('form').data('json-submit-field', submit_button);
            return true;
          }
        },
        'form.search[method="get"]': {
          'submit': function () {
            console.log('form.search[method="get"] submit');
            var form = $(this);
            var frag_href = form.data('frag');
            boom.frags.create(form, frag_href + '?' + form.serialize());
            event.stopImmediatePropagation();
            return false;
          }
        },
        'form[method="post"]': {
          'submit': function() {
            // Form submit events, will submit normally if no data-json defined
            console.log('form[method="post"] submit');
            var form = $(this);
            boom.util.tinymce.save(form);
            var json_href = form.data('json');
            if (json_href) {
              // If data-json defined, ajax submit to data-json
              var data = form.serializeArray();
              var data_submit_field = form.data('json-submit-field');
              if (data_submit_field && data_submit_field.attr('name') && data_submit_field.attr('value')) {
                data.push({
                  name: data_submit_field.attr('name'),
                  value: data_submit_field.val()
                });
                form.removeData('json-submit-field');
              }
              // if (form.data)
              $.post(
                json_href,
                data,
                function(res, status, req) {
                  boom.util.flash_message(res);
                  if (res.status == 'ok') {
                    console.log(form.data());
                    var json_complete = (data_submit_field ? data_submit_field.data('json-complete'):false) || form.data('json-complete');
                    if (json_complete) {
                      // data-json_complete contains a json array of actions to complete
                      // e.g.
                      //    "[ ['update',null,'/contents/10.frag'], ['update',['/contents/10','contents/8']] ]"
                      //       update    current frag, with new url. update, frags with these urls, no new url so refresh
                      // Actions are always arrays, first parameter is the method (boom.frags.*) second can be null if the current form is to be passed, the rest are passed with no processing.
                      // THIS MEANS: If you just pass a method, it must be in an array, and the method will have the current form passed as first parameter
                      // Also: update and create have a magical 2nd parameter, if you pass a url containing "{json_id}" e.g. "/contents/{json_id}/edit.frag" {json_id} will be replaced with the value of result.data.id
                      console.log('Running json-complete', json_complete)
                      if (typeof json_complete == 'string') {
                        json_complete = JSON.parse(json_complete.replace(/\'/g, '\"'));
                      }
                      for (var i = 0; i < json_complete.length; i++) {
                        var params = json_complete[i];
                        var func = params.shift();
                        if (func in boom.frags) {
                          params[0] = params[0] || form;
                          if ((func == 'update' || func == 'create') && typeof params[1] == 'string') {
                            params[1] = params[1].replace(/((\%7b)|\{)json_id((\%7d)|\})/i, (res.data || {}).id);
                          }
                          if (func == 'update' && params[2] === null)
                            params[2] = form;
                          boom.frags[func].apply(this, params);
                          console.log('json-complete function', func, params);
                        }
                      }
                    }
                  }
                },
                'json'
              ).error(function(req) {
                if (req.status == 403)
                  form.removeClass('link_secure').submit();
              });
              return false;
            }
            console.log('returning true');
            return true;
          }
        },
        'a.link_secure': {
          'click': function() {
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
            if (form.attr('onsubmit')) {
              form.onsubmit();
            } else {
              //form.trigger('submit');
              form.submit();
            }
            return false;
          }
        },
        '.toggle_section': {
          'click': function () {
            boom.util.toggle_section(this);
            return false;
          }
        },
        // We can initialise jQuery UI elements here too on load
        '.jqui_tabs': {
          'boom_load': function () {
            console.log('.jqui_tabs load');
            $(this).tabs();
            return false;
          }
        },
        '.jq_simplecolor': {
          'boom_load': function () {
            console.log('.jq_simplecolor');
            $(this).simpleColorPicker();
            return false;
          }
        },
        '.get_widget': {
          'boom_load': function () {
            // Not completed yet...
            return false;
          }
        }
      }
    },
    init: function () {
      // Initialise frags plugin for Civicboom
      // If boom_development not set, override console.log
      if (!('boom_development' in window) && console) console.log = function () {};
      console.log('boom.frag.init');
      // boom.frags.container should be set to the element that will contain the frags
      if (boom.frags.container == null) {
        boom.frags.container = $('#frag_containers');
      }
      // Set up ajax error handler
      $(document).ajaxError(function(event, req, settings, exception){
        console.log('ajaxError', event, req, settings, exception);
        // Try and get json response
        try {
          jsob = $.parseJSON(req.responseText);
        } catch (e) {
          // json parse error, fudge response and show flash message
          if (req.status == 404) {
            boom.util.flash_message({
              message: 'The page you requested could not be found, it may have been removed or hidden.',
              status: 'error'
            });
          } else {
            boom.util.flash_message({
              message: 'A server error has occurred!',
              status: 'error'
            });
          }
        }
        // If json response ok
        if (jsob) {
          if (typeof jsob.message != 'undefined' && typeof jsob.data != 'undefined' && typeof jsob.data.invalid != 'undefined') {
            jsob.message = jsob.message + ' (';
            for (var i in jsob.data.invalid) {
              jsob.message = jsob.message + i + ': ' + jsob.data.invalid[i] + ', ';
            }
            jsob.message = jsob.message + ')';
          }
          boom.util.flash_message(jsob);
        }
        // If 402 payment required add upgrade popup to the modal queue! (horrible, I know, but better than the previous hack)
        if (req.status == 402) {
          var holder = $('<span />');
          holder.load('/misc/upgrade_popup.frag', function () {
            boom.util.modal_queue.add(boom.frags.templates.modal_data('Upgrade plans', holder));
          });
        }
      });
      // Initialise fragment events
      for (var eventType in boom.frags.events.frag) {
        console.log (
          'registering frag event:', eventType
        );
       $('.'+boom.frags.classes.container).live('frag_'+eventType, boom.frags.events.frag[eventType]);
      }
      // Initialise live events
      for (var selector in boom.frags.events.live) {
        for (var eventType in boom.frags.events.live[selector]) {
          console.log (
            'registering event:', selector, eventType
          );
          $(selector).live(eventType, boom.frags.events.live[selector][eventType]);
        }
      }
      // Trigger manual frag_load_static for each fragment.
      $('.'+boom.frags.classes.container).trigger('frag_load_static');
    },
    getFragment: function (element) {
      // Get fragment in which this element exists, or if element is fragment, return itself
      // Also checks & converts current element if not a jquery object
      element = boom.util.convert_jquery(element);
      // element = (element.jquery) ? element : $(element);
      return element.hasClass(boom.frags.classes.container) ? element : element.parents('.'+boom.frags.classes.container);
    },
    setAutoSave: function (form) {
      // Setup auto save for form
      console.log('setAutoSave', form);
      form = boom.util.convert_jquery(form);
      boom.frags.setInterval(form, 'auto_save', false, function() {
        boom.util.tinymce.save(form);
        var data = form.find('.auto_save:input,[name="_authentication_token"]:input,[name="_method"]:input').serialize();
        $.ajax({
          type: 'POST',
          dataType: 'json',
          url: form.data('json'),
          data: data,
          success: function(data) {
            boom.util.flash_message(data);
          },
          error: function(data) {
            boom.util.flash_message({status:'error', message:'Error automatically saving your content'});
          }
        });
      }, boom.frags.vars.auto_save_time);
    },
    setTimeout: function (element, name, dup_allowed, func, time) {
      var t;
      name = 't_'+name;
      // If not dup_allowed check timer exists and return false if it does!
      if (!dup_allowed && (boom.frags.getFragment(element).data('timers') || {})[name])
        return false;
      var wrapped_func = function () {
        func();
        boom.frags.deleteTimer(element, name);
      }
      t = setTimeout(wrapped_func, time);
      name = name+((dup_allowed)?('_'+t):'');
      boom.frags.setTimer(element, name, t);
      return name;
    },
    setInterval: function (element, name, dup_allowed, func, time) {
      var t;
      name = 'i_'+name;
      if (!dup_allowed && (boom.frags.getFragment(element).data('timers') || {})[name])
        return false;
      t = setInterval(func, time);
      name = name+((dup_allowed)?('_'+t):'');
      boom.frags.setTimer(element, name, t);
      return name;
    },
    setTimer: function (element, name, timer) {
      // Set a timer on this elements fragment
      element = boom.frags.getFragment(element);
      if (element.length == 0)
        element = $('body');
      if (!element.data('timers'))
        element.data('timers', {});
      element.data('timers')[name] = timer;
    },
    deleteTimer: function (element, name, clear) {
      // Removes a timer (reference only!) from a fragment
      element = boom.frags.getFragment(element);
      if (element.length == 0)
        element = $('body');
      var timers = element.data('timers');
      if (!timers || !timers[name]) return;
      if (clear)
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
    clearTimers: function (element) {
      element = boom.frags.getFragment(element);
      if (element.length == 0)
        element = $('body');
      var timers = element.data('timers');
      if (timers) {
        for (var key in timers) {
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
    create: function (element, new_url, list_type, from_history, callback) {
      // Creates a new fragment
      // Params:
      // element String element of or in current fragment (loads after current)
      // new_url String url to load into new fragment (can be undefined if element is an anchor element)
      // list_type String additional class to add to frag container
      // from_history Boolean skip adding to history
      // callback Function called back with success boolean as only parameter
      var url = new_url || $(element).attr('href');
      
      var current_frag = boom.frags.getFragment(element);
      //_gaq.push(['_trackPageview', url]);
      var frag_loading = $('<div></div>')
          .attr('id', boom.frags.prefix + (boom.frags.counter++))
          .addClass(boom.frags.classes.container)
          .addClass(list_type || '')
          .append(boom.frags.templates.loading_holder());
      
      if (current_frag.length > 0) {
        current_frag.after(frag_loading);
      } else {
        boom.frags.container.prepend(frag_loading)
      }
      
      // FIXME: Scrolling
      $(window)._scrollable().scrollTo(frag_loading, {duration: boom.frags.vars.scroll_duration});
      boom.frags.update(frag_loading, url, undefined, function (success) {
        if (success) {
          // TODO: Tweak animation!
          frag_loading.fadeTo(0, 0.01);
          frag_loading.animate({opacity: 1.0}, boom.frags.vars.scroll_duration, function () {
            frag_loading.removeAttr('style');
          });
          if (!from_history) boom.frags.remove_after(frag_loading, function () {
            // FIXME: rewrite history
            //if (!from_history) boom.frags.update_history();
          });
        } else {
          frag_loading.remove();
        }
        if (typeof callback != 'undefined')
          callback(success, frag_loading); // Callback with loaded frag to make chaining easier
      });
      return frag_loading; // Return frag_loading as we don't have a success here!
    },
    update: function (element_hrefselector, url, exclude, callback) {
      // Updates a frag or set of frags
      // Params:
      // element_hrefselector jQuery/Array/String jQuery object of element(s) to update, array of strings to search anchor hrefs for and update parent fragments, a string to search for as before.
      // url String url to load into found frag(s), can be undefined in which case will reload frag's current content.
      // callback Function callback after all fragments updated with overall success as parameter
      // exclude jQuery jQuery object to exclude element(s) from
      if (typeof element_hrefselector == 'string') {
        element_hrefselector = [element_hrefselector]; // We iterate over anyways to save repeated code
      }
      if ($.isArray(element_hrefselector)) {
        var elements = $([]);
        for (var i = 0; i<element_hrefselector.length; i++) {
          if (!element_hrefselector[i]) continue; // Skip any blank selector hrefs (content with no parent!)
          elements = elements.add($('a[href*="'+element_hrefselector[i]+'"]'));
        }
        element_hrefselector = elements.parents('.'+boom.frags.classes.container);
      } else {
        element_hrefselector = boom.frags.getFragment(element_hrefselector);
      }
      if (exclude) {
        exclude = exclude.hasClass(boom.frags.classes.container) ? exclude : exclude.parents('.'+boom.frags.classes.container);
        element_hrefselector = element_hrefselector.not(exclude);
      }
      // element_hrefselector = element_hrefselector.not(exclude)
      var success = true;
      var refreshed_elements = $([]);
      element_hrefselector.each(function(index, element) {
        element = $(element);
        var current_frag = element.hasClass(boom.frags.classes.container) ? element : element.parents('.'+boom.frags.classes.container);
        boom.frags.clearTimers(current_frag); // Clear any timers!
        var _url = url || current_frag.find('.'+boom.frags.classes.data).data('frag_url'); // frag_data div has data-frag_url
        //var _url = url || current_frag.find('.'+boom.frags.classes.source).attr('href');
        current_frag.load(_url, function (res, status, req) {
          //var success = false;
          if (req.status == 200) {
            success = success && true;
            refreshed_elements.add(current_frag);
            current_frag.trigger('frag_load');
          } else {
            success = false;
          }
          if (index == element_hrefselector.length - 1)
            if (typeof callback != 'undefined')
              callback(success, refreshed_elements);
        });
      });
      return element_hrefselector;
    },
    remove: function (element, callback, from_history, ignore_after) {
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
      
      var callback_after = function (success) {
        if (callback) {
          // run callback after this and next frags are removed
          callback();
        } else if (boom.frags.container.children().length == 0 && boom.frags.vars.default_frags) {
          // If we have a callback then we're probably in the middle of multiple frags being removed
          // Therefore if there is no callback and all frags have been removed, load default frags!
          var default_frags = boom.frags.vars.default_frags.slice(0); // Create a copy of default frags array
          var next_frag = function (success, loaded_frag) {
            // Recursive function lshifts next frag from array, loads and recurs
            if (success && default_frags.length) {
              boom.frags.create(loaded_frag, default_frags.shift(), undefined, undefined, next_frag)
            }
          }
          next_frag(true, $('body')); // Begin the chain of default frag loading
        }
      }
      // Remove current frag
      current_frag.hide(boom.frags.vars.scroll_duration, function() {
        current_frag.remove();
        if (callback_done && !function_done)
          callback_after(true);
        function_done = true;
        // FIXME: rewrite history
        //if (!from_history) boom.frags.update_history();
      });
      // Remove next frag
      if (!ignore_after) boom.frags.remove_after(current_frag, function() {
        if (function_done && !callback_done)
          callback_after(true);
        callback_done = true;
      });
      // Close any modal windows
      $.modal.close();
      return false;
    },
    remove_after: function (element, callback) {
      // Removes all fragments after element's fragment
      // Params:
      // element jQuery element to remove frags from after.
      // callback Function called when all fragments closed
      element = boom.frags.getFragment(element);
      var next_frag = element.next('.'+boom.frags.classes.container);
      if (next_frag.length > 0) {
        boom.frags.remove(next_frag, function(success) {
          if (typeof callback != 'undefined') callback(success);
        });
      } else {
        if (typeof callback != 'undefined') callback(true);
      }
      return false;
    },
    close_modal: function () {
      $.modal.close();
    }
  }
  // Initialise boom.frags
  $(boom.frags.init);
}



//------------------------------------------------------------------------------
// Civicboom Fragment AJAX Mangment
//------------------------------------------------------------------------------

// Example: <a href="http://localhost:5000/test/frag" onclick="cb_frag($(this), 'http://localhost:5000/test/frag'); return false;">Link of AJAX</a>
/*
var frag_id_name                      = 'frag_';
var fragment_containers_id            = '#frag_containers';
var fragment_container_class          = 'frag_container';  // container for a full JSON object 500px
//var fragment_col_class                = 'frag_col_1';      // container for a bridge list 250px (half width)
var fragment_source_class             = 'frag_source';
var fragment_div_loading_placeholder  = ''+
'    <div class="frag_bars">'+
'        <div class="title_bar"></div>'+
'        <div class="action_bar"></div>'+
'        <div style="clear: both;"></div>'+
'    </div>'+
'    <div class="frag_data frag_content" style="overflow-y: hidden;">'+
'		<table style="height: 100%; text-align: center; margin: auto;"><tbody><tr><td>'+
'			Loading'+
'			<br>&nbsp;<br><img src="/images/ajax-loader.gif">'+
'		</td></tr></tbody></table>'+
'	</div>';
var fragment_help_class               = 'frag_help';
var scroll_duration = 600;

var frag_count      = 0;
var frag_loading    = null;
var frags_to_remove = null;

//------------------------------------------------------------------------------
//                               Create Frag
//------------------------------------------------------------------------------

// current_element = JQuery element object
// url             = String
function cb_frag(current_element, url, list_type, from_history, callback) {
    // Take the url from the current <A> element (hence the name url_a)
    var url_a = current_element.attr('href');
    
    if (url  ==undefined || url  ==null) {url = url_a;}
    if (url  ==undefined || url  ==null) {return;}
    
    // Set the class for this new fragment (bridge list or full container)
    var new_fragment_class = fragment_container_class;
    if (typeof list_type == 'string') {new_fragment_class += ' '+list_type}
    //if (list_type=='frag_col_1') {new_fragment_class += " "+fragment_col_class;}
    //else                         {}
    
    // Register this page view with Google analytics.
    // http://code.google.com/apis/analytics/docs/tracking/asyncMigrationExamples.html#VirtualPageviews
    _gaq.push(['_trackPageview', url_a]);

    // Get this parent fragment name
    var frag_div    = current_element.parents('.'+fragment_container_class) // go up the chain looking for '.frag' class to id the master parent
    var frag_div_id = frag_div.attr('id');
    
    // Generate new div name
    var frag_div_id_next = frag_id_name + frag_count++; //frag_div_id+'1'; // AllanC - I know this only appends one to the end, but it works
    
    // Create new div with loading placeholder
    frag_loading = $('<div id="'+frag_div_id_next+'" class="'+new_fragment_class+'">'+fragment_div_loading_placeholder+'</div>');
    frag_div.after(frag_loading); // Append new '.frag' div populated with with load placeholder data //$(fragment_containers_id).append 
    //frag_loading = $('#'+frag_div_id_next);
    
    // AllanC - Hack for IE7 Frag rendering
    //  1.) Make frag float:left
    //  2.) Calculate size of all divs in frag_container
    //  3.) Manually force the size of frag_container to fit all child divs
    // WHY did we bother! ... IE7 is TOTALLY broken ... we dont support it
    //if ($('html').hasClass('ie7')) {
    //    //frag_loading.attr('style', 'float:left;'); // A conditioal in CSS rule is now in place
    //    total_width = 0;
    //    $(fragment_containers_id).children().each(function(index, element) {
    //        element_width = document.defaultView.getComputedStyle(element, null).width
    //        element_width = parseInt(element_width.replace('px',''));
    //       element_width+= 5; //TODO fake border size, needs to be replaced by actual border/margin size
    //        total_width  += element_width;
    //    });
    //    $(fragment_containers_id).attr('style', 'width:'+total_width+'px;');
    //}
    
    // Start scrolling to new element
    // Scroll (smoothly)
    //  - http://plugins.jquery.com/project/ScrollTo
    //  - http://demos.flesler.com/jquery/scrollTo/
    $(window)._scrollable().scrollTo(frag_loading, {duration: scroll_duration}); //(fragment_containers_id)
    //$(window)._scrollable().scrollTo('100%',0, {duration: scroll_duration});
    //$(fragment_containers_id).scrollTo('100%', 0 , {duration: scroll_duration});
    
    function frag_update_history() {
        if (! from_history) update_history(); // Call update history with fragment URL
    }

    // AJAX load html fragment
    frag_loading.load(url,
        function(response, status, request){ // When AJAX load complete
          var frag_loading = $(this);
            if (request.status != 200) {
                frag_loading.remove();
                if (typeof callback != 'undefined') callback(false);
            }
            if (frag_loading) {
                frag_loading.fadeTo(0, 0.01); // Set opacity to 0.01 with a delay of 0, this could be replaced with a setOpacity call? I think this is creating animtion headaches
                //frag_loading.width(0); // animating width buggers up scrolling
                //frag_loading.animate({width: '500px', opacity: 1.0}, scroll_duration);
                frag_loading.animate({opacity: 1.0}, scroll_duration, function() { $(this).removeAttr('style'); }); // Once the animation is complete remove the opacity element because IE disabled antialiasing when this is set
                //frag_loading.fadeIn(scroll_duration);
                //frag_loading.toggle(scroll_duration);
                  
                  if (! from_history) cb_frag_remove_sibblings(frag_loading, frag_update_history);
                  
                  frag_loading = null;
                  html5ize(frag_loading);
                  if (typeof callback != 'undefined') callback(true);
                  // These are unneeded because the playholder is the correct width, so the scroll above will be scrolling to the correct place as the AJAX loads
                  //$(window)._scrollable().scrollTo(frag_loading, {duration: scroll_duration});
                  //$(window)._scrollable().scrollTo('100%',0, {duration: scroll_duration});
                  //$.scrollTo(frag_loading, {duration: scroll_duration}); //(fragment_containers_id)
                  //$(fragment_containers_id).scrollTo('100%', 0 , {duration: scroll_duration});    
                  $(convertYesNoCheckbox);
            }
        }
    );
    return frag_loading;
}

//------------------------------------------------------------------------------
//                               Load Frag
//------------------------------------------------------------------------------


function cb_frag_load(jquery_element, url) {
    // Register this page view with Google analytics. - see cb_frag() for more info
    // AllanC - this is not ideal as it will have the.frag and not record the actual pageview ... but it's better than nothing for now
    _gaq.push(['_trackPageview', url]);
    
  if (typeof cb_frag_get_variable(jquery_element, 'autoSaveDraftTimer') != 'undefined')
    clearInterval(cb_frag_get_variable(jquery_element, 'autoSaveDraftTimer'));
    
    var frag_container = jquery_element.parents('.'+fragment_container_class)
    frag_container.load(url, function() {
        html5ize(frag_container);
    });
}


//------------------------------------------------------------------------------
//                               Remove Frag
//------------------------------------------------------------------------------

function cb_frag_remove(jquery_element, callback, from_history) {
    var parent = jquery_element.parents('.'+fragment_container_class); // find parent
    if (typeof cb_frag_get_variable(jquery_element, 'autoSaveDraftTimer') != 'undefined')
        clearInterval(cb_frag_get_variable(jquery_element, 'autoSaveDraftTimer'));
    parent.toggle(scroll_duration, function(){
        parent.remove();
        // If no fragments on screen redirect to default page
        if ($('.'+fragment_container_class).length == 0) {
            window.location.replace("/");
        }
        if (typeof callback != 'undefined') callback();
        if (! from_history) update_history( $('.'+fragment_container_class).not('.'+fragment_help_class).last().find('.'+fragment_source_class).first().attr('href') );
    });
    cb_frag_remove_sibblings(parent);
    
    $.modal.close(); // Aditionaly, if this is in a popup then close the popup
}

function cb_frag_remove_sibblings(jquery_element, callback, ignorehelp) {
    var parent_siblings;
    if (ignorehelp) {
        parent_siblings = jquery_element.nextAll('.'+fragment_container_class+':not(.'+fragment_help_class+')');
    }
    else {
        parent_siblings = jquery_element.nextAll();
    }
    parent_siblings.toggle(scroll_duration, function() {
        parent_siblings.remove();
        if (typeof callback != 'undefined') callback();
        callback = undefined;
    });
    if (parent_siblings.length == 0 && typeof callback != 'undefined') callback();
}

//------------------------------------------------------------------------------
//                               Reload Frag
//------------------------------------------------------------------------------

function cb_frag_reload(param, exclude_frag) {
    // Can be passed a JQuery object or a String
    //  pamam can be:
    //    JQuery - find frag_container parent - find hidden source link for that frag - reload
    //    String - find hidden source link for all frags - dose source href contain param - reload
    // Sometimes we want to exclude a fragment in the reload search, these can be passed with OPTIONAL exclude_frag as a jquery object
    //
    // AllanC - Suggeston - it would be nice if cb_frag_reload could take a combination of string and jQuery objects in param
    
    function display_reload_feedback(jquery_element) {
        //jquery_element.find('.title_text').first() += ' <img src="/images/ajax-loader.gif" />';
        var title = jquery_element.find('.action_bar').first();
        title.html(title.html() + ' <img src="/images/ajax-loader.gif" />');
    }
    
    // Remove auto-save timer if refreshing fragment! GM
    function clear_autosave_timer(jquery_element) {
        if (typeof cb_frag_get_variable(jquery_element, 'autosavedrafttimer') != 'undefined') {
            clearInterval(cb_frag_get_variable(jquery_element, 'autoSaveDraftTimer'));
        }
    }
    
    function get_parent_container_element_source(jquery_element) {
        var container_element;
        if (jquery_element.hasClass(fragment_container_class)) {
            container_element   = jquery_element;
        } else {
            container_element   = jquery_element.parents('.'+fragment_container_class);
        }
        var frag_source_element = container_element.find('.'+fragment_source_class);
        var frag_source_href    = frag_source_element.attr('href');
        return [container_element, frag_source_href];
    }
    
    // Move up the chain from this element
    //   grab the href of the A frag_source
    //   and use that the .load the parent_frag container
    function reload_element(jquery_element) {
        var elem_source_pair = get_parent_container_element_source(jquery_element);
        var frag_element = elem_source_pair[0];
        var frag_source  = elem_source_pair[1];
        clear_autosave_timer(jquery_element); 
        display_reload_feedback(frag_element);
        frag_element.load(frag_source, function (text, status, xhr) {
            if (xhr.status == 404)
                cb_frag_remove(jquery_element);
        });
    }
    
    function reload_frags_containing(array_of_urls, exclude_frag) {
        // Look through all <A> tags in every frgament for the string
        // if the link contains this string
        // add the <A>'s parent frag to a refresh list (preventing duplicates)
        // go through the frag list refreshing
        var frags_to_refresh = {};
        $(fragment_containers_id+' a').each(function(index) {
            var link_element = $(this);
            for (var url_part in array_of_urls) {
                url_part = array_of_urls[url_part];
                link_element_href = link_element.attr('href');
                if (link_element_href!=undefined && link_element_href.indexOf(url_part) != -1) {
                    var elem_source_pair = get_parent_container_element_source(link_element);
                    var frag_element = elem_source_pair[0];
                    var frag_source  = elem_source_pair[1];
                    clear_autosave_timer(link_element); 
                    frags_to_refresh[frag_source] = frag_element;
                }
            }
        });
        
        // normalize exclude fragment if present
        if (exclude_frag && !exclude_frag.hasClass(fragment_container_class)) {
            exclude_frag = exclude_frag.parents('.'+fragment_container_class);
        }
        // Go though all frags found reloading them
        for (var frag_source in frags_to_refresh) {
            var frag_element = frags_to_refresh[frag_source]
            if (exclude_frag==null || exclude_frag.attr('id')!=frag_element.attr('id')) {
                display_reload_feedback(frag_element);
                frag_element.load(frag_source, function (text, status, xhr) {
                    if (xhr.status == 404)
                        cb_frag_remove(jquery_element);
                });
            }
        }
    }
    
    if      (param === false) return;
    
    if      (                            typeof param    == 'string') {reload_frags_containing([param],exclude_frag);}
    else if (typeOf(param) == 'array' && typeof param[0] == 'string') {reload_frags_containing( param ,exclude_frag);}
    else                                                              {reload_element(          param              );}

}

function cb_frag_set_source(jquery_element, url) {
    jquery_element.parents('.'+fragment_container_class).find('.'+fragment_source_class).attr('href', url);
}

// AllanC - Where is this used?
//function cb_frag_get_source(jquery_element) {
//  jquery_element.parents('.'+fragment_container_class).children('.'+fragment_source_class).attr('href');
//}

function cb_frag_set_variable(jquery_element, variable, value) {
  var valueClean = (typeof value == 'undefined')?(''):(value);
  jquery_element.parents('.'+fragment_container_class).find('.'+fragment_source_class).attr('cb'+variable, valueClean);
}

function cb_frag_get_variable(jquery_element, variable) {
  return jquery_element.parents('.'+fragment_container_class).find('.'+fragment_source_class).attr('cb'+variable);
}

// AllanC - in what circumstance is this used?
//function cb_frag_previous(jquery_element) {
//    return jquery_element.parents('.'+fragment_container_class).prev().children('.'+fragment_source_class);
//}
*/
//------------------------------------------------------------------------------
//                            Browser URL updating
//------------------------------------------------------------------------------

function createStateObj() {
  var stateObj = { 'blocks': []};
  $('.'+fragment_container_class).not('.'+fragment_help_class).each (function (index, element)
    {
      var s_url = $(element).find('.'+fragment_source_class).first().attr('href');
      stateObj.blocks[index] = {'url'  : s_url,
                                'classes': $(element).attr('class')
                               };
    });
  return stateObj;
}

function loadStateObj(stateObj) {
  var frag_previous;
  if(stateObj !== null) {
    if (typeof stateObj.blocks == 'undefined') return;
    
    var i = 0;
    
    function load() {
      if (i < stateObj.blocks.length) {
        var frag_source = frag_previous.find('.'+fragment_source_class).first();
        var stat_href = stateObj.blocks[i].url;
        frag_previous = cb_frag(frag_source, stat_href, undefined, true, load); //$($('.'+fragment_container_class)[i-1]).find('.'+fragment_source_class)
        i ++;
      } else {
        cb_frag_remove_sibblings($($('.'+fragment_container_class)[stateObj.blocks.length-1]), undefined, true);
        return;
      }
    }

    for (i = 0; i < stateObj.blocks.length; i++) {
      var frag_exists = typeof $('.'+fragment_container_class)[i] != 'undefined';
      var frag_container = $($('.'+fragment_container_class)[i]);
      var frag_source = frag_container.find('.'+fragment_source_class);
      var frag_href = frag_source.attr('href');
      var stat_href = stateObj.blocks[i].url;
      if (!frag_exists) {
        load ();
        //frag_container = cb_frag(frag_previous.find('.'+fragment_source_class).first(), stat_href, undefined, true, waiter); //$($('.'+fragment_container_class)[i-1]).find('.'+fragment_source_class)
        break;
      } else if (frag_href != stat_href) {
        frag_container.removeClass().addClass(stateObj.blocks[i].classes);
        frag_container.find('.'+fragment_source_class).first().attr('href', stat_href);
        cb_frag_reload (frag_container);
      }
      frag_previous = frag_container;
    }
    if (i = (stateObj.blocks.length - 1))
      cb_frag_remove_sibblings($($('.'+fragment_container_class)[stateObj.blocks.length-1]), undefined, true);
  }
}

function update_history(url, replace) {
  if (typeof url == 'undefined' || url == null)
    var url = $('.'+fragment_container_class).not('.'+fragment_help_class).last().find('.'+fragment_source_class).first().attr('href');
  if (typeof url == 'undefined' || url == null)
      return;
  // update the URL bar to point at the latest block, and
  // store previous blocks in the history state object
  if(Modernizr.history) {
    // Note: this object is limited to 640k (which ought to be
    // enough for anyone) when saved in the browser history file
    if (replace) {
      history.replaceState(createStateObj(), "Civicboom", url.replace("?format=frag", "").replace(".frag", ""));
    } else {
      history.pushState(createStateObj(), "Civicboom", url.replace("?format=frag", "").replace(".frag", ""));
    }
  } else {
    // if (replace) {
      // if (location.hash.substr(1,3) != 'cbh') {
        // location.replace('#cbh' + encode64($.JSON.encode(createStateObj())));
      // } else {
        // $(window).hashchange();
      // }
    // } else {
      // location.hash = '#cbh' + encode64($.JSON.encode(createStateObj()));
    // }
  }
}

$(function () {
  if(Modernizr.history) {
    // Browser supports HTML5 history states
    // FIXME: jQuery-ise this, rather than using the raw window.blah
    window.onpopstate = function(popstate) { loadStateObj(popstate.state); }
    } else if(Modernizr.hashchange) {
    // Browser does not support HTML5 history states
    // Use url hash instead
    // GregM: Causing stability issues in IE, removed for now
    // $(window).hashchange(function (e) {
    //   var hash = location.hash;
    //   if (hash != '' && typeof hash != 'undefined') {
    //     if (hash.substr(1,3) == 'cbh') {
    //       try {
    //         var stateObj = $.parseJSON(decode64(hash.substr(4)));
    //         loadStateObj(stateObj);
    //       } catch (e) {} 
    //     }
    //   }
    // });
  }
  update_history(location.href, true);
})
