from civicboom import model
from civicboom.lib.base import render
from formalchemy import forms, templates, fields
from civicboom.forms.renderers import *
from civicboom.forms.renderers import CheckBoxSetRelationRenderer, RadioSetRelationRenderer


class FieldSet(forms.FieldSet):
    pass

## Initialize fieldsets

#Foo = FieldSet(model.Foo)
#Reflected = FieldSet(Reflected)


class TemplateEngine(templates.TemplateEngine):
    def render(self, name, **kwargs):
        return render('/admin/formalchemy/%s.mako' % name, extra_vars=kwargs)


class CustomTemplateEngine(templates.TemplateEngine):
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
        DraftContent.creator.with_renderer(create_autocompleter("/members.json")),
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
        CommentContent.creator.with_renderer(create_autocompleter("/members.json")),
        CommentContent.title,
        CommentContent.parent,
        CommentContent.content,
        CommentContent.responses,
        CommentContent.attachments,
        CommentContent.creation_date,
        ])

FlaggedEntity = FieldSet(model.FlaggedEntity)
FlaggedEntity.engine = CustomTemplateEngine("flagged")
FlaggedEntity.configure(include=[
        FlaggedEntity.offending_content.readonly(),
        FlaggedEntity.offending_content_id.readonly(),
        FlaggedEntity.raising_member.readonly(),
        FlaggedEntity.timestamp.readonly(),
        FlaggedEntity.type.readonly(),
        FlaggedEntity.comment.readonly(),
        ])

Member = FieldSet(model.Member)
Member.engine = CustomTemplateEngine("member")
Member.configure(include=[
        Member.id,
        Member.name,
        Member.join_date,
        Member.payment_account.with_renderer(RadioSetRelationRenderer),
        ])

User = FieldSet(model.User)
User.engine = CustomTemplateEngine("user")
User.configure(include=[
        User.id,
        User.name,
        User.join_date,
        User.email,
        User.email_unverified,
        User.status,
        User.payment_account,
        ])

Group = FieldSet(model.Group)
Group.engine = CustomTemplateEngine("group")
Group.configure(include=[
        Group.id,
        Group.name,
        Group.join_date,
        Group.status,
        Group.join_mode,
        Group.member_visibility,
        Group.default_content_visibility,
        Group.default_role,
        Group.payment_account,
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



PaymentAccount = FieldSet(model.PaymentAccount)
PaymentAccount.engine = CustomTemplateEngine('payment_account')
PaymentAccount.configure(include=[
        PaymentAccount.type,
        PaymentAccount.billing_status,
        PaymentAccount.start_date,
        PaymentAccount.currency,
        PaymentAccount.frequency,
        PaymentAccount.taxable,
        PaymentAccount.tax_rate_code,
        PaymentAccount.members.with_renderer(CheckBoxSetRelationRenderer),
        PaymentAccount.billing_accounts.with_renderer(CheckBoxSetRelationRenderer),
        ])

Invoice = FieldSet(model.Invoice)
Invoice.engine = CustomTemplateEngine('invoice')
Invoice.configure(include=[
        Invoice.id,
        Invoice.payment_account,
        Invoice.status,
        Invoice.timestamp,
        Invoice.currency,
        Invoice.taxable,
        Invoice.tax_rate_code,
        Invoice.tax_rate,
        ])
