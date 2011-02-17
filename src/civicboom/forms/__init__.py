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
def create_autocompleter(url):
    class AutoCompleteRenderer(FieldRenderer):
        def render(self, options={}):
            cn = ""
            for name, val in options:
                if str(val) == self.value:
                    cn = name
            vars = dict(
                url=url,
                name=self.name,
                value=self.value,
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
        value= self.value and self.value or ''
        vars = dict(name=self.name, value=value)
        return """
<input id="%(name)s" name="%(name)s" type="text" value="%(value)s">
<script type="text/javascript">
$('#%(name)s').datepicker({dateFormat: 'yy-mm-dd'})
</script>
        """ % vars

FieldSet.default_renderers[geometry.Geometry] = GeometryFieldRenderer
FieldSet.default_renderers[sqlalchemy.UnicodeText] = TextAreaFieldRenderer
FieldSet.default_renderers[sqlalchemy.DateTime] = DatePickerFieldRenderer

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
        Content.creator.with_renderer(create_autocompleter("/members.json?list=all")),
        Content.title,
        #Content.status,
        Content.edit_lock,
        Content.visible,
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
        Content.flags,
        ])

ArticleContent = FieldSet(model.ArticleContent)
ArticleContent.engine = CustomTemplateEngine("content")
ArticleContent.configure(include=[
        ArticleContent.creator.with_renderer(create_autocompleter("/members.json?list=all")),
        ArticleContent.title,
        ArticleContent.edit_lock,
        ArticleContent.visible,
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
        AssignmentContent.creator.with_renderer(create_autocompleter("/members.json?list=all")),
        AssignmentContent.title,
        AssignmentContent.edit_lock,
        AssignmentContent.visible,
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
        DraftContent.creator.with_renderer(create_autocompleter("/members.json?list=all")),
        DraftContent.title,
        #DraftContent.status,
        DraftContent.edit_lock,
        DraftContent.visible,
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
        CommentContent.creator.with_renderer(create_autocompleter("/members.json?list=all")),
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
        #Group.members, # FIXME: links are to memberships, not members
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
        #ArticleContentGrid.status,
        ArticleContentGrid.attachments.readonly(),
        ArticleContentGrid.tags.readonly(),
        ])

AssignmentContentGrid = Grid(model.AssignmentContent)
AssignmentContentGrid.configure(include=[
        AssignmentContentGrid.title,
        AssignmentContentGrid.creator,
        AssignmentContentGrid.update_date.readonly(),
        #AssignmentContentGrid.status,
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
        #DraftContentGrid.status,
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
        UserGrid.email,
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
        LicenseGrid.id,
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
