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

class CustomTemplateEngine(TemplateEngine):
    def __init__(self, template):
        self.template = template

    def render(self, name, **kwargs):
        return render("/admin/classes/%s.mako" % self.template, extra_vars=kwargs)

ArticleContent = FieldSet(model.ArticleContent)
ArticleContent.engine = CustomTemplateEngine("content")
ArticleContent.configure(include=[
        ArticleContent.creator,
        ArticleContent.title,
        ArticleContent.status,
        ArticleContent.private,
        ArticleContent.parent,
        ArticleContent.tags,
        ArticleContent.content,
        ArticleContent.responses,
        ArticleContent.attachments,
        ArticleContent.creation_date,
        ArticleContent.update_date,
        ArticleContent.edits,
        ArticleContent.location,
        ])

AssignmentContent = FieldSet(model.AssignmentContent)
AssignmentContent.engine = CustomTemplateEngine("content")
AssignmentContent.configure(include=[
        AssignmentContent.creator,
        AssignmentContent.title,
        AssignmentContent.status,
        AssignmentContent.private,
        AssignmentContent.parent,
        AssignmentContent.tags,
        AssignmentContent.content,
        AssignmentContent.responses,
        AssignmentContent.attachments,
        AssignmentContent.creation_date,
        AssignmentContent.update_date,
        AssignmentContent.edits,
        AssignmentContent.location,
        ])

DraftContent = FieldSet(model.DraftContent)
DraftContent.engine = CustomTemplateEngine("content")
DraftContent.configure(include=[
        DraftContent.creator,
        DraftContent.title,
        DraftContent.status,
        DraftContent.private,
        DraftContent.parent,
        DraftContent.tags,
        DraftContent.content,
        DraftContent.responses,
        DraftContent.attachments,
        DraftContent.creation_date,
        DraftContent.update_date,
        DraftContent.edits,
        DraftContent.location,
        ])

CommentContent = FieldSet(model.CommentContent)
CommentContent.engine = CustomTemplateEngine("comment")
CommentContent.configure(include=[
        CommentContent.creator,
        CommentContent.title,
        CommentContent.parent,
        CommentContent.content,
        CommentContent.responses,
        CommentContent.attachments,
        CommentContent.creation_date,
        ])

User = FieldSet(model.User)
User.engine = CustomTemplateEngine("user")
User.configure(include=[
        User.username,
        User.name,
        User.join_date,
        User.email,
        User.status,
        User.avatar,
        User.home_location,
        User.webpage,
        User.description,
        User.location,
        ])

Group = FieldSet(model.Group)
Group.engine = CustomTemplateEngine("group")
Group.configure(include=[
        Group.username,
        Group.name,
        Group.join_date,
        Group.status,
        Group.avatar,
        Group.home_location,
        Group.webpage,
        Group.description,
        Group.members,
        ])

Message = FieldSet(model.Message)
Message.engine = CustomTemplateEngine("message")
Message.configure(include=[
        Message.source,
        Message.target,
        Message.timestamp,
        Message.text,
        ])

Tag = FieldSet(model.Tag)
Tag.engine = CustomTemplateEngine("tag")
Tag.configure(include=[
        Tag.name,
        Tag.parent,
        ])

Media = FieldSet(model.Media)
Media.engine = CustomTemplateEngine("media")
Media.configure(include=[
        Media.name.with_renderer(fields.TextFieldRenderer),
        Media.type,
        Media.subtype,
        Media.caption.with_renderer(fields.TextFieldRenderer),
        Media.credit.with_renderer(fields.TextFieldRenderer),
        Media.attached_to,
        ])

License = FieldSet(model.License)
License.engine = CustomTemplateEngine("license")


## Initialize grids
# Not doing this will result in the object list being rendered with
# all fields visible

#FooGrid = Grid(model.Foo)
#ReflectedGrid = Grid(Reflected)


ArticleContentGrid = Grid(model.ArticleContent)
ArticleContentGrid.configure(include=[
        ArticleContentGrid.title,
        ArticleContentGrid.creator,
        ArticleContentGrid.update_date,
        ArticleContentGrid.status,
        ArticleContentGrid.attachments,
        ArticleContentGrid.tags,
        ])

AssignmentContentGrid = Grid(model.AssignmentContent)
AssignmentContentGrid.configure(include=[
        AssignmentContentGrid.title,
        AssignmentContentGrid.creator,
        AssignmentContentGrid.update_date,
        AssignmentContentGrid.status,
        AssignmentContentGrid.attachments,
        AssignmentContentGrid.tags,
        ])

CommentContentGrid = Grid(model.CommentContent)
CommentContentGrid.configure(include=[
        CommentContentGrid.title,
        CommentContentGrid.creator,
        CommentContentGrid.attachments,
        CommentContentGrid.parent,
        ])

DraftContentGrid = Grid(model.DraftContent)
DraftContentGrid.configure(include=[
        DraftContentGrid.title,
        DraftContentGrid.creator,
        DraftContentGrid.update_date,
        DraftContentGrid.status,
        DraftContentGrid.attachments,
        DraftContentGrid.tags,
        ])


UserGrid = Grid(model.User)
UserGrid.configure(include=[
        UserGrid.name,
        UserGrid.username,
        UserGrid.join_date,
        UserGrid.status,
        ])

GroupGrid = Grid(model.Group)
GroupGrid.configure(include=[
        GroupGrid.name,
        GroupGrid.username,
        GroupGrid.join_date,
        GroupGrid.num_members,
        ])

MessageGrid = Grid(model.Message)
MessageGrid.configure(include=[
        MessageGrid.source,
        MessageGrid.target,
        MessageGrid.timestamp,
        ])


LicenseGrid = Grid(model.License)
LicenseGrid.configure(include=[
        LicenseGrid.code,
        LicenseGrid.name,
        ])

TagGrid = Grid(model.Tag)
TagGrid.configure(include=[
        TagGrid.name,
        TagGrid.parent,
        ])

MediaGrid = Grid(model.Media)
MediaGrid.configure(include=[
        MediaGrid.name,
        MediaGrid.type,
        MediaGrid.attached_to,
        ])


# custom renderers from geoformalchemy
from geoformalchemy.base import GeometryFieldRenderer
from geoalchemy import geometry
FieldSet.default_renderers[geometry.Geometry] = GeometryFieldRenderer

# custom renderers
from formalchemy.fields import TextAreaFieldRenderer
import sqlalchemy
FieldSet.default_renderers[sqlalchemy.UnicodeText] = TextAreaFieldRenderer
