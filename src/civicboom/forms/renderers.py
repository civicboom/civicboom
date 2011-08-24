from formalchemy.fields import FieldRenderer
from formalchemy.fields import TextAreaFieldRenderer
from formalchemy.fields import SelectFieldRenderer, RadioSet, CheckBoxSet, _extract_options
from civicboom.model.meta import location_to_string, JSONType
import json


def create_autocompleter(url):
    class AutoCompleteRenderer(FieldRenderer):
        def render(self, options={}):
            value = self._value if (hasattr(self, '_value') and self._value) else ''
            cn = ""
            for name, val in options:
                if str(val) == value:
                    cn = name
            vars = dict(
                url=url,
                name=self.name,
                value=value,
                value_name=cn,
            )
            return """
<input id="%(name)s_name" name="%(name)s_name" type="text" value="%(value_name)s">
<input id="%(name)s" name="%(name)s" type="hidden" value="%(value)s">
<script>
$('#%(name)s_name').autocomplete({
    source: function(req, respond) {
        // translate from CB-API formatted data ('response')
        // to jQueryUI formatted ('suggestions')
        $.getJSON("%(url)s&", req, function(response) {
            var suggestions = [];
            $.each(response.data.members, function(i, val) {
                suggestions.push({"label": val.name+" ("+val.username+")", "value": val.id});
            });
            respond(suggestions);
        });
    },
    select: function(event, ui) {
        $('#%(name)s_name').val(ui.item.label);
        $('#%(name)s').val(ui.item.value);
        return false;
    }
});
</script>
            """ % vars
    return AutoCompleteRenderer


class DatePickerFieldRenderer(FieldRenderer):
    def render(self):
        value = self._value if (hasattr(self, '_value') and self._value) else ''
        vars = dict(name=self.name, value=value.split(".")[0])
        return """
<input id="%(name)s" name="%(name)s" type="text" value="%(value)s">
<script type="text/javascript">
$('#%(name)s').datepicker({dateFormat: 'yy-mm-dd'})
</script>
        """ % vars


class EnumFieldRenderer(FieldRenderer):
    def render(self):
        value = self._value if (hasattr(self, '_value') and self._value) else ''
        opts = ""
        if self.field._columns[0].nullable:
            opts = opts + "<option value>None</option>\n"
        for o in self.field._columns[0].type.enums:  # is there a better way? :|
            sel = " selected" if value == o else ""
            opts = opts + ("<option value='%s'%s>%s</option>\n" % (o, sel, o.replace("_", " ")))
        vars = dict(name=self.name, opts=opts)
        return """
<select id="%(name)s" name="%(name)s">
%(opts)s
</select>
        """ % vars
     
class RadioSetRelationRenderer(RadioSet):
    def render(self, options, **kwargs):
        value = self._value
        self.radios = []
        if callable(options):
            options = options(self.field.parent)
        related_model = self.field.relation_type().__name__
        for i, (choice_name, choice_value) in enumerate(_extract_options(options)):
            choice_id = '%s_%i' % (self.name, i)
            radio = self.widget(self.name, choice_value, id=choice_id,
                                checked=self._is_checked(choice_value),
                                **kwargs)
            label = """
    <a href="/admin/%(model)s/models/%(choice_value)s">%(choice_name)s</a>
            """ % dict(model=related_model, choice_value=choice_value, choice_name=choice_name)
            self.radios.append(self.format % dict(field=radio, label=label))
        
        return """
    <div style="height: 120px; overflow: auto">
    %s
    </div>
        """ % ("<br />".join(self.radios or []))

class CheckBoxSetRelationRenderer(CheckBoxSet):
    def render(self, options, **kwargs):
        value = self._value
        self.radios = []
        if callable(options):
            options = options(self.field.parent)
        related_model = self.field.relation_type().__name__
        for i, (choice_name, choice_value) in enumerate(_extract_options(options)):
            choice_id = '%s_%i' % (self.name, i)
            radio = self.widget(self.name, choice_value, id=choice_id,
                                checked=self._is_checked(choice_value),
                                **kwargs)
            label = """
    <a href="/admin/%(model)s/models/%(choice_value)s">%(choice_name)s</a>
            """ % dict(model=related_model, choice_value=choice_value, choice_name=choice_name)
            self.radios.append(self.format % dict(field=radio, label=label))
        
        return """
    <div style="height: 120px; overflow: auto">
    %s
    </div>
        """ % ("<br />".join(self.radios or []))


class LocationPickerRenderer(FieldRenderer):
    def render(self):
        if hasattr(self, 'raw_value') and self.raw_value:
            lonlatval = location_to_string(self.raw_value)
            lonlat = "lonlat: {lon:%s, lat:%s}," % tuple(lonlatval.split(" "))
        else:
            lonlatval = ""
            lonlat = ""
        vars = dict(field_name=self.name, lonlat_js=lonlat, lonlat_str=lonlatval)
        return """
<div style="position: relative; z-index: 0;">
<input id="%(field_name)s_name" name="%(field_name)s_name" type="search" placeholder="Search for location" style="width: 100%%;">
<div style="padding-top: 6px; z-index: 1;" id="%(field_name)s_comp"></div>
<input id="%(field_name)s" name="%(field_name)s" type="hidden" value="SRID=4326;POINT(%(lonlat_str)s)">

<div style="width: 100%%; height: 200px; border: 1px solid black; z-index: 0;" id="%(field_name)s_div"></div>
<script type="text/javascript">
$(function() {
    map = map_picker('%(field_name)s', {
        style: 'wkt',
        %(lonlat_js)s
    });
});
</script>
</div>
""" % vars

