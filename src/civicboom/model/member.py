
from civicboom.model.meta import Base
from civicboom.model.message import Message

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String
from sqlalchemy import Enum, Integer, Date, DateTime, Boolean
from sqlalchemy import and_, null, func
from geoalchemy import GeometryColumn as Golumn, Point, GeometryDDL
from sqlalchemy.orm import relationship, backref, dynamic_loader

import urllib, hashlib


# many-to-many mappings need to be at the top, so that other classes can
# say "I am joined to other table X using mapping Y as defined above"

class GroupMembership(Base):
    __tablename__ = "map_user_to_group"
    _gmp          = Enum("admin", "normal", "view_only", name="group_membership_permission")
    group_id      = Column(Integer(), ForeignKey('member_group.id'), primary_key=True)
    member_id     = Column(Integer(), ForeignKey('member.id'), primary_key=True)
    premissions   = Column(_gmp,      nullable=False, default="normal")

class Follow(Base):
    __tablename__ = "map_member_to_follower"
    member_id     = Column(Integer(),    ForeignKey('member.id'), nullable=False, primary_key=True)
    follower_id   = Column(Integer(),    ForeignKey('member.id'), nullable=False, primary_key=True)


class Member(Base):
    "Abstract class"
    __tablename__   = "member"
    __type__        = Column(Enum("user", "group", name="member_type"))
    __mapper_args__ = {'polymorphic_on': __type__}
    _member_status  = Enum("pending", "active", "suspended", name="member_status")
    id              = Column(Integer(),      primary_key=True)
    username        = Column(String(32),     nullable=False, unique=True, index=True) # FIXME: check for invalid chars, see feature #54
    name            = Column(Unicode(250),   nullable=False, default=u"")
    join_date       = Column(Date(),         nullable=False, default=func.now())
    num_followers   = Column(Integer(),      nullable=False, default=0, doc="Controlled by postgres trigger")
    webpage         = Column(Unicode(),      nullable=True,  default=None)
    status          = Column(_member_status, nullable=False, default="pending")
    avatar          = Column(Unicode(250),   nullable=True)
    utc_offset      = Column(Integer(),      nullable=False, default=0)

    content_edits   = relationship("ContentEditHistory",  backref=backref('member', order_by=id))

    messages_to           = relationship("Message", primaryjoin=and_(Message.source_id!=null(), Message.target_id==id    ), backref=backref('target', order_by=id))
    messages_from         = relationship("Message", primaryjoin=and_(Message.source_id==id    , Message.target_id!=null()), backref=backref('source', order_by=id))
    messages_public       = relationship("Message", primaryjoin=and_(Message.source_id==id    , Message.target_id==null()) )
    messages_notification = relationship("Message", primaryjoin=and_(Message.source_id==null(), Message.target_id==id    ) )

    login_details        = relationship("UserLogin"       , backref=('user'), cascade="all,delete-orphan")
    groups               = relationship("Group"           , secondary=GroupMembership.__table__)
    followers            = relationship("Member"          , primaryjoin="Member.id==Follow.member_id"  , secondaryjoin="Member.id==Follow.follower_id", secondary=Follow.__table__)
    following            = relationship("Member"          , primaryjoin="Member.id==Follow.follower_id", secondaryjoin="Member.id==Follow.member_id"  , secondary=Follow.__table__)
    ratings              = relationship("Rating"          , backref=backref('member'), cascade="all,delete-orphan")
    flags                = relationship("FlaggedContent"  , backref=backref('member'), cascade="all,delete-orphan")
    feeds                = relationship("Feed"            , backref=backref('member'), cascade="all,delete-orphan")

    # Content relation shortcuts
    #content             = relationship(          "Content", backref=backref('creator'), primaryjoin=and_("Member.id==Content.creator_id") )# ,"Content.__type__!='comment'"  # cant get this to work, we want to filter out comments
    content_assignments = relationship("AssignmentContent")
    content_articles    = relationship(   "ArticleContent")
    content_drafts      = relationship(     "DraftContent")
    
    #See civicboom_init.py
    # content
    # content_assignments_active
    # content_assignments_previous
    # assignments_accepted = relationship("MemberAssignment", backref=backref("member"), cascade="all,delete-orphan")

    _config = None


    __to_dict__ = Base.__to_dict__.copy()
    __to_dict__.update({
        'list': {
            'id'                : None ,
            'name'              : None ,
            'username'          : None ,
            'avatar_url'        : None ,
        },
    })
    
    __to_dict__.update({
        'single': __to_dict__['list'].copy()
    })
    __to_dict__['single'].update({
            'num_followers'     : None ,
            'webpage'           : None ,
            'utc_offset'        : None ,
            'join_date'         : None ,
    })
    
    __to_dict__.update({
        'actions': __to_dict__['single'].copy()
    })
    __to_dict__['actions'].update({
            'following'        : lambda member: member.is_following(None), #c.logged_in_user
            'follower'         : lambda member: member.is_follower(None), #c.logged_in_user
            #'join' # join group?
    })


    @property
    def config(self):
        if not self._config:
            # import at the last minute -- importing at the start of the file
            # causes a dependency loop
            from civicboom.lib.settings import MemberSettingsManager
            self._config = MemberSettingsManager(self)
        return self._config

    def __unicode__(self):
        return self.name + " ("+self.username+")"

    def __str__(self):
        return unicode(self).encode('ascii', 'replace')

    def hash(self):
        h = hashlib.md5()
        for field in ("id","username","name","join_date","status","avatar","utc_offset"): #TODO: includes relationship fields in list?
            h.update(str(getattr(self,field)))
        return h.hexdigest()

    def send_message(self, m, delay_commit=False):
        import civicboom.lib.communication.messages as messages
        messages.send_message(self, m, delay_commit)

    def send_email(self, **kargs):
        from civicboom.lib.communication.email import send_email
        send_email(self, **kargs)

    def send_message_to_followers(self, m, delay_commit=False):
        for follower in self.followers:
            follower.send_message(m, delay_commit)

    def follow(self, member):
        from civicboom.lib.database.actions import follow
        return follow(self,member)
        
    def unfollow(self, member):
        from civicboom.lib.database.actions import unfollow
        return unfollow(self,member)

    def is_follower(self, member):
        if isinstance(member, basestring):
            follower_list = [m.username for m in self.followers]
        else:
            follower_list = self.followers
        return member in follower_list
    
    def is_following(self, member):
        if isinstance(member, basestring):
            following_list = [m.username for m in self.following]
        else:
            following_list = self.following
        return member in following_list

    @property
    def avatar_url(self, size=80):
        if self.avatar:
            return self.avatar
        return "/images/default_avatar.png"
    


