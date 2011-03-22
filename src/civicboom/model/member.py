
from civicboom.model.meta import Base, location_to_string
from civicboom.model.message import Message
from civicboom.lib.misc import update_dict
from civicboom.lib.helpers import wh_url

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String, LargeBinary as Binary
from sqlalchemy import Enum, Integer, Date, DateTime, Boolean
from sqlalchemy import and_, null, func
from geoalchemy import GeometryColumn as Golumn, Point, GeometryDDL
from sqlalchemy.orm import relationship, backref, dynamic_loader
from sqlalchemy.schema import DDL

import urllib, hashlib, copy



# many-to-many mappings need to be at the top, so that other classes can
# say "I am joined to other table X using mapping Y as defined above"
member_type              = Enum("user", "group",                     name="member_type"  )
account_types            = Enum("free", "plus", "corp", "corp_plus", name="account_types")

group_member_roles_level =     ("admin", "editor", "contributor", "observer") # the order of permissions e.g admin has higher privilages than editor
group_member_roles       = Enum("admin", "editor", "contributor", "observer", name="group_member_roles")
group_member_status      = Enum("active", "invite", "request",                name="group_member_status")

group_join_mode          = Enum("public", "invite" , "invite_and_request",    name="group_join_mode")
group_member_visibility  = Enum("public", "private",                          name="group_member_visibility" )
group_content_visibility = Enum("public", "private",                          name="group_content_visibility")


def has_role_required(role_required, role_current):
    """
    returns 1 or more if has permissons
    returns 0 or less if not permissions
    """
    try:
        permission_index_required = group_member_roles_level.index(role_required)
        permission_index_current  = group_member_roles_level.index(role_current)
        return permission_index_required - permission_index_current + 1
    except:
        return 0


class GroupMembership(Base):
    __tablename__ = "map_user_to_group"
    group_id      = Column(Integer(), ForeignKey('member_group.id'), primary_key=True)
    member_id     = Column(Integer(), ForeignKey('member.id')      , primary_key=True)
    role          = Column(group_member_roles , nullable=False, default="contributor")
    status        = Column(group_member_status, nullable=False, default="active")

DDL('DROP TRIGGER IF EXISTS update_group_size ON map_user_to_group').execute_at('before-drop', GroupMembership.__table__)
DDL("""
CREATE OR REPLACE FUNCTION update_group_size() RETURNS TRIGGER AS $$
    DECLARE
        tmp_group_id integer;
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            tmp_group_id := NEW.group_id;
        ELSIF (TG_OP = 'UPDATE') THEN
            IF (NEW.member_id != OLD.member_id OR NEW.group_id != OLD.group_id) THEN
                RAISE EXCEPTION 'Can only alter membership types, not relations';
            END IF;
            tmp_group_id := NEW.group_id;
        ELSIF (TG_OP = 'DELETE') THEN
            tmp_group_id := OLD.group_id;
        END IF;

        UPDATE member_group SET num_members = (
            SELECT count(*)
            FROM map_user_to_group
            WHERE group_id=tmp_group_id
        ) WHERE id=tmp_group_id;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_group_size
    AFTER INSERT OR UPDATE OR DELETE ON map_user_to_group
    FOR EACH ROW EXECUTE PROCEDURE update_group_size();
""").execute_at('after-create', GroupMembership.__table__)


class Follow(Base):
    __tablename__ = "map_member_to_follower"
    member_id     = Column(Integer(),    ForeignKey('member.id'), nullable=False, primary_key=True)
    follower_id   = Column(Integer(),    ForeignKey('member.id'), nullable=False, primary_key=True)

