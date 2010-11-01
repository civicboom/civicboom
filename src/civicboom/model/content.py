
from civicboom.model.meta import Base
from civicboom.model.member import Member
from civicboom.model.media import Media

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String
from sqlalchemy import Enum, Integer, Date, DateTime, Boolean, Float
from geoalchemy import GeometryColumn, Point, GeometryDDL
from sqlalchemy import and_, or_, func
from sqlalchemy.orm import relationship, backref

import hashlib
import copy
from webhelpers.text import truncate

#-------------------------------------------------------------------------------
# Enumerated Types
#-------------------------------------------------------------------------------
_content_type = Enum("comment", "draft", "article", "assignment", "syndicate", name="content_type")


#-------------------------------------------------------------------------------
# Objects
#-------------------------------------------------------------------------------

# many-to-many mappings need to be at the top, so that other classes can
# say "I am joined to other table X using mapping Y as defined above"

class ContentTagMapping(Base):
    __tablename__ = "map_content_to_tag"
    content_id    = Column(Integer(),    ForeignKey('content.id'), nullable=False, primary_key=True)
    tag_id        = Column(Integer(),    ForeignKey('tag.id')    , nullable=False, primary_key=True)

class Boom(Base):
    __tablename__ = "map_booms"
    content_id    = Column(Integer(),    ForeignKey('content_user_visible.id'), nullable=False, primary_key=True)
    member_id     = Column(Integer(),    ForeignKey('member.id')              , nullable=False, primary_key=True)

class Rating(Base):
    __tablename__ = "map_ratings"
    content_id    = Column(Integer(),    ForeignKey('content_user_visible.id'), nullable=False, primary_key=True)
    member_id     = Column(Integer(),    ForeignKey('member.id')              , nullable=False, primary_key=True)
    rating        = Column(Integer(),    nullable=False, default=0)

