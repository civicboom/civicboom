from formalchemy.fields import FieldRenderer
from formalchemy.fields import TextAreaFieldRenderer
from civicboom.model.meta import location_to_string


def create_autocompleter(url):
    class AutoCompleteRenderer(FieldRenderer):
        def render(self, options={}):
            sval = self._value if hasattr(self, '_value') else ''
            cn = ""
            for name, val in options:
                if str(val) == sval:
                    cn = name
            vars = dict(
                url=url,
                name=self.name,
                value=sval,
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
        value = self._value if hasattr(self, '_value') else ''
        vars = dict(name=self.name, value=value.split(".")[0])
        return """
<input id="%(name)s" name="%(name)s" type="text" value="%(value)s">
<script type="text/javascript">
$('#%(name)s').datepicker({dateFormat: 'yy-mm-dd'})
</script>
        """ % vars


class EnumFieldRenderer(FieldRenderer):
    def render(self):
        value = self._value if hasattr(self, '_value') else ''
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


from formalchemy.forms import FieldSet
from geoalchemy import geometry
import sqlalchemy

FieldSet.default_renderers[geometry.Geometry] = LocationPickerRenderer
FieldSet.default_renderers[sqlalchemy.UnicodeText] = TextAreaFieldRenderer
FieldSet.default_renderers[sqlalchemy.DateTime] = DatePickerFieldRenderer
FieldSet.default_renderers[sqlalchemy.Enum] = EnumFieldRenderer
