
from civicboom.model.meta import Base

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String
from sqlalchemy import Enum, Integer, Date, DateTime, Boolean
from geoalchemy import GeometryColumn, Point, GeometryDDL
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql

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
    status        = Column(Enum("active", "pending", "removed", name="member_statuses"))
    avatar        = Column(String(32), doc="Hash of a static file on our mirrors; if null & group, use default; if null & user, use gravatar") # FIXME: 32=md5? do we want md5?


class User(Member):
    __tablename__ = "member_user"

    id               = Column(Integer(), ForeignKey('member.id'), primary_key=True)
    notification_check_timestamp = Column(DateTime())
    new_messages     = Column(Boolean()) # FIXME: derived
    location         = GeometryColumn(Point(2), nullable=True, doc="Current location, for geo-targeted assignments. Nullable for privacy")
    location_updated = Column(DateTime())


class Group(Member):
    __tablename__ = "member_group"

    id               = Column(Integer(), ForeignKey('member.id'), primary_key=True)
    permissions_join = Column(Enum("open", "invite_only", name="group_permissions_join"), default="open")
    permissions_view = Column(Enum("open", "members_only", name="group_permissions_view"), default="open")
    behaviour        = Column(Enum("normal", "education", "organisation", name="group_behaviours"), default="normal") # FIXME: document this
    num_members      = Column(Integer()) # FIXME: derived


class GroupMembership(Base):
    __tablename__ = "member_group_members"

    id          = Column(Integer(), primary_key=True)
    group_id    = Column(Integer(), ForeignKey('member.id'))
    member_id   = Column(Integer(), ForeignKey('member.id'))
    premissions = Column(Enum("admin", "normal", "view_only", name="group_membership_permissions"), default="normal")

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

GeometryDDL(User.__table__)
