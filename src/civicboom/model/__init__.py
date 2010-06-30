"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from civicboom.model import meta

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #
    meta.Session.configure(bind=engine)
    meta.engine = engine


# FIXME:
# 0.9.7 had this included, 1.0 doesn't?
# docs mention including this in meta.py, but it doesn't work there? :S
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# civicboom objects
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String
from sqlalchemy import Enum, Integer, Date, DateTime, Boolean
from postgis    import GISColumn, Point, Curve, LineString
from sqlalchemy.orm import relationship
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
    __tablename__ = "content"

    id         = Column(Integer(), primary_key=True)
    title      = Column(Unicode(250))
    content    = Column(UnicodeText(), doc="The body of text")
    creator_id = Column(Integer(), ForeignKey('member.id'))
    parent_id  = Column(Integer(), ForeignKey('content.id'), nullable=True)
    location   = GISColumn(Point()) # FIXME: area?
    timestamp  = Column(DateTime())
    status     = Column(Enum(["show", "pending", "locked"])) # FIXME: "etc"?
    private    = Column(Boolean(), default=False, doc=_private_content_doc)
    license    = Column(Integer(), ForeignKey('license.id'))

    creator    = relationship("Member", primaryjoin="creator_id==Member.id")
    parent     = relationship("Content", primaryjoin="parent_id==Content.id")


class CommentContent(Content):
    __tablename__ = "content_comment"

    id = Column(Integer(), ForeignKey('content.id'), primary_key=True)


class DraftContent(Content):
    __tablename__ = "content_draft"

    id = Column(Integer(), ForeignKey('content.id'), primary_key=True)


class UserVisibleContent(Content):
    __tablename__ = "content_user_visible"

    id         = Column(Integer(), ForeignKey('content.id'), primary_key=True)
    views      = Column(Integer())
    boom_count = Column(Integer()) # FIXME: derived


class ArticleContent(UserVisibleContent):
    __tablename__ = "content_article"

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


# TODO: populate
# science, technology, politics, environment
class Tag(Base):
    __tablename__ = "tag"

    id        = Column(Integer(), primary_key=True)
    name      = Column(Unicode(250), unique=True)
    type      = Column(Unicode(250))
    parent_id = Column(Integer(), ForeignKey('tag.id'), nullable=True)

    parent    = relationship("Tag", primaryjoin="parent_id==Tag.id")


# FIXME: incomplete
class ContentEditHistory(Base):
    __tablename__ = "content_edit_history"

    id          = Column(Integer(), primary_key=True)
    content_id  = Column(Integer(), ForeignKey('content.id'))
    member_id   = Column(Integer(), ForeignKey('member.id'))
    timestamp   = Column(DateTime())
    ip          = Column(postgresql.INET(), index=True)
    source      = Column(Unicode(250), doc="civicboom, mobile, another_webpage, other service")
    text_change = Column(UnicodeText())

    content     = relationship("Content", primaryjoin="content_id==Content.id")
    member      = relationship("Member", primaryjoin="member_id==Member.id")


_mime_types = [
    "application", "audio", "example", "image",
    "message", "model", "multipart", "text", "video"
]

class Media(Base):
    __tablename__ = "media"

    id          = Column(Integer(), primary_key=True)
    content_id  = Column(Integer(), ForeignKey('content.id'))
    name        = Column(UnicodeText(250))
    type        = Column(Enum(_mime_types), doc="MIME type, eg 'text', 'video'")
    subtype     = Column(String(32), doc="MIME subtype, eg 'jpeg', '3gpp'")
    hash        = Column(String(32), index=True) # FIXME: 32=md5? do we want md5?
    caption     = Column(UnicodeText())
    credit      = Column(UnicodeText())
    ip          = Column(postgresql.INET(), index=True)

    content     = relationship("Content", primaryjoin="content_id==Content.id")

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


