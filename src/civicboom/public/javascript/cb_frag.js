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
      scroll_duration : 1000,
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
              // Close button
              .before(
                $('<a />').attr('href', '#').addClass('simplemodalClose fr icon16 i_delete')
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
                .append(settings.confirmTitle || originalLink.text() || '')
                // Close button
                .before(
                  $('<a />').attr('href', '#').addClass('simplemodalClose fr icon16 i_delete')
                )
            )
            .append(
              // popup-message
              $('<div />').addClass('popup-message').append(settings.confirm || '')
            )
            .append(
              // popup-actions
              $('<div />').addClass('popup-actions').append(
                (settings.confirmSecureOptions && originalLink.hasClass('link_secure')) ? (
                  // secure options
                  $('<ul />').appendEach(
                    $.map(settings.confirmSecureOptions, function(value) {
                      return $('<li />')
                        .append(value.title ? $('<h3 />').append(value.title) : '')
                        .append(value.content)
                        .append(
                          $('<a />')
                          .addClass('button')
                          .append(originalLink.text())
                          .data('original', originalLink)
                          .data('json', value.json)
                          .click(function() {
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
                          })
                        );
                    })
                  )
                ) : (
                  // buttons
                  $('<a />')
                    .addClass('button')
                    .data('original', originalLink)
                    .html(settings.confirmYes || 'Yes')
                    .click(function() {
                      var link = $(this);
                      console.log('click', this, link);
                      var original = link.data('original');
                      original.data('confirmed', 'true');
                      original.click();
                      $.modal.close();
                    })
                    .after(
                      originalLink.hasClass('link_dummy') ? '' : $('<a />').addClass('button').html(settings.confirmNo || 'No').click($.modal.close)
                    )
                )
              )
            )
          )
        );
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
                var form = $(event.target).parents('form');
                // Boom_load event triggers refresh or media listing
                $(event.target).parents('table.media_files').trigger('boom_load');
              }
            });
          });
          // Uploadify end
          return false;
        },
        'closed' : function(event, from_history) {
          console.log('frag_closed');
          if(!from_history) {
            $(this).remove(); // We need to remove the element here, before the history state save!!!
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
        'form.search[method="GET"]' : {
          'submit' : function(event) {
            console.log('form.search[method="get"] submit');
            var form = $(this);
            var i = true;
            
            // frag replace
            var frag_href;
            if (frag_href = form.data('frag')) {
              boom.frags.update(form, frag_href + '?' + form.serialize());
              event.stopImmediatePropagation();
              i = false;
            }
            if (frag_href = form.data('frag-new')) {
              boom.frags.create(form, frag_href + '?' + form.serialize());
              event.stopImmediatePropagation();
              i = false;
            }
            return i;
          }
        },
        'form[method="POST"]' : {
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
        /*
        '.thumbnail' : {
          'boom_load' : function() {
            var div = $(this);
            var img = div.children('img');
            
            $("<img/>").attr({
                src: $(img).attr("src"),
            }).load(function() {
                w = this.width; h = this.height;
                console.log("ENOUGH QUESTIONS GOOD BYE", w, h);
                if (w > h) $(img).addClass('landscape');
                if ($(img).width() && $(img).height()) {
                  $(img).css({
                    left: (div.width()/2)-(img.width()/2),
                    top:  (div.height()/2)-(img.height()/2),
                  });
                }
            });
            return false;
          }
        }
        */
        '.thumbnail' : {
          'boom_load' : function() {
            var div = $(this);
            var img = div.children('img');
            img.one('load', function() {
              div.trigger('boom_load');
            });
            if (img.width() && img.height()) {
                console.log("NHWAJNWAN", img, img.width(), img.height());
              if (img.width() > img.height()) img.addClass('landscape');
              img.css({
                left: (div.width()/2)-(img.width()/2),
                top:  (div.height()/2)-(img.height()/2),
              });
            }
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
        $('body').on('frag_' + eventType, '.' +boom.frags.classes.container, boom.frags.events.frag[eventType]);
        //$('.' + boom.frags.classes.container).live('frag_' + eventType, boom.frags.events.frag[eventType]);
      }
      // Initialise live events
      for(var selector in boom.frags.events.live) {
        for(var eventType in boom.frags.events.live[selector]) {
          console.log('registering event:', selector, eventType);
          $('body').on(eventType, selector, boom.frags.events.live[selector][eventType]);
          //$(selector).live(eventType, boom.frags.events.live[selector][eventType]);
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

      // We use a custom "animation" to show the new frag after it's loaded
      //   This starts with an invisible fragment behind current frags (so we can take measurements)
      frag_loading.css({
        'position': 'absolute',
        'z-index' : '-1',
        'overflow-x':'hidden',
        'opacity' : '0'
      });

      if(current_frag.length > 0) {
        current_frag.after(frag_loading);
      } else {
        boom.frags.container.prepend(frag_loading)
      }
      
      frag_loading.children('.frag_data').each(function () {
        $(this).css('width', $(this).css('width'));
      });
      var frag_width = frag_loading.css('width');

      boom.frags.update(frag_loading, url, undefined, function(success) {
        if(success) {
          // frag_load event is triggered by update above! No need for it here...
          // Once fragment has loaded force frag_data's width to it's measured width.
          frag_loading.children('.frag_data').each(function (){
            $(this).css('width', $(this).css('width'));
          });
          // Set fragment relative, opacity and width 0
          frag_loading.css({
            'position': 'relative',
            'width': '0',
            'opacity': '0',
            'overflow': 'hidden'
          });
          //frag_loading.fadeTo(0, 0.01);
          // Animate fragment to full width & opacity
          var frag_left = frag_loading.position().left; // Get left for scrolling calculation
          var scrollable = $(window)._scrollable(); // Get scrollable element (select once, use many)
          var frag_scroll = true; // Default scroll
          if (frag_loading.next().length) {
            frag_scroll = false; // If there is a frag after this one scroll to that frag & stay static
            scrollable.scrollTo(frag_loading.next());
          }
          // Animate
          frag_loading.animate({
            'opacity' : '1',
            'width' : frag_width
          }, {
            'duration': boom.frags.vars.scroll_duration,
            'complete': function() {
              frag_loading.removeAttr('style');
              scrollable.scrollTo(frag_loading);
            },
            'step': function (now, fx) {
              if (frag_scroll && fx.prop == 'width') {
                scrollable.scrollTo(frag_left + now);
              }
            }
          });
          
          if(!from_history)
            boom.frags.remove(frag_loading.next());
            // boom.frags.remove_after(frag_loading, function() {
              // // FIXME: rewrite history
              // //if (!from_history) boom.frags.update_history();
            // });
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
      boom.frags.clearTimers(current_frag);
      // if (current_frag.data('auto_save_timer') != 'undefined') {
      // clearInterval(current_frag.data('auto_save_timer'));
      // current_frag.removeData('auto_save_timer');
      // }
      
      // Close any modal windows before we start closing frags
      $.modal.close();
      // Remove current frag
      if(!ignore_after) current_frag = current_frag.add(current_frag.nextAll());
      var length = current_frag.length;
      var i = 0;
      // Set frag_data's width to be it's own calculated width (so does not get squashed!)
      current_frag.children('.frag_data').each(function () {
        $(this).css('width', $(this).css('width'));
      });
      
      current_frag.css({'overflow-x':'hidden'}).animate({'width':'0','opacity':'0'}, boom.frags.vars.scroll_duration, function() {
      //current_frag.hide(boom.frags.vars.scroll_duration, function() {
        var element = $(this);
        element.trigger('frag_closed');
        element.remove();
        if (length < ++i) return; // ++i increments i by 1 and returns the incremented number!
        if (callback) callback(true);
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
      });
    },
    modal_close :  function(element, callback) {
      $.modal.close();
      if (callback)
        callback(true);
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