class Interest(Base):
    __tablename__ = "map_interest"
    content_id    = Column(Integer(),    ForeignKey('content_user_visible.id'), nullable=False, primary_key=True)
    member_id     = Column(Integer(),    ForeignKey('member.id')              , nullable=False, primary_key=True)


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
    __type__        = Column(_content_type, nullable=False)
    __mapper_args__ = {'polymorphic_on': __type__}
    #_visiability = Enum("pending", "show", name="content_")
    _edit_lock   = Enum("parent_owner", "group", "system", name="edit_lock_level")
    id              = Column(Integer(),        primary_key=True)
    title           = Column(Unicode(250),     nullable=False, default=u"Untitled")
    content         = Column(UnicodeText(),    nullable=False, default=u"", doc="The body of text")
    creator_id      = Column(Integer(),        ForeignKey('member.id'), nullable=False)
    parent_id       = Column(Integer(),        ForeignKey('content.id'), nullable=True)
    location        = GeometryColumn(Point(2), nullable=True   ) # FIXME: area rather than point? AllanC - Point for now, need to consider referenceing polygon areas in future? (more research nedeed)
    creation_date   = Column(DateTime(),       nullable=False, default=func.now())
    update_date     = Column(DateTime(),       nullable=False, default=func.now(), doc="Controlled by postgres trigger")
    private         = Column(Boolean(),        nullable=False, default=False, doc="see class doc")
    license_id      = Column(Integer(),        ForeignKey('license.id'), nullable=False, default=1)
    
    visable         = Column(Boolean(),        nullable=False, default=True)
    edit_lock       = Column(_edit_lock,       nullable=True , default=None)

    num_responses   = Column(Integer(),        nullable=False, default=0) # Derived field - see postgress trigger
    num_comments    = Column(Integer(),        nullable=False, default=0) # Derived field - see postgress trigger
    
    # FIXME: remote_side is confusing, and do we want to cascade to delete replies?
    # AllanC - see civicboom_init.py for 'responsese'
    #responses       = relationship("Content",            backref=backref('parent', remote_side=id, order_by=creation_date), primaryjoin=and_("Content.id == Content.parent_id") )  #, cascade="all" AllanC - coulbe be dangerious, may need to consider more carefully delete behaviour for differnt types of content
                                   #,or_("Content.__type__!='comment'","Content.__type__!='draft'")    # foreign_keys=["Content.id"]
    
    parent          = relationship("Content", primaryjoin=parent_id==id, remote_side=id)
    creator         = relationship("Member" , primaryjoin="Content.creator_id==Member.id")
    
    attachments     = relationship("Media",              backref=backref('attached_to'), cascade="all,delete-orphan")
    edits           = relationship("ContentEditHistory", backref=backref('content', order_by=id), cascade="all,delete-orphan")
    tags            = relationship("Tag",                secondary=ContentTagMapping.__table__)
    license         = relationship("License")

    comments        = relationship("CommentContent", order_by=creation_date.asc(), cascade="all", primaryjoin="CommentContent.id == Content.parent_id") #, cascade="all" AllanC - coulbe be dangerious, may need to consider more carefully delete behaviour for differnt types of content    
    flags           = relationship("FlaggedContent", backref=backref('content'), cascade="all,delete-orphan")

    # used by obj_to_dict to create a string dictonary representation of this object
    __to_dict__ = copy.deepcopy(Base.__to_dict__)
    __to_dict__.update({
        'default': {
            'id'           : None ,
            'type'         : lambda content: content.__type__ ,
            #'status'       : None ,
            'parent_id'    : None ,
            'title'        : None ,
            'content_short': None ,
            'creator_id'   : None , 
            'url'          : None ,
            'thumbnail_url': None ,
            'creation_date': None ,
            'location'     : lambda content: content.location_string ,
            'num_responses': None ,
            'num_comments' : None ,
            'tags'         : lambda content: "implement tags" ,
            'license_id'   : None ,
            'private'      : None ,
            'edit_lock'    : None ,
        },
    })
    
    # Single Content Item
    __to_dict__.update({
        'full': copy.deepcopy(__to_dict__['default'])
    })
    __to_dict__['full'].update({
            'content'           : None ,
            'parent'            : lambda content: content.parent.to_dict(include_fields='creator') if content.parent else None ,
            'creator'           : lambda content: content.creator.to_dict() ,
            'attachments'       : lambda content: [   media.to_dict(                        ) for media    in content.attachments] ,
            'responses'         : lambda content: [response.to_dict(include_fields='creator') for response in content.responses  ] ,
            'comments'          : lambda content: [ comment.to_dict(                        ) for comment  in content.comments   ] ,
            'license'           : lambda content: content.license.to_dict() , 
    })
    del __to_dict__['full']['content_short']
    del __to_dict__['full']['parent_id']
    del __to_dict__['full']['license_id']
    del __to_dict__['full']['creator_id']
    
    
    # Actions
    __to_dict__.update({
        'full+actions': copy.deepcopy(__to_dict__['full'])
    })
    def __to_dict_function_action_list__(content):
        from pylons import tmpl_context as c
        return content.action_list_for(c.logged_in_persona)
    __to_dict__['full+actions'].update({
            'actions': __to_dict_function_action_list__
    })

    
    def __unicode__(self):
        return self.title + u" (" + self.__type__ + u")"

    def __link__(self):
        from pylons import url, app_globals
        return url('content', id=self.id, host=app_globals.site_host)

    def clone(self, content):
        if content and content.id:
            for field in ["title","content","creator","parent_id","location","creation_date","private","license_id"]:
                setattr(self,field,getattr(content,field))

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

    def action_list_for(self, member):
        action_list = []
        if self.editable_by(member):
            action_list.append('edit')
        if self.viewable_by(member):
            action_list.append('view')
        return action_list

    def editable_by(self, member):
        """
        Check to see if a member object has the rights to edit this content
        """
        if self.edit_lock:
            return False
        if self.creator == member  :
            return True
        # TODO check groups of creator to see if member is in the owning group
        return False

    def viewable_by(self, member):
        """
        Check to see if a member object has the rights to view this content
        """
        # TODO check groups of creator to see if member is in the owning group
        if self.editable_by(member):
            return True # Always allow content to be viewed by owners/editors
        if self.__type__ == "draft":
            return False # if draft, only editors (above) can see
        if self.__type__ == "comment":
            return self.parent.viewable_by(member) # if comment, show if we can see the parent article
        if self.visable == True:
            return True
        return False

    def flag(self, **kargs):
        """
        Flag content as offensive or spam (can throw exception if fails)
        """
        from civicboom.lib.database.actions import flag_content
        flag_content(self, **kargs)
    
    def delete(self):
        """
        Delete the content from the DB, this will cause all cascade behaviour to take place
        Be very sure you want to do this!
        """
        from civicboom.lib.database.actions import del_content
        del_content(self)

    def aggregate_via_creator(self):
        """
        Aggregate a summary of this content to Twitter, Facebook, LinkedIn, etc via the content creators user account
        """
        from civicboom.lib.civicboom_lib import aggregate_via_user
        if self.__type__ == 'article' or self.__type__ == 'assignment':
            return aggregate_via_user(self, self.creator)
    
    
    @property
    def thumbnail_url(self):
        """
        TODO
        If there is media attached return the first image?
        if no media, check content for youtube video and get thumbnail from that? (maybe process this before content commit?)
        else return the default image url: (could vary depending on type?)
        
        This should be saved in the DB as thumbnail_url as a shortcut!
        """
        for media in self.attachments:
            thumbnail_url = media.thumbnail_url
            if thumbnail_url and thumbnail_url!="":
                return thumbnail_url

        from civicboom.lib.helpers import wh_public
        thumbnail_type = self.__type__
        if thumbnail_type=='article' and self.response_type != None:
            thumbnail_type = 'response'
        return wh_public("images/default_thumbnail_%s.png" % thumbnail_type)

    @property
    def url(self):
        from pylons import url, app_globals
        return url('content', host=app_globals.site_host, id=self.id)

    @property
    def content_short(self):
        return truncate(self.content, length=100)

    @property
    def location_string(self):
        if self.location:
            from civicboom.model.meta import Session
            return '%s %s' % (self.location.coords(Session)[1], self.location.coords(Session)[0])
        return None
        # AllanC Note: duplicated for Member location ... could we have location_string in a common place?
    

