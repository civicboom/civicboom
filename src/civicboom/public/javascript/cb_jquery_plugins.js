(function($) {
  $.widget("ui.tagged", {
    options: {
      appendTo: "body",
      tagSource: [],
      triggerKeys: ['enter', 'comma', 'tab'],
      initialTags: [],
      minLength: 1,
      select: false,
      update: null,
      removeText: 'x',
      requireMatch: true,
      placeholder: null,
      hiddenFieldName: null,
      hiddenFieldRenderer: function (elementsArray) {
        return $.map(elementsArray, function (value){
          return $(value).data('value');
        }).join(',');
      },
      itemNormaliser: function (item) {
        if (typeof item == 'string' || typeof item == 'number')
          item = {
            name: item,
            value: item
          }
        return item;
      },
      noResultsString: 'No results...',
      itemRenderer: function (item) {
        return $('<li />').data('value', item.value).append($('<a />').append(item.name));
      }
    },
    _create: function () {
      var self = this,
        doc = this.element[0].ownerDocument,
        suppressKeyPress;
       
      this.element.addClass('cb-tags');
      
      var originalItemNormaliser = this.options.itemNormaliser
      this.options.itemNormaliser = function (item) {
        var new_item = originalItemNormaliser(item);
        new_item.is_no_results = item.is_no_results;
        return new_item;
      }
      
      this.input = this.element.append('<li class="cb-tag-new"><input class="cb-tag-input" type="text" /></li>').find('.cb-tag-input');
      
      if (this.options.placeholder)
        this.input.attr('placeholder', this.options.placeholder);
      
      this.hiddenField = null;
      this._createHiddenField();
      
      this.element.on('click', '*', function (event){
        var elem = $(this);
        if (elem.hasClass('cb-tag-remove')) {
          elem.parent().remove();
          self._update();
        }
        self.input.focus();
        return false;
      });
      
      // If we don't use a timeout we get a search happen with previously selected value :(
      this.timeoutFocus = null;
      
      this.input.on('focus', function () {
        var input = $(this);
        self.timeoutFocus = setTimeout(function () {
          if (input.val())
            input.autocomplete('search');
        }, 100);
      });
      
      this.input.autocomplete({
        appendTo: this.options.appendTo,
        minLength: 1,
        source: function (req, callback) {
          if (typeof self.options.tagSource == 'function') {
            self.options.tagSource(req, function (data) {
              if (data.length == 0)
                data.push({is_no_results:true});
              for (var i = 0; i < data.length; i++) {
                data[i] = self.options.itemNormaliser(data[i])
              }
              callback(data);
            }, self);
          } else {
            // Array!
          }
        },
        focus: function(event, ui) {
          self.input.val(ui.item.name);
          return false;
        },
        select: function(event, ui) {
          clearTimeout(self.timeoutFocus);
          self.timeoutFocus = null;
          self.input.val('');
          self.input.parent().before(self.options.itemRenderer(ui.item).append(self.options.removeElement?self.options.removeElement:$('<a href="#" class="fr cb-tag-remove"></a>').append(self.options.removeText)));
          self._update();
          return false;
        }
      }).data('autocomplete')._renderItem = function (ul, item) {
        if (item.is_no_results) return $('<li />').append(self.options.noResultsString).appendTo(ul);
        return self.options.itemRenderer(item).data( "item.autocomplete", item ).appendTo(ul);
      };
    },
    clear: function () {
      this.element.children().not('.cb-tag-new').remove();
      this._update();
    },
    _update: function () {
      if (typeof this.options.update == 'function')
        this.options.update.apply(this.element);
      this._updateHiddenField();
    },
    _createHiddenField: function (self) {
      this.hiddenField = this.input.after($('<input type="hidden" />').attr('name', this.options.hiddenFieldName).addClass('cb-tag-hidden')).next('.cb-tag-hidden');
      if (this.options.hiddenFieldName) {
        this.hiddenField.attr('name', this.options.hiddenFieldName);
      }
    },
    _updateHiddenField: function () {
      if (this.hiddenField) {
        this.hiddenField.val( this.options.hiddenFieldRenderer( $.makeArray(this.element.children('li').not('.cb-tag-input')) ) );
      }
    },
  })
})(jQuery);