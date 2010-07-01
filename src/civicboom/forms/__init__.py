from pylons import config
from civicboom import model
from civicboom.lib.base import render
from formalchemy import config as fa_config
from formalchemy import templates
from formalchemy import validators
from formalchemy import fields
from formalchemy import forms
from formalchemy import tables
from formalchemy.ext.fsblob import FileFieldRenderer
from formalchemy.ext.fsblob import ImageFieldRenderer

fa_config.encoding = 'utf-8'

class TemplateEngine(templates.TemplateEngine):
    def render(self, name, **kwargs):
        return render('/forms/%s.mako' % name, extra_vars=kwargs)
fa_config.engine = TemplateEngine()

class FieldSet(forms.FieldSet):
    pass

class Grid(tables.Grid):
    pass

## Initialize fieldsets

#Foo = FieldSet(model.Foo)
#Reflected = FieldSet(Reflected)

## Initialize grids

#FooGrid = Grid(model.Foo)
#ReflectedGrid = Grid(Reflected)

# custom renderers from geoformalchemy
from geoformalchemy.base import GeometryFieldRenderer
from geoalchemy import geometry
FieldSet.default_renderers[geometry.Geometry] = GeometryFieldRenderer

# custom renderers
from formalchemy.fields import TextAreaFieldRenderer
import sqlalchemy
FieldSet.default_renderers[sqlalchemy.UnicodeText] = TextAreaFieldRenderer
