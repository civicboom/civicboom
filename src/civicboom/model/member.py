
from civicboom.model.meta import Base

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String
from sqlalchemy import Enum, Integer, Date, DateTime, Boolean
from geoalchemy import GeometryColumn as Golumn, Point, GeometryDDL
from sqlalchemy.orm import relationship, backref

class Member(Base):
    "Abstract class"
    __tablename__   = "member"
    __type__        = Column(Enum("user", "group", name="member_type")) # FIXME: need full list
    __mapper_args__ = {'polymorphic_on': __type__}
    _member_status  = Enum("active", "pending", "removed", name="member_status")
    id              = Column(Integer(),      primary_key=True)
    username        = Column(String(32),     nullable=False, unique=True, index=True) # FIXME: check for invalid chars
    name            = Column(Unicode(250),   nullable=False  )
    join_date       = Column(Date(),         nullable=False, default="now()")
    home_location   = Column(Unicode(250),   nullable=True,  doc="Name of a location for informational purposes, eg 'London', 'Global', 'Wherever the sun shines'")
    description     = Column(UnicodeText(),  nullable=False, default=u"")
    num_followers   = Column(Integer(),      nullable=False, default=0) #FIXME: derived
    webpage         = Column(Unicode(),      nullable=False, default=u"")
    status          = Column(_member_status, nullable=False, default="active")
    avatar          = Column(String(32),     nullable=True,  doc="Hash of a static file on our mirrors; if null & group, use default; if null & user, use gravatar") # FIXME: 32=md5? do we want md5?
    created_content = relationship("Content", backref=backref('creator'))
#    parent_memberships = relationship("GroupMembership", backref=backref("members"))


class User(Member):
    __tablename__    = "member_user"
    __mapper_args__  = {'polymorphic_identity': 'user'}
    id               = Column(Integer(),  ForeignKey('member.id'), primary_key=True)
    last_message     = Column(DateTime(), nullable=False,   default="now()", doc="the last time the user saw a message")
    new_messages     = Column(Boolean(),  nullable=False,   default=False) # FIXME: derived
    location         = Golumn(Point(2),   nullable=True,    doc="Current location, for geo-targeted assignments. Nullable for privacy")
    location_updated = Column(DateTime(), nullable=False,   default="now()")


class Group(Member):
    __tablename__    = "member_group"
    __mapper_args__  = {'polymorphic_identity': 'group'}
    id               = Column(Integer(), ForeignKey('member.id'), primary_key=True)
    permissions_join = Column(Enum("open", "invite_only", name="group_permissions_join"), nullable=False, default="open")
    permissions_view = Column(Enum("open", "members_only", name="group_permissions_view"), nullable=False, default="open")
    behaviour        = Column(Enum("normal", "education", "organisation", name="group_behaviours"), nullable=False, default="normal") # FIXME: document this
    num_members      = Column(Integer()) # FIXME: derived

#    members          = relationship("GroupMembership", backref=backref("groups"))


class GroupMembership(Base):
    __tablename__ = "member_group_members"
    _gmp          = Enum("admin", "normal", "view_only", name="group_membership_permission")
    id            = Column(Integer(), primary_key=True)
    group_id      = Column(Integer(), ForeignKey('member.id'), nullable=False)
    member_id     = Column(Integer(), ForeignKey('member.id'), nullable=False)
    premissions   = Column(_gmp,      nullable=False, default="normal")


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

GeometryDDL(User.__table__)