class DraftContent(Content):
    __tablename__   = "content_draft"
    __mapper_args__ = {'polymorphic_identity': 'draft'}
    id              = Column(Integer(), ForeignKey('content.id'), primary_key=True)
    target_type     = Column(_content_type, nullable=True, default=None)
    #publish_id      = Column(Integer(), nullable=True, doc="if present will overwite the published content with this draft")

    def __init__(self):
        self.private = True

    def clone(self, content):
        Content.clone(self, content)
        self.publish_id = content.id


class CommentContent(Content):
    __tablename__   = "content_comment"
    __mapper_args__ = {'polymorphic_identity': 'comment'}
    id              = Column(Integer(), ForeignKey('content.id'), primary_key=True)

    __to_dict__ = {} #Content.__to_dict__.copy()
    __to_dict__['default'] = {
        'creator'      : lambda content: content.creator.to_dict('default') ,
        'content'      : None ,
        'creation_date': None ,
    }
    __to_dict__['full']         = copy.deepcopy(__to_dict__['default'])
    __to_dict__['full+actions'] = copy.deepcopy(__to_dict__['full'])


class UserVisibleContent(Content):
    "Abstract class"
    __tablename__ = "content_user_visible"
    id            = Column(Integer(), ForeignKey('content.id'), primary_key=True)
    views         = Column(Integer(), nullable=False, default=0)
    boom_count    = Column(Integer(), nullable=False, default=0, doc="Controlled by postgres trigger")

    # Setup __to_dict__fields
    __to_dict__ = copy.deepcopy(Content.__to_dict__)
    _extra_user_visible_fields = {
            'views'        : None ,
            'boom_count'   : None ,
    }
    __to_dict__['default'     ].update(_extra_user_visible_fields)
    __to_dict__['full'        ].update(_extra_user_visible_fields)
    __to_dict__['full+actions'].update(_extra_user_visible_fields)
    #__to_dict__['list_with_media'].update(_extra_user_visible_fields)
    #__to_dict__['list_no_creator'].update(_extra_user_visible_fields)

    def action_list_for(self, member):
        action_list = Content.action_list_for(self, member)
        if self.is_parent_owner(member):
            if self.response_type == 'none':
                action_list.append('approve')
                action_list.append('seen')
                action_list.append('dissasociate')
        return action_list

    def is_parent_owner(self, member):
        # TODO
        # Currently just check editable_by, but needs aditional checks to see if member is part of organisation
        if self.parent:
            return self.parent.editable_by(member)
        return False

    def boom_to_all_followers(self, member):
        from civicboom.lib.database.actions import boom_to_all_followers
        return boom_to_all_followers(self, member)


