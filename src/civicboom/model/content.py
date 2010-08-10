
from civicboom.model.meta import Base
from civicboom.model.member import Member
from civicboom.model.media import Media

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String
from sqlalchemy import Enum, Integer, Date, DateTime, Boolean, Float
from geoalchemy import GeometryColumn, Point, GeometryDDL
from sqlalchemy import func
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
      responses are provate to oringinal creator

    (FIXME: is this correct?)
    """
    __tablename__   = "content"
    __type__        = Column(Enum("comment", "draft", "article", "assignment", "syndicate", name="content_type"), nullable=False)
    __mapper_args__ = {'polymorphic_on': __type__}
    _content_status = Enum("pending", "show", "locked", name="content_status")
    id              = Column(Integer(),        primary_key=True)
    title           = Column(Unicode(250),     nullable=True)
    content         = Column(UnicodeText(),    nullable=True, doc="The body of text")
    creator_id      = Column(Integer(),        ForeignKey('member.id'), nullable=False)
    parent_id       = Column(Integer(),        ForeignKey('content.id'), nullable=True)
    location        = GeometryColumn(Point(2), nullable=True   ) # FIXME: area rather than point? AllanC - Point for now, need to consider referenceing polygon areas in future? (more research nedeed)
    creation_date   = Column(DateTime(),       nullable=False, default=func.now())
    update_date     = Column(DateTime(),       nullable=False, default=func.now(), doc="Controlled by postgres trigger")
    status          = Column(_content_status,  nullable=False, default="pending")
    private         = Column(Boolean(),        nullable=False, default=False, doc="see class doc")
    license_id      = Column(Integer(),        ForeignKey('license.id'), nullable=False, default=1)
    # FIXME: remote_side is confusing, and do we want to cascade to delete replies?
    responses       = relationship("Content",            backref=backref('parent', remote_side=id, order_by=creation_date)) #, cascade="all" AllanC - coulbe be dangerious, may need to consider more carefully delete behaviour for differnt types of content
    attachments     = relationship("Media",              backref=backref('attached_to'), cascade="all,delete-orphan")
    edits           = relationship("ContentEditHistory", backref=backref('content', order_by=id), cascade="all,delete-orphan")
    tags            = relationship("Tag",                secondary=ContentTagMapping.__table__)
    license         = relationship("License")

    comments        = relationship("CommentContent", order_by=creation_date.asc(), cascade="all", primaryjoin="CommentContent.id == Content.parent_id") #, cascade="all" AllanC - coulbe be dangerious, may need to consider more carefully delete behaviour for differnt types of content    

    def __unicode__(self):
        return self.title + u" (" + self.__type__ + u")"

    def hash(self):
        h = hashlib.md5()
        # Problem? TODO?
        # What about pythons own hash(obj) method?
        # AllanC - creator, parent, attachments and license are realtions and WILL trigger an additional query in most cases.
        #          we cant rely on just looking at creator_id etc as this may not be set until a commit
        #          solutions on a postcard?
        # is there a way in SQLAlchemy to force and object to resolve ID's without a commit?
        # need to add hash to sub objects? like Media etc
        for field in ("id","title","content","creator","parent","update_date","status","private","license","attachments"): # AllanC: unfinished field list? include relations?
            h.update(str(getattr(self,field)))
        return h.hexdigest()

    def editable_by(self, member):
        """
        Check to see if a member object has the rights to edit this content
        """
        if self.status  == "locked": return False
        if self.creator == None    : return True # If nobody owns it then eveyone can edit it, this is used when first creating blank content
        if self.creator == member  : return True
        # TODO check groups of creator to see if member is in the owning group
        return False


class DraftContent(Content):
    __tablename__   = "content_draft"
    __mapper_args__ = {'polymorphic_identity': 'draft'}
    id              = Column(Integer(), ForeignKey('content.id'), primary_key=True)

class CommentContent(Content):
    __tablename__   = "content_comment"
    __mapper_args__ = {'polymorphic_identity': 'comment'}
    id              = Column(Integer(), ForeignKey('content.id'), primary_key=True)



class UserVisibleContent(Content):
    "Abstract class"
    __tablename__ = "content_user_visible"
    id            = Column(Integer(), ForeignKey('content.id'), primary_key=True)
    views         = Column(Integer(), nullable=False, default=0)
    boom_count    = Column(Integer(), nullable=False, default=0, doc="Controlled by postgres trigger")


class ArticleContent(UserVisibleContent):
    __tablename__   = "content_article"
    __mapper_args__ = {'polymorphic_identity': 'article'}
    id              = Column(Integer(), ForeignKey('content_user_visible.id'), primary_key=True)
    rating          = Column(Float(), nullable=False, default=0, doc="Controlled by postgres trigger")
    ratings         = relationship("Rating", backref=backref('content'), cascade="all,delete-orphan")


class AssignmentContent(UserVisibleContent):
    __tablename__   = "content_assignment"
    __mapper_args__ = {'polymorphic_identity': 'assignment'}
    id              = Column(Integer(),        ForeignKey('content_user_visible.id'), primary_key=True)
    event_date      = Column(DateTime(),       nullable=True)
    due_date        = Column(DateTime(),       nullable=True)
    assigned_to     = relationship("MemberAssignment", backref=backref("content"), cascade="all,delete-orphan")
    closed          = Column(Boolean(),        nullable=False, default=False, doc="when assignment is created it must have associated MemberAssigmnet records set to pending")
    
    def hash(self):
        h = hashlib.md5(UserVisibleContent.hash(self))
        for field in ("event_date","due_date","closed"): #TODO: includes assigned_to in list?
            h.update(str(getattr(self,field)))
        return h.hexdigest()


class MemberAssignment(Base):
    __tablename__ = "member_assignment"
    _assignment_status = Enum("pending", "accepted", "withdrawn", name="assignment_status")
    content_id    = Column(Integer(),    ForeignKey('content_assignment.id'), nullable=False, primary_key=True)
    member_id     = Column(Integer(),    ForeignKey('member.id')            , nullable=False, primary_key=True)
    status        = Column(_assignment_status,  nullable=False)


class License(Base):
    __tablename__ = "license"
    id            = Column(Integer(),     primary_key=True)
    code          = Column(Unicode(32),   nullable=False, unique=True)
    name          = Column(Unicode(250),  nullable=False, unique=True)
    url           = Column(Unicode(250),  nullable=False)
    description   = Column(UnicodeText(), nullable=False)
    #articles      = relationship("Content", backref=backref('license'))

    def __init__(self, code=None, name=None, description=None, url=None):
        self.code = code
        self.name = name
        self.description = description
        self.url = url

    def __unicode__(self):
        return self.code


# "type" was added so that "artist_name:red_box" and "photo_of:red_box" could
# be separated, but we could have category->artists->red_box and
# article_contents->photo_of->red_box instead
# Shish - assuming we don't need types AllanC agreed
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
    children      = relationship("Tag", backref=backref('parent', remote_side=id))

    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent

    def __unicode__(self):
        return self.full_name

    @property
    def full_name(self):
        if self.parent:
            # FIXME: unicode arrow? HTML &rarr?
            return self.parent.full_name + " --> " + self.name
        else:
            return self.name


# FIXME: unseeded
class ContentEditHistory(Base):
    __tablename__ = "content_edit_history"
    id            = Column(Integer(),     primary_key=True)
    content_id    = Column(Integer(),     ForeignKey('content.id'), nullable=False)
    member_id     = Column(Integer(),     ForeignKey('member.id'), nullable=False)
    timestamp     = Column(DateTime(),    nullable=False, default=func.now())
    source        = Column(Unicode(250),  nullable=False, default="other", doc="civicboom, mobile, another_webpage, other service")
    text_change   = Column(UnicodeText(), nullable=False)


GeometryDDL(Content.__table__)