DDL('DROP TRIGGER IF EXISTS update_follower_count ON map_member_to_follower').execute_at('before-drop', Follow.__table__)
DDL("""
CREATE OR REPLACE FUNCTION update_follower_count() RETURNS TRIGGER AS $$
    DECLARE
        tmp_member_id integer;
        tmp_follower_id integer;
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            tmp_member_id   := NEW.member_id;
            tmp_follower_id := NEW.follower_id;
        ELSIF (TG_OP = 'UPDATE') THEN
            RAISE EXCEPTION 'Can''t alter follows, only add or remove';
        ELSIF (TG_OP = 'DELETE') THEN
            tmp_member_id   := OLD.member_id;
            tmp_follower_id := OLD.follower_id;
        END IF;

        UPDATE member SET num_followers = (
            SELECT count(*)
            FROM map_member_to_follower
            WHERE member_id=tmp_member_id
        ) WHERE id=tmp_member_id;
        
        UPDATE member SET num_following = (
            SELECT count(*)
            FROM map_member_to_follower
            WHERE follower_id=tmp_follower_id
        ) WHERE id=tmp_follower_id;
        
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_follower_count
    AFTER INSERT OR UPDATE OR DELETE ON map_member_to_follower
    FOR EACH ROW EXECUTE PROCEDURE update_follower_count();
""").execute_at('after-create', Follow.__table__)


def _generate_salt():
    import os
    return os.urandom(256)