#class JSONTypeRenderer(FieldRenderer):
#    def render(self):
#        import ast
#        if hasattr(self, '_value') and self._value:
#            print self._value
#            value = json.dumps(ast.literal_eval(self._value)).replace("'", "&apos;").replace('"', '\\"')
#        else:
#            value = '{}'
#        vars = dict(field_name=self.name, value=value)
#        return """
#%(value)s
#<input id="%(field_name)s" name="%(field_name)s" type="hidden" value='%(value)s' />
#<div id="%(field_name)s_area">
#    <div class="area" style="float:left">
#        <select class="key" size="5" style="width:180px"></select><br />
#        <input class="value" disabled="disabled" type="text" value="" /><br />
#        <input class="save" type="button" value="Save" />&nbsp;
#        <input type="button" value="New" />&nbsp;
#        <input type="button" value="Del" />&nbsp;
#    </div>
#</div>
#<script type="text/javascript">
#$(function() {
#    var init_value = "%(value)s";
#    var field = $("#%(field_name)s");
#    var div   = $("#%(field_name)s_area");
#    var obj = JSON.parse(init_value);
#    
#    function select_change() {
#        var object = $(this);
#        var area = object.parents('.area')
#        var i_val = area.children('.value');
#        var split = object.val().split('|');
#        i_val.val(split[1]).removeAttr('disabled');
#        area.nextAll().remove();
#        if (! isNaN(Number(i_val.val())))
#            return;
#        if (i_val.val() === 'null')
#            return;
#        try {
#            obj = JSON.parse(i_val.val());
#            i_val.attr('disabled','disabled');
#            var new_area = area.clone(false);
#            new_area.find('.key').removeAttr('cevent');
#            area.parent().append(new_area);
#            populate(new_area, JSON.parse(i_val.val()));
#        } catch (e) {};
#    }
#    function save(area) {
#        var s_key = area.children('.key'),
#            i_val = area.children('.value');
#        var selected = s_key.children('option:selected');
#        selected.val(selected.html()+'|'+i_val.val());
#        
#        saved = JSON.stringify(objectify(area));
#        if (area.index() == 0) {
#            field.val(saved);
#            alert (field.val());
#        } else {
#            a_prev = area.prev();
#            a_prev.children('.value').val(saved);
#            save(area.prev());
#        }
#    }
#    function button_click() {
#        var object = $(this);
#        var area = object.parents('.area')
#        var s_key = area.children('.key'),
#            i_val = area.children('.value');
#        if (object.val() == 'Save') {
#            save(area);
#            s_key.change();
#        } else if (object.val() == 'Del') {
#            s_key.find('option:selected').remove();
#            i_val.attr('disabled','disabled');
#            s_key.change();
#        } else {
#            var key = prompt('Variable key?');
#            if (key == '') return;
#            var options = s_key.find('option').map(function(){return $(this).html()}).get();
#            for (lopt in options)
#                if (options[lopt] == key)
#                    return;
#            var opt = $('<option></option>');
#            opt.html(key);
#            var value = key+'|';
#            opt.val(value);
#            s_key.append(opt);
#        }
#    }
#    function populate(area, object) {
#        var s_key = area.children('.key'),
#            i_val = area.children('.value');
#        if (s_key.attr('cevent') !== 'ok') {
#            s_key.change(select_change).attr('cevent','ok');
#            area.children('input:button').click(button_click);
#        }
#        s_key.children('option').remove();
#        if (typeof object.length !== 'undefined') {
#            s_key.attr('is_array', 'true');
#            for (var i = 0; i < object.length; i++) {
#                var value = object[i];
#                if (typeof value === 'object')
#                    value = JSON.stringify(value);
#                var opt = $('<option></option>');
#                opt.val(i+'|'+value);
#                opt.html(i);
#                s_key.append(opt);
#            }
#        } else {
#            for (key in object) {
#                var type = 'string';
#                var value = object[key]
#                if (typeof value === 'object')
#                    value = JSON.stringify(value);
#                var opt = $('<option></option>');
#                opt.val(key+'|'+value);
#                opt.html(key);
#                s_key.append(opt);
#            }
#        }
#    }
#    function parse(string) {
#        var split = string.split('|');
#        var key   = split[0],
#            value = split[1];
#        try {
#            value = JSON.parse(value)
#        } catch (err) {}
#        return {k:key, v:value};
#    }
#    function parse_jq() {
#        return parse($(this).val());
#    }
#    function objectify(area) {
#        var s_key = area.children('.key'),
#            i_val = area.children('.value');
#        var map = s_key.find('option').map(parse_jq).get();
#        var ret;
#        if (s_key.attr('is_array') == 'true') {
#            ret = [];
#            for (key in map) {
#                if (typeof map[key].k !== 'undefined')
#                    ret[map[key].k] = map[key].v;
#            }
#        } else {
#            ret = {};
#            for (key in map) {
#                if (typeof map[key].k !== 'undefined')
#                    ret[map[key].k] = map[key].v;
#            }
#        }
#        return ret;
#    }
#    populate(div.children('.area').first(), obj);
#});
#</script>
#<div style="clear:both"></div>
#""" % vars


from formalchemy.forms import FieldSet
from geoalchemy import geometry
import sqlalchemy

FieldSet.default_renderers[geometry.Geometry] = LocationPickerRenderer
FieldSet.default_renderers[sqlalchemy.UnicodeText] = TextAreaFieldRenderer
FieldSet.default_renderers[sqlalchemy.DateTime] = DatePickerFieldRenderer
FieldSet.default_renderers[sqlalchemy.Enum] = EnumFieldRenderer
#FieldSet.default_renderers[JSONType] = JSONTypeRenderer