class ArticleContent(UserVisibleContent):
    __tablename__   = "content_article"
    __mapper_args__ = {'polymorphic_identity': 'article'}
    _response_type  = Enum("none", "approved", "seen", "dissassociated", name="response_type")
    id              = Column(Integer(), ForeignKey('content_user_visible.id'), primary_key=True)
    rating          = Column(Float(), nullable=False, default=0, doc="Controlled by postgres trigger")
    ratings         = relationship("Rating", backref=backref('content'), cascade="all,delete-orphan")
    response_type   = Column(_response_type, nullable=False, default="none")

    # AllanC TODO:
    # Could have derived fields for count="20" min="1" max="10"
    # This is used by Yahoos RSS guide and could be very usefull for statistical processing in future
    # http://video.search.yahoo.com/mrss - see <media:community>

    # Setup __to_dict__fields
    __to_dict__ = copy.deepcopy(UserVisibleContent.__to_dict__)
    _extra_article_fields = {
        'rating'        : None ,
        'response_type' : None ,
    }
    __to_dict__['default'     ].update(_extra_article_fields)
    __to_dict__['full'        ].update(_extra_article_fields)
    __to_dict__['full+actions'].update(_extra_article_fields)
    #__to_dict__['list_with_media'].update(_extra_article_fields)
    #__to_dict__['list_no_creator'].update(_extra_article_fields)

    def rate(self, member, rating):
        from civicboom.lib.database.actions import rate_content
        return rate_content(self, member, rating)

    def parent_seen(self):
        from civicboom.lib.database.actions import parent_seen
        return parent_seen(self)

    def parent_approve(self):
        from civicboom.lib.database.actions import parent_approve
        return parent_approve(self)

    def parent_dissasociate(self):
        from civicboom.lib.database.actions import parent_disasociate
        return parent_disasociate(self)


class SyndicatedContent(UserVisibleContent):
    __tablename__   = "content_syndicate"
    __mapper_args__ = {'polymorphic_identity': 'syndicate'}
    id              = Column(Integer(), ForeignKey('content_user_visible.id'), primary_key=True)
    # FIXME: incomplete