class Message(Base):
    __tablename__ = "message"

    id          = Column(Integer(), primary_key=True)
    source_id   = Column(Integer(), ForeignKey('member.id'), nullable=True)
    target_id   = Column(Integer(), ForeignKey('member.id'), nullable=True)
    timestamp   = Column(DateTime())
    text        = Column(UnicodeText())

    source      = relationship("Member", primaryjoin="source_id==Member.id")
    target      = relationship("Member", primaryjoin="target_id==Member.id")


class Member(Base):
    "Abstract class"
    __tablename__ = "member"

    id            = Column(Integer(), primary_key=True)
    username      = Column(String(32), unique=True, index=True) # FIXME: check for invalid chars
    name          = Column(Unicode(250))
    join_date     = Column(Date())
    home_location = Column(Unicode(250), nullable=True, doc="Name of a location for informational purposes, eg 'London', 'Global', 'Wherever the sun shines'")
    description   = Column(UnicodeText())
    num_followers = Column(Integer()) #FIXME: derived
    webpage       = Column(Unicode())
    status        = Column(Enum(["active", "pending", "removed"]))
    avatar        = Column(String(32), doc="Hash of a static file on our mirrors; if null & group, use default; if null & user, use gravatar") # FIXME: 32=md5? do we want md5?


class User(Member):
    __tablename__ = "member_user"

    id               = Column(Integer(), ForeignKey('member.id'), primary_key=True)
    notification_check_timestamp = Column(DateTime())
    new_messages     = Column(Boolean()) # FIXME: derived
    location         = GISColumn(Point(), nullable=True, doc="Current location, for geo-targeted assignments. Nullable for privacy")
    location_updated = Column(DateTime())


class Group(Member):
    __tablename__ = "member_group"

    id               = Column(Integer(), ForeignKey('member.id'), primary_key=True)
    permissions_join = Column(Enum(["open", "invite_only"]), default="open")
    permissions_view = Column(Enum(["open", "members_only"]), default="open")
    behaviour        = Column(Enum(["normal", "education", "organisation"]), default="normal") # FIXME: document this
    num_members      = Column(Integer()) # FIXME: derived


class GroupMembership(Base):
    __tablename__ = "member_group_members"

    id          = Column(Integer(), primary_key=True)
    group_id    = Column(Integer(), ForeignKey('member.id'))
    member_id   = Column(Integer(), ForeignKey('member.id'))
    premissions = Column(Enum(["admin", "normal", "view_only"]), default="normal")

    group       = relationship("Member", primaryjoin="group_id==Member.id")
    member      = relationship("Member", primaryjoin="member_id==Member.id")


# FIXME: incomplete
#class MemberUserLogin(Base):
#    member      = Column(Integer(), ForeignKey('member.id'))
#    type (facebook, google, yahoo?)
#    password? id?


# FIXME: incomplete
#class MemberUserSettingsDetails(Base):
#    memberId
#    full name


# FIXME: incomplete
#class MemberUserSettingsPayment(Base):
#    memberId


# We need to potentially add additional tables to handle a range of
# aggregation plugins and other settings over time, we need a flexible /
# scalable / maintainable approach to this.

# FIXME: incomplete
#class MemberUserSettingsAggregationTwitter(Base):
#    memberId
#    OAuth token for twitter (we DO NOT want to store there password!!!!)


# FIXME: incomplete
#class MemberUserSettingsAggregationFacebook(Base):
#    memberId
#    OAuth token?


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


# relational magic should create these?

#class MemberFollow(Base):
#    memberId_follow
#    memberId_follower

#class ContentTag(Base)
#    tagId
#    contentId

#class BoomLog(Base):
#    userId
#    contentId

#class RatingLog(Base):
#    memberId
#    contentArticleId
#    rating




## Non-reflected tables may be defined and mapped at module level
#foo_table = sa.Table("Foo", meta.metadata,
#    sa.Column("id", sa.types.Integer, primary_key=True),
#    sa.Column("bar", sa.types.String(255), nullable=False),
#    )
#
#class Foo(object):
#    pass
#
#orm.mapper(Foo, foo_table)


## Classes for reflected tables may be defined here, but the table and
## mapping itself must be done in the init_model function
#reflected_table = None
#
#class Reflected(object):
#    pass
