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
from formalchemy.fields import FieldRenderer
from formalchemy.fields import TextAreaFieldRenderer
from geoformalchemy.base import GeometryFieldRenderer
from geoalchemy import geometry
import sqlalchemy

fa_config.encoding = 'utf-8'

class TemplateEngine(templates.TemplateEngine):
    def render(self, name, **kwargs):
        return render('/admin/formalchemy/%s.mako' % name, extra_vars=kwargs)
fa_config.engine = TemplateEngine()

class FieldSet(forms.FieldSet):
    pass

class Grid(tables.Grid):
    pass

# custom renderers {{{
#class MemberFieldRenderer(FieldRenderer):
#    def render(self, options={}):
#        value= self.value and self.value or ''
#        cn = ""
#        for name, n in options:
#            if str(n) == self.value:
#                cn = name
#        vars = dict(field_name=self.name, value=value, value_name=cn)
#        return """
#<div style="padding-bottom: 2em;">
#	<input id="%(field_name)s_name" name="%(field_name)s_name" type="text" value="%(value_name)s">
#	<div id="%(field_name)s_comp"></div>
#	<input id="%(field_name)s" name="%(field_name)s" type="hidden" value="%(value)s">
#</div>
#<script>autocomplete_member("%(field_name)s_name", "%(field_name)s_comp", "%(field_name)s");</script>
#        """ % vars

FieldSet.default_renderers[geometry.Geometry] = GeometryFieldRenderer
FieldSet.default_renderers[sqlalchemy.UnicodeText] = TextAreaFieldRenderer
#FieldSet.default_renderers[model.Member] = MemberFieldRenderer

# }}}
# object editors {{{
## Initialize fieldsets

#Foo = FieldSet(model.Foo)
#Reflected = FieldSet(Reflected)

class CustomTemplateEngine(TemplateEngine):
    def __init__(self, template):
        self.template = template

    def render(self, name, **kwargs):
        return render("/admin/classes/%s.mako" % self.template, extra_vars=kwargs)

Content = FieldSet(model.Content)
Content.engine = CustomTemplateEngine("content")
Content.configure(include=[
        Content.creator,
        Content.title,
        Content.status,
        Content.private,
        Content.parent,
        Content.tags,
        Content.content,
        Content.responses,
        Content.attachments,
        Content.creation_date,
        Content.update_date,
        Content.edits,
        Content.location,
        ])

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

FlaggedContent = FieldSet(model.FlaggedContent)
FlaggedContent.engine = CustomTemplateEngine("flagged")
FlaggedContent.configure(include=[
        FlaggedContent.content.readonly(),
        FlaggedContent.content_id.readonly(),
        FlaggedContent.member.readonly(),
        FlaggedContent.timestamp.readonly(),
        FlaggedContent.type.readonly(),
        FlaggedContent.comment.readonly(),
        ])

User = FieldSet(model.User)
User.engine = CustomTemplateEngine("user")
User.configure(include=[
        User.username,
        User.name,
        User.join_date,
        User.email,
        User.status,
        ])

Group = FieldSet(model.Group)
Group.engine = CustomTemplateEngine("group")
Group.configure(include=[
        Group.username,
        Group.name,
        Group.join_date,
        Group.status,
        Group.members,
        ])

Message = FieldSet(model.Message)
Message.engine = CustomTemplateEngine("message")
Message.configure(include=[
        Message.source,
        Message.target,
        Message.timestamp,
        Message.subject.with_renderer(fields.TextFieldRenderer),
        Message.content,
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
# }}}
# object grids {{{
## Initialize grids
# Not doing this will result in the object list being rendered with
# all fields visible

#FooGrid = Grid(model.Foo)
#ReflectedGrid = Grid(Reflected)

ArticleContentGrid = Grid(model.ArticleContent)
ArticleContentGrid.configure(include=[
        ArticleContentGrid.title,
        ArticleContentGrid.creator,
        ArticleContentGrid.update_date.readonly(),
        ArticleContentGrid.status,
        ArticleContentGrid.attachments.readonly(),
        ArticleContentGrid.tags.readonly(),
        ])

AssignmentContentGrid = Grid(model.AssignmentContent)
AssignmentContentGrid.configure(include=[
        AssignmentContentGrid.title,
        AssignmentContentGrid.creator,
        AssignmentContentGrid.update_date.readonly(),
        AssignmentContentGrid.status,
        AssignmentContentGrid.attachments.readonly(),
        AssignmentContentGrid.tags.readonly(),
        ])

CommentContentGrid = Grid(model.CommentContent)
CommentContentGrid.configure(include=[
        CommentContentGrid.title,
        CommentContentGrid.creator,
        CommentContentGrid.parent,
        CommentContentGrid.attachments.readonly(),
        ])

DraftContentGrid = Grid(model.DraftContent)
DraftContentGrid.configure(include=[
        DraftContentGrid.title,
        DraftContentGrid.creator,
        DraftContentGrid.update_date.readonly(),
        DraftContentGrid.status,
        DraftContentGrid.attachments.readonly(),
        DraftContentGrid.tags.readonly(),
        ])


FlaggedContentGrid = Grid(model.FlaggedContent)
FlaggedContentGrid.configure(include=[
        FlaggedContentGrid.content,
        FlaggedContentGrid.type.readonly(),
        FlaggedContentGrid.member,
        FlaggedContentGrid.comment.readonly(),
        ])

UserGrid = Grid(model.User)
UserGrid.configure(include=[
        UserGrid.name,
        UserGrid.username,
        UserGrid.join_date.readonly(),
        UserGrid.status,
        ])

GroupGrid = Grid(model.Group)
GroupGrid.configure(include=[
        GroupGrid.name,
        GroupGrid.username,
        GroupGrid.join_date.readonly(),
        GroupGrid.num_members,
        ])

MessageGrid = Grid(model.Message)
MessageGrid.configure(include=[
        MessageGrid.source,
        MessageGrid.target,
        MessageGrid.timestamp.readonly(),
        MessageGrid.subject,
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

# }}}
