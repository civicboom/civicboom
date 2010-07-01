
from civicboom.model.meta import Base
from civicboom.model.member import Member

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String
from sqlalchemy import Enum, Integer, Date, DateTime, Boolean
from geoalchemy import GeometryColumn, Point, GeometryDDL
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import postgresql

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
    __type_col__    = Column(Enum("comment", "draft", "article", name="content_type")) # FIXME: need full list
    __mapper_args__ = {'polymorphic_on': __type_col__}

    id         = Column(Integer(), primary_key=True)
    title      = Column(Unicode(250))
    content    = Column(UnicodeText(), doc="The body of text")
    creator_id = Column(Integer(), ForeignKey('member.id'))
    parent_id  = Column(Integer(), ForeignKey('content.id'), nullable=True)
    location   = GeometryColumn(Point(2)) # FIXME: area?
    timestamp  = Column(DateTime())
    status     = Column(Enum("show", "pending", "locked", name="content_status")) # FIXME: "etc"?
    private    = Column(Boolean(), default=False, doc=_private_content_doc)
    license_id = Column(Integer(), ForeignKey('license.id'))

    responses   = relationship("Content", backref=backref('parent', remote_side=id)) # FIXME: remote_side is confusing
    attachments = relationship("Media", backref=backref('content', order_by=id))


class CommentContent(Content):
    __tablename__ = "content_comment"
    __mapper_args__ = {'polymorphic_identity': 'comment'}

    id = Column(Integer(), ForeignKey('content.id'), primary_key=True)


class DraftContent(Content):
    __tablename__ = "content_draft"
    __mapper_args__ = {'polymorphic_identity': 'draft'}

    id = Column(Integer(), ForeignKey('content.id'), primary_key=True)


class UserVisibleContent(Content):
    "Abstract class"
    __tablename__ = "content_user_visible"

    id         = Column(Integer(), ForeignKey('content.id'), primary_key=True)
    views      = Column(Integer())
    boom_count = Column(Integer()) # FIXME: derived


class ArticleContent(UserVisibleContent):
    __tablename__ = "content_article"
    __mapper_args__ = {'polymorphic_identity': 'article'}

    id         = Column(Integer(), ForeignKey('content_user_visible.id'), primary_key=True)
    rating     = Column(Integer()) # FIXME: derived


# TODO: populate
class License(Base):
    __tablename__ = "license"

    id          = Column(Integer(), primary_key=True)
    code        = Column(Unicode(32), unique=True)
    name        = Column(Unicode(250), unique=True)
    description = Column(UnicodeText())
    url         = Column(UnicodeText())

    articles    = relationship("Content", backref=backref('license'))

    def __init__(self, code, name, description, url):
        self.code = code
        self.name = name
        self.description = description
        self.url = url


# TODO: populate
# science, technology, politics, environment
class Tag(Base):
    __tablename__ = "tag"

    id        = Column(Integer(), primary_key=True)
    name      = Column(Unicode(250)) # FIXME: type::name should be unique
    type      = Column(Unicode(250))
    parent_id = Column(Integer(), ForeignKey('tag.id'), nullable=True)

    children  = relationship("Tag", backref=backref('parent', remote_side=id))

    def __init__(self, name, type="Topic", parent=None):
        self.name = name
        self.type = type
        self.parent = parent


class ContentEditHistory(Base):
    __tablename__ = "content_edit_history"

    id          = Column(Integer(), primary_key=True)
    content_id  = Column(Integer(), ForeignKey('content.id'))
    member_id   = Column(Integer(), ForeignKey('member.id'))
    timestamp   = Column(DateTime())
    ip          = Column(postgresql.INET(), index=True)
    source      = Column(Unicode(250), doc="civicboom, mobile, another_webpage, other service")
    text_change = Column(UnicodeText())

    content     = relationship("Content", backref=backref('edit_history', order_by=id))
    member      = relationship("Member", backref=backref('edits_made', order_by=id))


class Media(Base):
    __tablename__ = "media"

    id          = Column(Integer(), primary_key=True)
    content_id  = Column(Integer(), ForeignKey('content.id'))
    name        = Column(UnicodeText(250))
    type        = Column(Enum("application", "audio", "example", "image", "message", "model", "multipart", "text", "video", name="media_types"), doc="MIME type, eg 'text', 'video'")
    subtype     = Column(String(32), doc="MIME subtype, eg 'jpeg', '3gpp'")
    hash        = Column(String(32), index=True) # FIXME: 32=md5? do we want md5?
    caption     = Column(UnicodeText())
    credit      = Column(UnicodeText())
    ip          = Column(postgresql.INET(), index=True)

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
