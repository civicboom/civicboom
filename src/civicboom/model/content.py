
from civicboom.model.meta import Base
from civicboom.model.member import Member

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String
from sqlalchemy import Enum, Integer, Date, DateTime, Boolean
from geoalchemy import GeometryColumn, Point, GeometryDDL
from sqlalchemy.orm import relationship, backref

_private_content_doc = """
means different things depending on which child table extends it:

ContentComment
  only visible to the user and the user/group who wrote the content being replied to

ContentDraft
  only visible to the user writing it (otherwise group visible)

ContentArticle
  only visible to creator and requester

ContentAssignment
  only visible to creator and creator-specificed users/groups

FIXME: is this correct?
"""

class Content(Base):
    "Abstract class"
    __tablename__   = "content"
    __type__        = Column(Enum("comment", "draft", "article", name="content_type"), nullable=False) # FIXME: need full list
    __mapper_args__ = {'polymorphic_on': __type__}
    _content_status = Enum("show", "pending", "locked", name="content_status") # FIXME: "etc"?
    id              = Column(Integer(),        primary_key=True)
    title           = Column(Unicode(250),     nullable=False  )
    content         = Column(UnicodeText(),    nullable=False, doc="The body of text")
    creator_id      = Column(Integer(),        ForeignKey('member.id'), nullable=False)
    parent_id       = Column(Integer(),        ForeignKey('content.id'), nullable=True)
    location        = GeometryColumn(Point(2), nullable=True   ) # FIXME: area rather than point?
    timestamp       = Column(DateTime(),       nullable=False, default="now()")
    status          = Column(_content_status,  nullable=False, default="show")
    private         = Column(Boolean(),        nullable=False, default=False, doc=_private_content_doc)
    license_id      = Column(Integer(),        ForeignKey('license.id'), nullable=False)
    responses       = relationship("Content", backref=backref('parent', remote_side=id)) # FIXME: remote_side is confusing
    attachments     = relationship("Media",   backref=backref('content', order_by=id))


class CommentContent(Content):
    __tablename__   = "content_comment"
    __mapper_args__ = {'polymorphic_identity': 'comment'}
    id              = Column(Integer(), ForeignKey('content.id'), primary_key=True)


class DraftContent(Content):
    __tablename__   = "content_draft"
    __mapper_args__ = {'polymorphic_identity': 'draft'}
    id              = Column(Integer(), ForeignKey('content.id'), primary_key=True)


class UserVisibleContent(Content):
    "Abstract class"
    __tablename__ = "content_user_visible"
    id            = Column(Integer(), ForeignKey('content.id'), primary_key=True)
    views         = Column(Integer(), nullable=False, default=0)
    boom_count    = Column(Integer(), nullable=False, default=0) # FIXME: derived


class ArticleContent(UserVisibleContent):
    __tablename__   = "content_article"
    __mapper_args__ = {'polymorphic_identity': 'article'}
    id              = Column(Integer(), ForeignKey('content_user_visible.id'), primary_key=True)
    rating          = Column(Integer(), nullable=False, default=0) # FIXME: derived


class License(Base):
    __tablename__ = "license"
    id            = Column(Integer(),     primary_key=True)
    code          = Column(Unicode(32),   nullable=False, unique=True)
    name          = Column(Unicode(250),  nullable=False, unique=True)
    description   = Column(UnicodeText(), nullable=False)
    url           = Column(UnicodeText(), nullable=False)
    articles      = relationship("Content", backref=backref('license'))

    def __init__(self, code, name, description, url):
        self.code = code
        self.name = name
        self.description = description
        self.url = url


class Tag(Base):
    __tablename__ = "tag"
    id            = Column(Integer(),    primary_key=True)
    name          = Column(Unicode(250), nullable=False) # FIXME: type::name should be unique
    type          = Column(Unicode(250), nullable=False, default=u"Topic")
    parent_id     = Column(Integer(),    ForeignKey('tag.id'), nullable=True)
    children      = relationship("Tag", backref=backref('parent', remote_side=id))

    def __init__(self, name, type=u"Topic", parent=None):
        self.name = name
        self.type = type
        self.parent = parent


class ContentEditHistory(Base):
    __tablename__ = "content_edit_history"
    id            = Column(Integer(),     primary_key=True)
    content_id    = Column(Integer(),     ForeignKey('content.id'), nullable=False)
    member_id     = Column(Integer(),     ForeignKey('member.id'), nullable=False)
    timestamp     = Column(DateTime(),    nullable=False, default="now()")
    source        = Column(Unicode(250),  nullable=False, default="other", doc="civicboom, mobile, another_webpage, other service")
    text_change   = Column(UnicodeText(), nullable=False)
    content       = relationship("Content", backref=backref('edit_history', order_by=id))
    member        = relationship("Member",  backref=backref('edits_made', order_by=id))


class Media(Base):
    __tablename__ = "media"
    _media_types  = Enum("application", "audio", "example", "image", "message", "model", "multipart", "text", "video", name="media_types")
    id            = Column(Integer(),        primary_key=True)
    content_id    = Column(Integer(),        ForeignKey('content.id'), nullable=False)
    name          = Column(UnicodeText(250), nullable=False)
    type          = Column(_media_types,     nullable=False, doc="MIME type, eg 'text', 'video'")
    subtype       = Column(String(32),       nullable=False, doc="MIME subtype, eg 'jpeg', '3gpp'")
    hash          = Column(String(32),       nullable=False, index=True) # FIXME: 32=md5? do we want md5?
    caption       = Column(UnicodeText(),    nullable=False)
    credit        = Column(UnicodeText(),    nullable=False)

    def get_mime_type(self):
        return self.type + "/" + self.subtype

    def get_url(self):
        """
        http://static-e.civicboom.com/e16c819f/my_face.jpg
        """
        return "http://static-%s.civicboom.com/%s/%s" % (self.hash[0], self.hash, self.name)
        # return "http://s3.amazonaws.com/civicboom-media/%s/%s" % (self.hash, self.name)

    def copy_to_mirror(self):
        """
        scp my_face.jpg static-e.civicboom.com:~/staticdata/e1/6c/e16c819f
        """
        # see paramiko
        #scp = SCPClient(SSHTransport("static-%s.civicboom.com" % (self.hash[0], )))
        #scp.put(self.name, "~/staticdata/%s/%s/%s" % (self.hash[0:1], self.hash[2:3], self.hash))
        # upload to S3
        return True


# FIXME: incomplete
#class ContentAssignment(ContentUserVisable):
#    (?date of event?)
#    dateDue
#    private D (if any AssignmentClosed records exist)
#    private_response (bool) (already exisits? see content)


# FIXME: incomplete
#class AssignmentAccepted(Base):
#    contentAssignmentId
#    memberId
#    withdrawn (boolean)


# FIXME: incomplete
#class AssignmentClosed(Base):
#    contentAssignmentId
#    memberId

GeometryDDL(Content.__table__)
