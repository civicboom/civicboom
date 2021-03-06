from civicboom import model

from formalchemy.tables import Grid


## Initialize grids
# Not doing this will result in the object list being rendered with
# all fields visible

#FooGrid = Grid(model.Foo)
#ReflectedGrid = Grid(Reflected)

ContentGrid = Grid(model.Content)
ContentGrid.configure(include=[
        ContentGrid.title,
        ContentGrid.creator,
        ContentGrid.update_date.readonly(),
        #ContentGrid.status,
        ])

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


FlaggedEntityGrid = Grid(model.FlaggedEntity)
FlaggedEntityGrid.configure(include=[
        FlaggedEntityGrid.offending_content,
        FlaggedEntityGrid.type.readonly(),
        FlaggedEntityGrid.raising_member,
        FlaggedEntityGrid.comment.readonly(),
        ])

MemberGrid = Grid(model.Member)
MemberGrid.configure(include=[
        MemberGrid.id,
        MemberGrid.name,
        ])

UserGrid = Grid(model.User)
UserGrid.configure(include=[
        UserGrid.id,
        UserGrid.name,
        UserGrid.email,
        UserGrid.join_date.readonly(),
        UserGrid.status,
        ])

GroupGrid = Grid(model.Group)
GroupGrid.configure(include=[
        GroupGrid.id,
        GroupGrid.name,
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

PaymentAccountGrid = Grid(model.PaymentAccount)
PaymentAccountGrid.configure(include=[
        PaymentAccountGrid.type,
        PaymentAccountGrid.billing_status,
        PaymentAccountGrid.start_date,
        PaymentAccountGrid.currency,
        PaymentAccountGrid.frequency,
        PaymentAccountGrid.taxable,
        PaymentAccountGrid.tax_rate_code,
        ])

InvoiceGrid = Grid(model.Invoice)
InvoiceGrid.configure(include=[
        InvoiceGrid.id,
        InvoiceGrid.payment_account,
        InvoiceGrid.status,
        InvoiceGrid.timestamp,
        InvoiceGrid.due_date,
        InvoiceGrid.currency,
        InvoiceGrid.taxable,
        InvoiceGrid.tax_rate_code,
        InvoiceGrid.tax_rate,
        ])
