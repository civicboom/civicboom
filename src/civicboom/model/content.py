
from civicboom.model.meta import Base
from civicboom.model.member import Member

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String
from sqlalchemy import Enum, Integer, Date, DateTime, Boolean
from geoalchemy import GeometryColumn, Point, GeometryDDL
from sqlalchemy.orm import relationship, backref

import hashlib


# many-to-many mappings need to be at the top, so that other classes can
# say "I am joined to other table X using mapping Y as defined above"

class ContentTagMapping(Base):
    __tablename__ = "map_content_to_tag"
    content_id    = Column(Integer(),    ForeignKey('content.id'), nullable=False, primary_key=True)
    tag_id        = Column(Integer(),    ForeignKey('tag.id'), nullable=False, primary_key=True)

class Boom(Base):
    __tablename__ = "map_booms"
    content_id    = Column(Integer(),    ForeignKey('content_user_visible.id'), nullable=False, primary_key=True)
    member_id     = Column(Integer(),    ForeignKey('member.id'), nullable=False, primary_key=True)

class Rating(Base):
    __tablename__ = "map_ratings"
    content_id    = Column(Integer(),    ForeignKey('content_user_visible.id'), nullable=False, primary_key=True)
    member_id     = Column(Integer(),    ForeignKey('member.id'), nullable=False, primary_key=True)
    rating        = Column(Integer(),    nullable=False, default=0)


class Content(Base):
    """
    Abstract class

    "private" means different things depending on which child table extends it:

    ContentComment
      only visible to the user and the user/group who wrote the content being replied to

    ContentDraft
      only visible to the user writing it (otherwise group visible)

    ContentArticle
      only visible to creator and requester

    ContentAssignment
      only visible to creator and creator-specificed users/groups

    (FIXME: is this correct?)
    """
    __tablename__   = "content"
    # FIXME: is this list complete?
    __type__        = Column(Enum("comment", "draft", "article", "assignment", name="content_type"), nullable=False)
    __mapper_args__ = {'polymorphic_on': __type__}
    # FIXME: "etc"?
    _content_status = Enum("show", "pending", "locked", name="content_status")
    id              = Column(Integer(),        primary_key=True)
    title           = Column(Unicode(250),     nullable=False  )
    content         = Column(UnicodeText(),    nullable=False, doc="The body of text")
    creator_id      = Column(Integer(),        ForeignKey('member.id'), nullable=False)
    parent_id       = Column(Integer(),        ForeignKey('content.id'), nullable=True)
    # FIXME: area rather than point?
    location        = GeometryColumn(Point(2), nullable=True   )
    creation_date   = Column(DateTime(),       nullable=False, default="now()")
    update_date     = Column(DateTime(),       nullable=False, default="now()")
    status          = Column(_content_status,  nullable=False, default="show")
    private         = Column(Boolean(),        nullable=False, default=False, doc="see class doc")
    # FIXME: default license? People just making comments probably don't want to pick one every time
    license_id      = Column(Integer(),        ForeignKey('license.id'), nullable=False)
    # FIXME: remote_side is confusing, and do we want to cascade to delete replies?
    responses       = relationship("Content",            backref=backref('parent', remote_side=id), cascade="all")
    attachments     = relationship("Media",              backref=backref('attached_to'), cascade="all,delete-orphan")
    edits           = relationship("ContentEditHistory", backref=backref('content', order_by=id), cascade="all,delete-orphan")
    tags            = relationship("Tag",                secondary=ContentTagMapping.__table__)

    def __unicode__(self):
        return self.title + u" (" + self.__type__ + u")"


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
    ratings         = relationship("Rating", backref=backref('content'), cascade="all,delete-orphan")


class AssignmentContent(UserVisibleContent):
    __tablename__   = "content_assignment"
    __mapper_args__ = {'polymorphic_identity': 'assignment'}
    id              = Column(Integer(),        ForeignKey('content_user_visible.id'), primary_key=True)
    event_date      = Column(DateTime(),       nullable=True)
    due_date        = Column(DateTime(),       nullable=True)
    assigned_to     = relationship("MemberAssignment", backref=backref("content"), cascade="all,delete-orphan")
    #private D (if any AssignmentClosed records exist) # FIXME: "content" already has this?
    #private_response (bool) (already exisits? see content)