class User(Member):
    __tablename__    = "member_user"
    __mapper_args__  = {'polymorphic_identity': 'user'}
    id               = Column(Integer(),  ForeignKey('member.id'), primary_key=True)
    last_check       = Column(DateTime(), nullable=False,   default=func.now(), doc="The last time the user checked their messages. You probably want to use the new_messages derived boolean instead.")
    new_messages     = Column(Boolean(),  nullable=False,   default=False) # FIXME: derived
    location         = Golumn(Point(2),   nullable=True,    doc="Current location, for geo-targeted assignments. Nullable for privacy")
    location_updated = Column(DateTime(), nullable=False,   default=func.now())
    #dob              = Column(DateTime(), nullable=True) # Needs to be stored in user settings but not nesiserally in the main db record
    email            = Column(Unicode(250), nullable=True)
    email_unverifyed = Column(Unicode(250), nullable=True)

    def __unicode__(self):
        return self.name + " ("+self.username+") (User)"

    def hash(self):
        h = hashlib.md5(Member.hash(self))
        for field in ("email",):
            h.update(str(getattr(self,field)))
        return h.hexdigest()

    @property
    def config(self):
        if not self._config:
            # import at the last minute -- importing at the start of the file
            # causes a dependency loop
            from civicboom.lib.settings import MemberSettingsManager
            self._config = MemberSettingsManager(self)
        return self._config

    @property
    def avatar_url(self, size=80):
        if self.avatar:
            return self.avatar
        #default = "http://www.civicboom.com/images/default_avatar.jpg"
        default = "identicon"
        hash = hashlib.md5(self.email.lower()).hexdigest()
        args = urllib.urlencode({'d':default, 's':str(size), 'r':"pg"})
        return "http://www.gravatar.com/avatar/%s?%s" % (hash, args)


class Group(Member):
    __tablename__    = "member_group"
    __mapper_args__  = {'polymorphic_identity': 'group'}
    id               = Column(Integer(), ForeignKey('member.id'), primary_key=True)
    permissions_join = Column(Enum("open", "invite_only", name="group_permissions_join"), nullable=False, default="open")
    permissions_view = Column(Enum("open", "members_only", name="group_permissions_view"), nullable=False, default="open")
    behaviour        = Column(Enum("normal", "education", "organisation", name="group_behaviours"), nullable=False, default="normal") # FIXME: document this
    num_members      = Column(Integer(), nullable=False, default=0, doc="Controlled by postgres trigger")
    members          = relationship("Member", secondary=GroupMembership.__table__)

    def __unicode__(self):
        return self.name + " ("+self.username+") (Group)"


class UserLogin(Base):
    __tablename__    = "member_user_login"
    id          = Column(Integer(),    primary_key=True)
    member_id   = Column(Integer(),    ForeignKey('member.id'))
    # FIXME: need full list; facebook, google, yahoo?
    #type        = Column(Enum("password", "openid", name="login_type"), nullable=False, default="password")
    type        = Column(String( 32),  nullable=False, default="password") # String because new login types could be added via janrain over time    
    token       = Column(String(250),  nullable=False)


class MemberSetting(Base):
    __tablename__    = "member_setting"
    member_id   = Column(Integer(),     ForeignKey('member.id'), primary_key=True)
    name        = Column(String(250),   primary_key=True)
    value       = Column(UnicodeText(), nullable=False)

    member      = relationship("Member", backref=backref('settings', cascade="all,delete-orphan"))


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