class Member(Base):
    "Abstract class"
    __tablename__   = "member"
    __type__        = Column(member_type)
    __mapper_args__ = {'polymorphic_on': __type__}
    _member_status  = Enum("pending", "active", "suspended", name="member_status")
    id              = Column(Integer(),      primary_key=True)
    username        = Column(String(32),     nullable=False, unique=True, index=True) # FIXME: check for invalid chars, see feature #54
    name            = Column(Unicode(250),   nullable=False, default=u"")
    join_date       = Column(Date(),         nullable=False, default=func.now())
    status          = Column(_member_status, nullable=False, default="pending")
    avatar          = Column(String(40),     nullable=True)
    utc_offset      = Column(Integer(),      nullable=False, default=0)
    location_home   = Golumn(Point(2),       nullable=True)
    payment_account_id = Column(Integer(),   ForeignKey('payment_account.id'), nullable=True)
    salt            = Column(Binary(length=256), nullable=False, default=_generate_salt)

    num_following            = Column(Integer(), nullable=False, default=0, doc="Controlled by postgres trigger")
    num_followers            = Column(Integer(), nullable=False, default=0, doc="Controlled by postgres trigger")
    num_unread_messages      = Column(Integer(), nullable=False, default=0, doc="Controlled by postgres trigger")
    num_unread_notifications = Column(Integer(), nullable=False, default=0, doc="Controlled by postgres trigger")
    # AllanC - TODO - derived field trigger needed
    #account_type             = Column(account_types, nullable=False, default='free', doc="Controlled by postgres trigger")

    content_edits   = relationship("ContentEditHistory",  backref=backref('member', order_by=id))

    payment_account       = relationship("PaymentAccount", cascade="delete,delete-orphan", single_parent=True) #AllanC - TODO: Double check the delete cascade, we dont want to delete the account unless no other links to the payment record exist

    groups_roles         = relationship("GroupMembership" , backref="member", cascade="all,delete-orphan", lazy='joined') #AllanC- TODO: needs eagerload group? does lazy=joined do it?
    ratings              = relationship("Rating"          , backref=backref('member'), cascade="all,delete-orphan")
    flags                = relationship("FlaggedContent"  , backref=backref('member'), cascade="all,delete-orphan")
    feeds                = relationship("Feed"            , backref=backref('member'), cascade="all,delete-orphan")

    # AllanC - I wanted to remove these but they are still used by actions.py because they are needed to setup the base test data
    followers            = relationship("Member"          , primaryjoin="Member.id==Follow.member_id"  , secondaryjoin="Member.id==Follow.follower_id", secondary=Follow.__table__)
    following            = relationship("Member"          , primaryjoin="Member.id==Follow.follower_id", secondaryjoin="Member.id==Follow.member_id"  , secondary=Follow.__table__)

    assigments           = relationship("MemberAssignment", backref=backref("member"), cascade="all,delete-orphan")

    # Content relation shortcuts
    #content             = relationship(          "Content", backref=backref('creator'), primaryjoin=and_("Member.id==Content.creator_id") )# ,"Content.__type__!='comment'"  # cant get this to work, we want to filter out comments
    
    #content_assignments = relationship("AssignmentContent")
    #content_articles    = relationship(   "ArticleContent")
    #content_drafts      = relationship(     "DraftContent")
    
    #See civicboom_init.py
    # content
    # content_assignments_active
    # content_assignments_previous
    # assignments_accepted = relationship("MemberAssignment", backref=backref("member"), cascade="all,delete-orphan")
    #interests = relationship("")

    #messages_to           = relationship("Message", primaryjoin=and_(Message.source_id!=null(), Message.target_id==id    ), backref=backref('target', order_by=id))
    #messages_from         = relationship("Message", primaryjoin=and_(Message.source_id==id    , Message.target_id!=null()), backref=backref('source', order_by=id))
    #messages_public       = relationship("Message", primaryjoin=and_(Message.source_id==id    , Message.target_id==null()) )
    #messages_notification = relationship("Message", primaryjoin=and_(Message.source_id==null(), Message.target_id==id    ) )

    #groups               = relationship("Group"           , secondary=GroupMembership.__table__) # Could be reinstated with only "active" groups, need to add criteria


    _config = None

    __to_dict__ = copy.deepcopy(Base.__to_dict__)
    __to_dict__.update({
        'default': {
            'id'                : None ,
            'name'              : None ,
            'username'          : None ,
            'avatar_url'        : None ,
            'type'              : lambda member: member.__type__ ,
            'location_home'     : lambda member: location_to_string(member.location_home) ,
            'num_followers'     : None ,
            'num_following'     : None ,
            'account_type'      : None ,
        },
    })
    
    __to_dict__.update({
        'full': copy.deepcopy(__to_dict__['default'])
    })
    __to_dict__['full'].update({
            'num_followers'       : None ,
            'utc_offset'          : None ,
            'join_date'           : None ,
            'website'             : lambda member: member.config.get('website') ,
            'description'         : lambda member: member.config.get('description') ,
            #'url'                 : None ,
            
            #'followers'           : lambda member: [m.to_dict() for m in member.followers            ] ,
            #'following'           : lambda member: [m.to_dict() for m in member.following            ] ,
            #'messages_public'     : lambda member: [m.to_dict() for m in member.messages_public[:5]  ] ,
            #'assignments_accepted': lambda member: [a.to_dict() for a in member.assignments_accepted if a.private==False] ,
            #'content_public'      : lambda member: [c.to_dict() for c in member.content_public       ] ,
            #'groups_public'       : lambda member: [update_dict(gr.group.to_dict(),{'role':gr.role}) for gr in member.groups_roles if gr.status=="active" and gr.group.member_visibility=="public"] ,  #AllanC - also duplicated in members_actions.groups ... can this be unifyed
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
        return self.name or self.username

    def __str__(self):
        return unicode(self).encode('ascii', 'replace')
    
    def __link__(self):
        from civicboom.lib.web import url
        return url('member', id=self.id, subdomain='', absolute=True)

    def hash(self):
        h = hashlib.md5()
        for field in ("id","username","name","join_date","status","avatar","utc_offset"): #TODO: includes relationship fields in list?
            h.update(str(getattr(self,field)))
        return h.hexdigest()

    def action_list_for(self, member):
        action_list = []
        #if self.can_message(member):
        #    action_list.append('editable')
        if self == member:
            action_list.append('settings')
            action_list.append('logout')
        if member and member.is_following(self):
            action_list.append('unfollow')
        else:
            if self != member:
                action_list.append('follow')
        if self != member:
            action_list.append('message')
            if member and member.__type__ == 'group'  and not member.get_membership(self):
                action_list.append('invite')
        return action_list

    def send_message(self, m, delay_commit=False):
        import civicboom.lib.communication.messages as messages
        messages.send_message(self, m, delay_commit)

    def send_email(self, **kargs):
        from civicboom.lib.communication.email_lib import send_email
        send_email(self, **kargs)

    def send_message_to_followers(self, m, delay_commit=False):
        for follower in self.followers:
            follower.send_message(m, delay_commit)

    def follow(self, member, delay_commit=False):
        from civicboom.lib.database.actions import follow
        return follow(self, member, delay_commit=delay_commit)
        
    def unfollow(self, member, delay_commit=False):
        from civicboom.lib.database.actions import unfollow
        return unfollow(self, member, delay_commit=delay_commit)

    def is_follower(self, member):
        #if not member:
        #    return False
        #from civicboom.controllers.members import MembersController
        #member_search = MembersController().index
        #return bool(member_search(member=self, followed_by=member)['data']['list']['count'])
        from civicboom.lib.database.actions import is_follower
        return is_follower(self, member)
    
    def is_following(self, member):
        #if not member:
        #    return False
        #from civicboom.controllers.members import MembersController
        #member_search = MembersController().index
        #return bool(member_search(member=self, follower_of=member)['data']['list']['count'])
        from civicboom.lib.database.actions import is_follower
        return is_follower(member, self)

    @property
    def url(self):
        from civicboom.lib.web import url
        return url('member', id=self.username, absolute=True)

    @property
    def avatar_url(self, size=80):
        if self.avatar:
            return wh_url("avatars", self.avatar)
        return wh_url("public", "images/default/avatar.png")

    def delete(self):
        from civicboom.lib.database.actions import del_member
        return del_member(self)

    def add_to_interests(self, content):
        from civicboom.lib.database.actions import add_to_interests
        return add_to_interests(self, content)
    
    def has_permission(self, required_account_type):
        member_account_type = self.account_type
        #AllanC TODO: This may need updating to use something more sophisticated than just monkey if statements
        #             need > ... we want corp customers to do what the plus customers can do
        if required_account_type == member_account_type:
            return True
        #return False
        return True # lizze needs to demo plus features on a newly created account...

    
    def can_publish_assignment(self):
        # AllanC - could be replaced with some form of 'get_permission('publish') ??? we could have lots of permissiong related methods ... just a thought
        #from civicboom.lib.civicboom_lib import can_publish_assignment
        #return can_publish_assignment(self)
        #AllanC - TODO - check member payment level to acertain what the limit is - set limit to this users level
        # if not member.payment_level:
        
        limit = None
        account_type = self.account_type
        
        from pylons import config
        if account_type == 'free':
            limit = config['payment.free.assignment_limit']
        elif account_type == 'plus':
            limit = config['payment.plus.assignment_limit']
            
        if not limit:
            return True
        if len(self.active_assignments_period) > limit:
            return False
        return True

    #@property
    #def payment_account(self):
    #    return self._payment_account
    #@payment_account.setter
    def set_payment_account(self, value, delay_commit=False):
        #self._payment_account = value
        from civicboom.lib.database.actions import set_payment_account
        set_payment_account(self, value, delay_commit)
    @property
    # AllanC - TODO this needs to be a derrived field
    def account_type(self):
        if self.payment_account and self.payment_account.type:
            return self.payment_account.type
        return 'free'

    def check_action_key(self, action, key):
        """
        Check that this member was the one who generated the key to
        the specified action.
        """
        return (key == self.get_action_key(action))

    def get_action_key(self, action):
        """
        Generate a key, anyone with this key is allowed to perform
        $action on behalf of this member.

        The key is the hash of (member.id, action, member.salt).
        Member.id is included because while the salt *should* be
        unique, the ID *is* unique by definition.

        The salt should be kept secret by the server, not even shown
        to the user who owns it -- thus when presented with a key,
        we can guarantee that this server is the one who generated
        it. If the key for a user/action pair is only given to that
        user after they've authenticated, then we can guarantee that
        anyone with that key has been given it by the user.


        Usage:
        ~~~~~~
        Alice:
            key = alice.get_action_key('read article 42')
            bob.send_message("Hey bob, if you want to read article 42, "+
                             "tell the system I gave you this key: "+key)

        Bob:
            api.content.show(42, auth=(alice, key))

        System:
            wanted_content = get_content(42)
            claimed_user = get_member(alice)
            if key == claimed_user.get_action_key('read article '+wanted_content.id):
                print(wanted_content)
        """
        return hashlib.sha1(str(self.id)+action+self.salt).hexdigest()

GeometryDDL(Member.__table__)


class User(Member):
    __tablename__    = "member_user"
    __mapper_args__  = {'polymorphic_identity': 'user'}
    id               = Column(Integer(),  ForeignKey('member.id'), primary_key=True)
    last_check       = Column(DateTime(), nullable=False,   default=func.now(), doc="The last time the user checked their messages. You probably want to use the new_messages derived boolean instead.")
    new_messages     = Column(Boolean(),  nullable=False,   default=False) # FIXME: derived
    location_current = Golumn(Point(2),   nullable=True,    doc="Current location, for geo-targeted assignments. Nullable for privacy")
    location_updated = Column(DateTime(), nullable=False,   default=func.now())
    #dob              = Column(DateTime(), nullable=True) # Needs to be stored in user settings but not nesiserally in the main db record
    email            = Column(Unicode(250), nullable=True)
    email_unverified = Column(Unicode(250), nullable=True)

    login_details    = relationship("UserLogin", backref=('user'), cascade="all,delete-orphan")

    __to_dict__ = copy.deepcopy(Member.__to_dict__)
    _extra_user_fields = {
        'location_current' : lambda member: location_to_string(member.location_home) ,
        'location_updated' : None ,
    }
    __to_dict__['default'     ].update(_extra_user_fields)
    __to_dict__['full'        ].update(_extra_user_fields)



    def __unicode__(self):
        return self.name or self.username

    def hash(self):
        h = hashlib.md5(Member.hash(self))
        for field in ("email",):
            h.update(str(getattr(self,field)))
        for login in self.login_details:
            h.update(login.token)
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
            return wh_url("avatars", self.avatar)
        email = self.email or self.email_unverified
        if email:
            hash    = hashlib.md5(email.lower()).hexdigest()
            default = "identicon"
            #default = "http://www.civicboom.com/images/default/avatar.jpg"
            args    = urllib.urlencode({'d':default, 's':str(size), 'r':"pg"})
            return "https://secure.gravatar.com/avatar/%s?%s" % (hash, args)
        return Member.avatar_url

DDL('DROP TRIGGER IF EXISTS update_location_time ON member_user').execute_at('before-drop', User.__table__)
GeometryDDL(User.__table__)
DDL("""
CREATE OR REPLACE FUNCTION update_location_time() RETURNS TRIGGER AS $$
    BEGIN
        UPDATE member_user SET location_updated = now() WHERE id=NEW.id;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_location_time
    AFTER UPDATE ON member_user
    FOR EACH ROW
    WHEN (OLD.location_current IS DISTINCT FROM NEW.location_current)
    EXECUTE PROCEDURE update_location_time();
""").execute_at('after-create', User.__table__)



class Group(Member):
    __tablename__      = "member_group"
    __mapper_args__    = {'polymorphic_identity': 'group'}
    id                         = Column(Integer(), ForeignKey('member.id'), primary_key=True)
    join_mode                  = Column(group_join_mode         , nullable=False, default="invite")
    member_visibility          = Column(group_member_visibility , nullable=False, default="public")
    default_content_visibility = Column(group_content_visibility, nullable=False, default="public")
    #behaviour                  = Column(Enum("normal", "education", "organisation", name="group_behaviours"), nullable=False, default="normal") # FIXME: document this
    default_role               = Column(group_member_roles, nullable=False, default="contributor")
    # AllanC: TODO - num_mumbers postgress trigger needs updating, we only want to show GroupMembership.status=="active" in the count
    num_members                = Column(Integer(), nullable=False, default=0, doc="Controlled by postgres trigger")
    #members                    = relationship("Member", secondary=GroupMembership.__table__)
    members_roles              = relationship("GroupMembership", backref="group", cascade="all,delete-orphan", lazy='joined')
    

    def __unicode__(self):
        return self.name or self.username

    @property
    def num_admins(self):
        return len([m for m in self.members_roles if m.role=="admin"]) #Count be optimised with Session.query....limit(2).count()?


    __to_dict__ = copy.deepcopy(Member.__to_dict__)
    _extra_group_fields = {
        'join_mode'                 : None ,
        'member_visibility'         : None ,
        'default_content_visibility': None ,
        'default_role'              : None ,
        'num_members'               : lambda group: group.num_members if group.member_visibility=="public" else None ,
    }
    __to_dict__['default'].update(_extra_group_fields)
    __to_dict__['full'   ].update(_extra_group_fields)



    # Private admin integrity helper - used in set_role and remove_member
    def _check_last_admin(self, member=None, membership=None):
        if not membership:
            membership = self.get_membership(member)
        if membership and membership.role=="admin" and self.num_admins<=1:
            from civicboom.lib.web import action_error
            raise action_error('cannot remove last admin', code=400)
    
    def action_list_for(self, member):
        action_list = Member.action_list_for(self, member)
        membership = self.get_membership(member)
        join = self.can_join(member, membership)
        if member and (join=="join" or join=="request"):
            action_list.append(join)
        else:
            if self.is_admin(member, membership):
                action_list.append('delete')
                action_list.append('remove') #AllanC - could be renamed? this means remove member?
                action_list.append('set_role')
                action_list.append('settings_group')
                if self.num_admins>1:
                    action_list.append('remove_self')
                    action_list.append('set_role_self')
            else:
                action_list.append('remove_self')
        return action_list


    def is_admin(self, member, membership=None):
        if not member:
            return False
        if self.username == member.username: #originaly self==member but wasnt sure if SQL alchemy calculates equality, they could have differnt object references
            return True
        if not membership:
            membership = self.get_membership(member)
        if membership and membership.member_id==member.id and membership.status=="active" and membership.role=="admin":
            return True
        return False

    def can_join(self, member, membership=None):
        if member==self:
            return False
        if not membership:
            membership = self.get_membership(member)
        if not membership:
            if self.join_mode=="public":
                return "join"
            if self.join_mode=="invite_and_request":
                return "request"
        elif membership.member_id==member.id and membership.status=="invite":
            return "join"
        return False

    def get_membership(self, member):
        from civicboom.lib.database.get_cached import get_membership
        return get_membership(self, member)

    def join(self, member, delay_commit=False):
        from civicboom.lib.database.actions import join_group
        return join_group(self, member, delay_commit=delay_commit)
        
    def remove_member(self, member, delay_commit=False):
        from civicboom.lib.database.actions import remove_member
        self._check_last_admin(member) # Check admin integrity
        return remove_member(self, member, delay_commit=delay_commit)
    
    def invite(self, member, role=None, delay_commit=False):
        from civicboom.lib.database.actions import invite
        return invite(self, member, role, delay_commit=delay_commit)
        
    def set_role(self, member, role, delay_commit=False):
        from civicboom.lib.database.actions import set_role
        self._check_last_admin(member) # Check admin integrity
        return set_role(self, member, role, delay_commit=delay_commit)
    
    def delete(self):
        from civicboom.lib.database.actions import del_group
        return del_group(self)
    

class UserLogin(Base):
    __tablename__    = "member_user_login"
    id          = Column(Integer(),    primary_key=True)
    member_id   = Column(Integer(),    ForeignKey('member.id'), index=True)
    # FIXME: need full list; facebook, google, yahoo?
    #type        = Column(Enum("password", "openid", name="login_type"), nullable=False, default="password")
    type        = Column(String( 32),  nullable=False, default="password") # String because new login types could be added via janrain over time
    token       = Column(String(250),  nullable=False)


class MemberSetting(Base):
    __tablename__    = "member_setting"
    member_id   = Column(Integer(),     ForeignKey('member.id'), primary_key=True, index=True)
    name        = Column(String(250),   primary_key=True)
    value       = Column(UnicodeText(), nullable=False)

    member      = relationship("Member", backref=backref('settings', cascade="all,delete-orphan"))


class PaymentAccount(Base):
    __tablename__    = "payment_account"
    id          = Column(Integer(), primary_key=True)
    type        = Column(account_types, nullable=True, default="free")
    
    
    
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