class AssignmentContent(UserVisibleContent):
    __tablename__   = "content_assignment"
    __mapper_args__ = {'polymorphic_identity': 'assignment'}
    id              = Column(Integer(),        ForeignKey('content_user_visible.id'), primary_key=True)
    event_date      = Column(DateTime(),       nullable=True)
    due_date        = Column(DateTime(),       nullable=True)
    assigned_to     = relationship("MemberAssignment", backref=backref("content"), cascade="all,delete-orphan")
    #assigned_to     = relationship("Member", backref=backref("assigned_assignments"), secondary="MemberAssignment")
    closed          = Column(Boolean(),        nullable=False, default=False, doc="when assignment is created it must have associated MemberAssigmnet records set to pending")
    
    # Setup __to_dict__fields
    __to_dict__ = copy.deepcopy(UserVisibleContent.__to_dict__)
    _extra_assignment_fields = {
            'due_date'              : None ,
            'event_date'            : None ,
            'closed'                : None ,
    }
    __to_dict__['default'     ].update(_extra_assignment_fields)
    __to_dict__['full'        ].update(_extra_assignment_fields)
    __to_dict__['full+actions'].update({
            'accepted' : lambda content: [a.member.to_dict() for a in content.assigned_to if a.status=="accepted" ] ,
            'pending'  : lambda content: [a.member.to_dict() for a in content.assigned_to if a.status=="pending"  ] ,
            'withdrawn': lambda content: [a.member.to_dict() for a in content.assigned_to if a.status=="withdrawn"] ,
    })
    __to_dict__['full+actions'].update(__to_dict__['full'])
    #__to_dict__['list_with_media'].update(_extra_assignment_fields)
    #__to_dict__['list_no_creator'].update(_extra_assignment_fields)


    def action_list_for(self, member):
        action_list = UserVisibleContent.action_list_for(self, member)
        if self.acceptable_by(member):
            status = self.previously_accepted_by(member)
            if not status:
                action_list.append('accept')
            elif status != 'withdrawn':
                action_list.append('withdraw')
        return action_list
    
    def hash(self):
        h = hashlib.md5(UserVisibleContent.hash(self))
        for field in ("event_date","due_date","closed"): #TODO: includes assigned_to in list?
            h.update(str(getattr(self,field)))
        return h.hexdigest()

    def acceptable_by(self, member):
        if self.creator==member: return False
        if self.closed         : return False #TODO - finish - "closed and not in assinged_to list"
        #if member has accepted before? (will this break templates?)
        return True
        
    def previously_accepted_by(self, member):
        from civicboom.lib.database.actions import assignment_previously_accepted_by
        return assignment_previously_accepted_by(self, member)

    def accept(self, member):
        from civicboom.lib.database.actions import accept_assignment
        #if self.acceptable_by(member):
        return accept_assignment(self, member)
        #return False
    
    def withdraw(self, member):
        from civicboom.lib.database.actions import withdraw_assignemnt
        return withdraw_assignemnt(self, member)

    def invite(self, members):
        """
        For closed assignments we need to invite specific members to participate
        invite can be given a single member or a list of members (as username strings or member object list)
        """
        from civicboom.lib.database.actions import accept_assignment
        from civicboom.model.meta import Session
        def invite_member(member):
            return accept_assignment(self, member, status="pending", delay_commit=True)
        if isinstance(members, list):
            for member in members:
                invite_member(member)
        else:
            invite_member(members)
        Session.commit()
        
    @property
    def num_accepted(self):
        """
        TODO
        To be replaced with derived field with DB trigger or update_assignment call
        accepted_by is set after the db is setup in civicboom_init
        """
        return len(accepted_by)


class MemberAssignment(Base):
    __tablename__ = "member_assignment"
    _assignment_status = Enum("pending", "accepted", "withdrawn", name="assignment_status")
    content_id    = Column(Integer(),    ForeignKey('content_assignment.id'), nullable=False, primary_key=True)
    member_id     = Column(Integer(),    ForeignKey('member.id')            , nullable=False, primary_key=True)
    status        = Column(_assignment_status,  nullable=False)

    member       = relationship("Member")

class License(Base):
    __tablename__ = "license"
    id            = Column(Integer(),     primary_key=True)
    code          = Column(Unicode(32),   nullable=False, unique=True)
    name          = Column(Unicode(250),  nullable=False, unique=True)
    url           = Column(Unicode(250),  nullable=False)
    description   = Column(UnicodeText(), nullable=False)
    #articles      = relationship("Content", backref=backref('license'))

    __to_dict__ = copy.deepcopy(Base.__to_dict__)
    __to_dict__.update({
        'default': {
            'id'           : None ,
            'code'         : None ,
            'name'         : None ,
            'url'          : None ,
            'description'  : None ,
        },
    })
    __to_dict__.update({
        'full'   : copy.deepcopy(__to_dict__['default'])
    })
    __to_dict__.update({
        'actions': copy.deepcopy(__to_dict__['default'])
    })


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


class FlaggedContent(Base):
    __tablename__ = "flagged_content"
    _flag_type = Enum("offensive", "spam", "copyright", "automated", "other", name="flag_type")
    id            = Column(Integer(),     primary_key=True)
    content_id    = Column(Integer(),     ForeignKey('content.id'), nullable=False)
    member_id     = Column(Integer(),     ForeignKey('member.id') , nullable=True )
    timestamp     = Column(DateTime(),    nullable=False, default=func.now())
    type          = Column(_flag_type,    nullable=False)
    comment       = Column(UnicodeText(), nullable=True, doc="optional should the user want to add additional details")

    def __str__(self):
        return "%s - %s (%s)" % (self.member.username, self.comment, self.type)


GeometryDDL(Content.__table__)