class MemberAssignment(Base):
    __tablename__ = "member_assignment"
    content_id    = Column(Integer(),    ForeignKey('content_assignment.id'), nullable=False, primary_key=True)
    member_id     = Column(Integer(),    ForeignKey('member.id'), nullable=False, primary_key=True)
    withdrawn     = Column(Boolean(),    nullable=False, default=False)



# FIXME: is this needed?
#class AssignmentClosed(Base):
#    contentAssignmentId
#    memberId


class License(Base):
    __tablename__ = "license"
    id            = Column(Integer(),     primary_key=True)
    code          = Column(Unicode(32),   nullable=False, unique=True)
    name          = Column(Unicode(250),  nullable=False, unique=True)
    description   = Column(UnicodeText(), nullable=False)
    url           = Column(UnicodeText(), nullable=False)
    #articles      = relationship("Content", backref=backref('license'))

    def __init__(self, code=None, name=None, description=None, url=None):
        self.code = code
        self.name = name
        self.description = description
        self.url = url

    def __unicode__(self):
        return self.code


# FIXME: do we need types *and* parents?
# "type" was added so that "artist_name:red_box" and "photo_of:red_box" could
# be separated, but we could have category->artists->red_box and
# article_contents->photo_of->red_box instead
# Shish - assuming we don't need types
class Tag(Base):
    """
    A topic for an article, eg "cakes", "printers"

    Tags can have parents, eg:
    Food > Cakes
    Science & Technology > Hardware > Printers

    Tags should normally be capitalised and plural
    """
    __tablename__ = "tag"
    id            = Column(Integer(),    primary_key=True)
    name          = Column(Unicode(250), nullable=False) # FIXME: should be unique within its category
    #type          = Column(Unicode(250), nullable=False, default=u"Topic")
    parent_id     = Column(Integer(),    ForeignKey('tag.id'), nullable=True)
    #children      = relationship("Tag", backref=backref('parent', remote_side=id))

    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent

    def __unicode__(self):
        return self.name


# FIXME: unseeded
class ContentEditHistory(Base):
    __tablename__ = "content_edit_history"
    id            = Column(Integer(),     primary_key=True)
    content_id    = Column(Integer(),     ForeignKey('content.id'), nullable=False)
    member_id     = Column(Integer(),     ForeignKey('member.id'), nullable=False)
    timestamp     = Column(DateTime(),    nullable=False, default="now()")
    source        = Column(Unicode(250),  nullable=False, default="other", doc="civicboom, mobile, another_webpage, other service")
    text_change   = Column(UnicodeText(), nullable=False)


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

    def __init__(self, tmp_file=None, original_name=None, caption=None, credit=None):
        "Create a Media object from a blob of data + upload form details"
        if tmp_file:
            self.name = original_name
            (self.type, self.subtype) = ["video", "3gpp"] # FIXME: magic(tmp_file).split("/")
            self.hash = hashlib.md5(file(tmp_file).read()).hexdigest() # FIXME: send chunks to md5, not the whole file
            self.caption = caption
            self.credit = credit

        # process tmp_file
        # create processed_file
        # create thumbnail

        # copy to mirror via SCP
        #scp = SCPClient(SSHTransport("static.civicboom.com"))
        #scp.put(self.name, "~/staticdata/%s/%s/%s" % (self.hash[0:1], self.hash[2:3], self.hash))

        # copy to amazon s3
        # ...

    def __unicode__(self):
        return self.name

    @property
    def mime_type(self):
        return self.type + "/" + self.subtype

    @property
    def original_url(self):
        "The URL of the original as-uploaded file"
        return "http://static.civicboom.com/originals/%s/%s" % (self.hash, self.name)

    @property
    def media_url(self):
        "The URL of the processed media, eg .flv file for video"
        exts = {
            "audio": "ogg",
            "image": "jpeg",
            "video": "flv"
        }
        return "http://static.civicboom.com/media/%s/data.%s" % (self.hash, exts[self.type])

    @property
    def thumbnail_url(self):
        "The URL of a JPEG-format thumbnail of this media"
        return "http://static.civicboom.com/thumbnails/%s/thumb.jpg" % (self.hash, )


GeometryDDL(Content.__table__)
