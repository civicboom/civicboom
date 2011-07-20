
from civicboom.model.meta import Base, location_to_string, JSONType
from civicboom.model.member import Member, has_role_required
from civicboom.model.media import Media

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText, String
from sqlalchemy import Enum, Integer, DateTime, Boolean, Float
from geoalchemy import GeometryColumn, Point, GeometryDDL
from sqlalchemy import and_, or_, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import DDL, CheckConstraint, UniqueConstraint

import hashlib
import copy
from webhelpers.text import truncate

#-------------------------------------------------------------------------------
# Enumerated Types
#-------------------------------------------------------------------------------
_content_type = Enum("comment", "draft", "article", "assignment", "syndicate", name="content_type")

publishable_types = ["article", "assignment"]


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
    content_id    = Column(Integer(),    ForeignKey('content.id'), nullable=False, primary_key=True)
    member_id     = Column(Integer(),    ForeignKey('member.id') , nullable=False, primary_key=True)
    timestamp     = Column(DateTime(),   nullable=False, default=func.now())
    member        = relationship("Member" , primaryjoin='Member.id==Boom.member_id')
    content       = relationship("Content", primaryjoin='Content.id==Boom.content_id')
    # AllanC - could we enforce that content is user visible at the DB level here?
    # Shish - it can be done, but is a little ugly (join the boom to the contents table,
    #         check that __type__ is in the whitelist, make sure the whitelist is up to date)


class Rating(Base):
    __tablename__ = "map_ratings"
    content_id    = Column(Integer(),    ForeignKey('content_user_visible.id'), nullable=False, primary_key=True)
    member_id     = Column(Integer(),    ForeignKey('member.id')              , nullable=False, primary_key=True)
    rating        = Column(Integer(),    nullable=False)

    __table_args__ = (
        CheckConstraint("rating > 0 AND rating <= 5"),
        {}
    )


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
    __type__        = Column(_content_type, nullable=False, index=True)
    __mapper_args__ = {'polymorphic_on': __type__}
    #_visiability = Enum("pending", "show", name="content_")
    _edit_lock   = Enum("parent_owner", "group", "system", name="edit_lock_level")
    id              = Column(Integer(),        primary_key=True)
    title           = Column(Unicode(250),     nullable=False, default=u"Untitled")
    content         = Column(UnicodeText(),    nullable=False, default=u"", doc="The body of text")
    creator_id      = Column(Integer(),        ForeignKey('member.id'),  nullable=False, index=True)
    parent_id       = Column(Integer(),        ForeignKey('content.id'), nullable=True,  index=True)
    location        = GeometryColumn(Point(2), nullable=True   ) # FIXME: area rather than point? AllanC - Point for now, need to consider referenceing polygon areas in future? (more research nedeed)
    creation_date   = Column(DateTime(),       nullable=False, default=func.now())
    update_date     = Column(DateTime(),       nullable=False, default=func.now(), doc="Controlled by postgres trigger")
    private         = Column(Boolean(),        nullable=False, default=False, doc="see class doc")
    license_id      = Column(Unicode(32),      ForeignKey('license.id'), nullable=False, default=u"CC-BY")
    visible         = Column(Boolean(),        nullable=False, default=True)
    edit_lock       = Column(_edit_lock,       nullable=True , default=None)
    extra_fields    = Column(JSONType(mutable=True), nullable=False, default={})

    num_responses   = Column(Integer(),        nullable=False, default=0) # Derived field - see postgress trigger
    num_comments    = Column(Integer(),        nullable=False, default=0) # Derived field - see postgress trigger
    
    # FIXME: remote_side is confusing?
    # AllanC - it would be great to just have 'parent', we get a list of responses from API (contnte_lists.repnses)
    #          however :( without the 'responses' relationship deleting content goes nuts about orphas
    # Shish  - do we want to cascade to delete replies?
    # AllanC - we want to cascade deleting of comments, but not full responses. Does the 'comments' cascade below over this?
    responses       = relationship("Content",  primaryjoin=id==parent_id, backref=backref('parent', remote_side=id, order_by=creation_date))
    #parent          = relationship("Content", primaryjoin=parent_id==id, remote_side=id)
    creator         = relationship("Member" , primaryjoin="Content.creator_id==Member.id", backref=backref('content', cascade="all,delete-orphan"))
    
    attachments     = relationship("Media",              backref=backref('attached_to')         , cascade="all,delete-orphan")
    edits           = relationship("ContentEditHistory", backref=backref('content', order_by=id), cascade="all,delete-orphan")
    tags            = relationship("Tag",                secondary=ContentTagMapping.__table__ )
    license         = relationship("License")
    
    comments        = relationship("CommentContent", order_by=creation_date.asc(), cascade="all", primaryjoin="(CommentContent.id==Content.parent_id) & (Content.visible==True)")
    flags           = relationship("FlaggedContent", backref=backref('content'), cascade="all,delete-orphan")

    __table_args__ = (
        CheckConstraint("length(title) > 0"),
        CheckConstraint("substr(extra_fields,1,1)='{' AND substr(extra_fields,length(extra_fields),1)='}'"),
        {}
    )
    

    # used by obj_to_dict to create a string dictonary representation of this object
    __to_dict__ = copy.deepcopy(Base.__to_dict__)
    __to_dict__.update({
        'default': {
            'id'           : None ,
            'type'         : lambda content: content.__type__ ,
            #'status'       : None ,
            'parent_id'    : None ,
            'title'        : None ,
            'content_short': None , # this is a property # lambda content: "implement content_short postgress trigger" ,
            'creator_id'   : None ,
            'thumbnail_url': None ,
            'creation_date': None ,
            'update_date'  : None ,
            'location'     : lambda content: location_to_string(content.location),
            'num_responses': None ,
            'num_comments' : None ,
            'license_id'   : None ,
            'private'      : None ,
            'edit_lock'    : None ,
            'url'          : lambda content: content.__link__(),
        },
    })
    
    # Single Content Item
    __to_dict__.update({
        'full': copy.deepcopy(__to_dict__['default'])
    })
    __to_dict__['full'].update({
            'content'     : None ,
            'parent'      : lambda content: content.parent.to_dict(include_fields='creator') if content.parent else None ,
            'creator'     : lambda content: content.creator.to_dict() if content.creator else None ,
            'attachments' : lambda content: [   media.to_dict(                        ) for media    in content.attachments] ,
            #'responses'   : lambda content: [response.to_dict(include_fields='creator') for response in content.responses  ] ,
            #'comments'    : lambda content: [ comment.to_dict(                        ) for comment  in content.comments   ] ,
            'license'     : lambda content: content.license.to_dict() ,
            'tags'        : lambda content: [tag.name for tag in content.tags] ,
            'root_parent' : lambda content: content.root_parent.to_dict(include_fields='creator') if content.root_parent else None,
            #'url'         : None ,
    })
    del __to_dict__['full']['parent_id']
    del __to_dict__['full']['creator_id']
    del __to_dict__['full']['license_id']
    del __to_dict__['full']['content_short']
    
    
    
    def __unicode__(self):
        return self.title # + u" (" + self.__type__ + u")"

    def __link__(self):
        from civicboom.lib.web import url
        return url('content', id=self.id, sub_domain='www', qualified=True)

    def clone(self, content):
        if content and content.id:
            for field in ["title", "content", "creator", "parent_id", "location", "creation_date", "private", "license_id"]:
                setattr(self, field, getattr(content, field))

    def hash(self):
        h = hashlib.md5()
        # Problem? TODO?
        # What about pythons own hash(obj) method?
        # AllanC - creator, parent, attachments and license are realtions and WILL trigger an additional query in most cases.
        #          we cant rely on just looking at creator_id etc as this may not be set until a commit
        #          solutions on a postcard?
        # is there a way in SQLAlchemy to force and object to resolve ID's without a commit?
        # need to add hash to sub objects? like Media etc
        for field in ("id", "title", "content", "creator", "parent", "update_date", "status", "private", "license", "attachments"): # AllanC: unfinished field list? include relations?
            h.update(str(getattr(self, field)))
        return h.hexdigest()

    def action_list_for(self, member, **kwargs):
        action_list = []
        if self.editable_by(member):
            action_list.append('edit')
        if self.viewable_by(member):
            action_list.append('view')
        if self.private == False and self.creator != member:
            action_list.append('flag')
        if self.private == False:
            action_list.append('aggregate')
        return action_list

    def editable_by(self, member):
        """
        Check to see if a member object has the rights to edit this content
        
        NOTE: This does not take into account the logged_in_personas role
        """
        if self.edit_lock:
            return False
        if self.creator == member:
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
        if self.visible == True:
            # GregM: If current content has a root parent then check viewable_by on root parent
            root = self.root_parent
            if root:
                return root.viewable_by(member)
            # GregM: If content is private check member is a trusted follower of content's creator
            #       We NEED to check has accepted, invited etc. for requests
            if self.private == True:
                if self.creator.is_follower_trusted(member):
                    return True
                elif self.__type__ == "assignment":
                    from civicboom.lib.database.get_cached import get_assigned_to
                    member_assignment = get_assigned_to(self, member)
                    if member_assignment:
                        if not member_assignment.member_viewed:
                            from civicboom.model.meta import Session
                            member_assignment.member_viewed = True
                            Session.commit()
                        return True
                return False
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
        from civicboom.lib.aggregation import aggregate_via_user
        if self.__type__ == 'article' or self.__type__ == 'assignment':
            return aggregate_via_user(self, self.creator)
    
    @property
    def root_parent(self):
        """
        Find this piece of content's root parent (or False if this is the root!)
        """
        from civicboom.lib.database.get_cached import find_content_root
        return find_content_root(self)
    
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

        thumbnail_type = self.__type__
        if thumbnail_type == 'article' and self.approval != None:
            thumbnail_type = 'response'

        from civicboom.lib.helpers import wh_url
        return wh_url("public", "images/default/thumbnail_%s.png" % thumbnail_type)

    @property
    def url(self):
        from pylons import url, app_globals
        return url('content', id=self.id, qualified=True)

    @property
    def content_short(self):
        """
        AllanC TODO: Derived field - Postgress trigger needed
        """
        from cbutils.text import strip_html_tags
        return truncate(strip_html_tags(self.content).strip(), length=500, indicator='...', whole_word=True)


DDL('DROP TRIGGER update_response_count ON content').execute_at('before-drop', Content.__table__)
DDL("""
CREATE OR REPLACE FUNCTION update_response_count() RETURNS TRIGGER AS $$
    DECLARE
        tmp_parent_id integer;
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            tmp_parent_id := NEW.parent_id;
        ELSIF (TG_OP = 'UPDATE') THEN
            -- use old because sometimes content will be updated to set parent to
            -- null (disassociating), but there is no use case where the parent is
            -- changed from null to a new value (yet...)
            tmp_parent_id := OLD.parent_id;
        ELSIF (TG_OP = 'DELETE') THEN
            tmp_parent_id := OLD.parent_id;
        END IF;

        IF tmp_parent_id IS NOT NULL THEN
            UPDATE content SET num_responses = (
                SELECT count(*)
                FROM content
                WHERE __type__='article' AND parent_id=tmp_parent_id
            ) WHERE id=tmp_parent_id;

            UPDATE content SET num_comments = (
                SELECT count(*)
                FROM content
                WHERE __type__='comment' AND parent_id=tmp_parent_id
            ) WHERE id=tmp_parent_id;
        END IF;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_response_count
    AFTER INSERT OR UPDATE OR DELETE ON content
    FOR EACH ROW EXECUTE PROCEDURE update_response_count();
""").execute_at('after-create', Content.__table__)
GeometryDDL(Content.__table__)

DDL("CREATE INDEX content_fts_idx ON content USING gin(to_tsvector('english', title || ' ' || content));").execute_at('after-create', Content.__table__)


class DraftContent(Content):
    __tablename__   = "content_draft"
    __mapper_args__ = {'polymorphic_identity': 'draft'}
    id              = Column(Integer(), ForeignKey('content.id'), primary_key=True)
    target_type     = Column(_content_type, nullable=True, default='article')
    #publish_id      = Column(Integer(), nullable=True, doc="if present will overwite the published content with this draft")
    auto_publish_trigger_date = Column(DateTime(), nullable=True)

    __to_dict__ = copy.deepcopy(Content.__to_dict__)
    _extra_draft_fields = {
            'target_type'     : None ,
    }
    __to_dict__['default'     ].update(_extra_draft_fields)
    __to_dict__['full'        ].update(_extra_draft_fields)

    def __init__(self):
        self.private  = True # AllanC? hu? - GregM: Removed set to user/hub default in contents controller
        self.__type__ = 'draft'

    def clone(self, content):
        Content.clone(self, content)
        self.publish_id = content.id
        
    def action_list_for(self, member, **kwargs):
        action_list = Content.action_list_for(self, member, **kwargs)
        if self.creator == member and has_role_required('editor', kwargs.get('role', 'admin')):
            action_list.append('publish')
            action_list.append('delete')
        return action_list


class CommentContent(Content):
    __tablename__   = "content_comment"
    __mapper_args__ = {'polymorphic_identity': 'comment'}
    id              = Column(Integer(), ForeignKey('content.id'), primary_key=True)

    __to_dict__ = {} #Content.__to_dict__.copy()
    __to_dict__['default'] = {
        'id'           : None ,
        'creator'      : lambda content: content.creator.to_dict('default') ,
        'content'      : None ,
        'creation_date': None ,
    }
    __to_dict__['full']         = copy.deepcopy(__to_dict__['default'])

    def __init__(self):
        self.__type__ = 'comment'


class UserVisibleContent(Content):
    "Abstract class"
    __tablename__ = "content_user_visible"
    id            = Column(Integer() , ForeignKey('content.id'), primary_key=True)
    views         = Column(Integer() , nullable=False, default=0)
    publish_date  = Column(DateTime(), nullable=False, default=func.now())
    boom_count    = Column(Integer() , nullable=False, default=0, doc="Controlled by postgres trigger")

    # Setup __to_dict__fields
    __to_dict__ = copy.deepcopy(Content.__to_dict__)
    _extra_user_visible_fields = {
            'views'        : None ,
            'boom_count'   : None ,
            'publish_date' : None ,
    }
    __to_dict__['default'     ].update(_extra_user_visible_fields)
    __to_dict__['full'        ].update(_extra_user_visible_fields)


    def action_list_for(self, member, **kwargs):
        action_list = Content.action_list_for(self, member, **kwargs)
        action_list.append('respond')
        if self.creator == member and has_role_required('editor', kwargs.get('role', 'admin')):
            action_list.append('update')
            action_list.append('delete')
        if self.is_parent_owner(member) and member.has_account_required('plus'): # observing member need a paid account
            if has_role_required('editor', kwargs.get('role', 'admin')):
                if self.approval == 'none':
                    action_list.append('approve')
                    action_list.append('seen')
                    action_list.append('dissasociate')
        #AllanC: TODO - if has not boomed before - check boom list:
        if self.creator != member:
            action_list.append('boom')
        return action_list

    def is_parent_owner(self, member):
        # TODO
        # Currently just check editable_by, but needs aditional checks to see if member is part of organisation
        if self.parent:
            return self.parent.editable_by(member)
        return False

    def boom_content(self, member):
        from civicboom.lib.database.actions import boom_content
        return boom_content(self, member)


class ArticleContent(UserVisibleContent):
    __tablename__   = "content_article"
    __mapper_args__ = {'polymorphic_identity': 'article'}
    _approval  = Enum("none", "approved", "seen", "dissassociated", name="approval")
    id         = Column(Integer(), ForeignKey('content_user_visible.id'), primary_key=True)
    rating     = Column(Float(), nullable=False, default=0, doc="Controlled by postgres trigger")
    ratings    = relationship("Rating", backref=backref('content'), cascade="all,delete-orphan")
    approval   = Column(_approval, nullable=False, default="none")

    __table_args__ = (
        CheckConstraint("rating >= 0 AND rating <= 1"),
        {}
    )

    # AllanC TODO:
    # Could have derived fields for count="20" min="1" max="10"
    # This is used by Yahoos RSS guide and could be very usefull for statistical processing in future
    # http://video.search.yahoo.com/mrss - see <media:community>

    # Setup __to_dict__fields
    __to_dict__ = copy.deepcopy(UserVisibleContent.__to_dict__)
    _extra_article_fields = {
        'rating'   : None ,
        'approval' : None ,
    }
    __to_dict__['default'     ].update(_extra_article_fields)
    __to_dict__['full'        ].update(_extra_article_fields)

    def __init__(self):
        self.__type__ = 'article'

    def rate(self, member, rating):
        from civicboom.lib.database.actions import rate_content
        return rate_content(self, member, rating)

    def parent_seen(self):
        from civicboom.lib.database.actions import parent_seen
        return parent_seen(self)

    def parent_approve(self):
        from civicboom.lib.database.actions import parent_approve
        return parent_approve(self)

    def parent_disassociate(self):
        from civicboom.lib.database.actions import parent_disassociate
        return parent_disassociate(self)


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
    closed          = Column(Boolean(),        nullable=False, default=False, doc="when assignment is created it must have associated MemberAssigmnet records set to pending")
    default_response_license_id = Column(Unicode(32), ForeignKey('license.id'), nullable=False, default=u"CC-BY")
    num_accepted    = Column(Integer(),        nullable=False, default=0) # Derived field - see postgress trigger

    default_response_license    = relationship("License")

    assigned_to     = relationship("MemberAssignment", backref=backref("content"), cascade="all,delete-orphan")
    #assigned_to     = relationship("Member", backref=backref("assigned_assignments"), secondary="MemberAssignment")

    ## there is a case where "due date < event date" makes sense, sort
    ## of -- when submitting eg photos to be displayed at an event
    #__table_args__ = (
    #    CheckConstraint("(event_date IS NULL) OR (due_date IS NULL) OR (due_date >= event_date)"),
    #    {}
    #)
    
    # Setup __to_dict__fields
    __to_dict__ = copy.deepcopy(UserVisibleContent.__to_dict__)
    _extra_assignment_fields = {
            'due_date'                : None ,
            'event_date'              : None ,
            'closed'                  : None ,
            'num_accepted'            : None ,
            'default_response_license': lambda content: content.license.to_dict() ,
    }
    __to_dict__['default'     ].update(_extra_assignment_fields)
    __to_dict__['full'        ].update(_extra_assignment_fields)
    #__to_dict__['full+actions'].update({
    #        'accepted' : lambda content: [a.member.to_dict() for a in content.assigned_to if a.status=="accepted" ] ,
    #        'pending'  : lambda content: [a.member.to_dict() for a in content.assigned_to if a.status=="pending"  ] ,
    #        'withdrawn': lambda content: [a.member.to_dict() for a in content.assigned_to if a.status=="withdrawn"] ,
    #})
    #__to_dict__['full+actions'].update(__to_dict__['full'])

    def __init__(self):
        self.__type__ = 'assignment'

    def action_list_for(self, member, **kwargs):
        action_list = UserVisibleContent.action_list_for(self, member, **kwargs)
        if self.creator == member:
            action_list.append('invite_to_assignment')
        if self.acceptable_by(member):
            status = self.previously_accepted_by(member)
            if not status:
                action_list.append('accept')
            elif status != 'withdrawn':
                action_list.append('withdraw')
        return action_list
    
    def hash(self):
        h = hashlib.md5(UserVisibleContent.hash(self))
        for field in ("event_date", "due_date", "closed"): #TODO: includes assigned_to in list?
            h.update(str(getattr(self, field)))
        return h.hexdigest()

    def acceptable_by(self, member):
        if self.creator == member:
            return False
        if self.closed:
            return False #TODO - finish - "closed and not in assinged_to list"
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

    # GregM: Added kwargs to allow for invite controller adding role (needed for group invite, trying to genericise things as much as possible)
    def invite(self, members, **kwargs):
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


class MemberAssignment(Base):
    __tablename__ = "member_assignment"
    _assignment_status = Enum("pending", "accepted", "withdrawn", "responded", name="assignment_status")
    content_id    = Column(Integer(),    ForeignKey('content_assignment.id'), nullable=False, primary_key=True)
    member_id     = Column(Integer(),    ForeignKey('member.id')            , nullable=False, primary_key=True)
    status        = Column(_assignment_status,  nullable=False)
    member_viewed = Column(Boolean(),    nullable=False, default=False, doc="a flag to keep track to see if the member invited has actually viewed this page")
    #update_date   = Column(DateTime(),   nullable=False, default=func.now(), doc="Controlled by postgres trigger")
    # AllanC - TODO - implement member assignment update date postgress trigger

    #member       = relationship("Member")
    #content      = relationship("AssignmentContent")


DDL('DROP TRIGGER IF EXISTS update_num_accepted ON member_assignment').execute_at('before-drop', MemberAssignment.__table__)
DDL("""
CREATE OR REPLACE FUNCTION update_num_accepted() RETURNS TRIGGER AS $$
    DECLARE
        tmp_content_id integer;
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            tmp_content_id := NEW.content_id;
        ELSIF (TG_OP = 'UPDATE') THEN
            tmp_content_id := NEW.content_id;
        ELSIF (TG_OP = 'DELETE') THEN
            tmp_content_id := OLD.content_id;
        END IF;

        UPDATE content_assignment SET num_accepted = (
            SELECT count(*)
            FROM member_assignment
            WHERE member_assignment.status = 'accepted' AND member_assignment.content_id=tmp_content_id
        ) WHERE id=tmp_content_id;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_num_accepted
    AFTER INSERT OR UPDATE OR DELETE ON member_assignment
    FOR EACH ROW EXECUTE PROCEDURE update_num_accepted();
""").execute_at('after-create', MemberAssignment.__table__)


class License(Base):
    __tablename__ = "license"
    id            = Column(Unicode(32),   nullable=False, primary_key=True)
    name          = Column(Unicode(250),  nullable=False, unique=True)
    url           = Column(Unicode(250),  nullable=False)
    description   = Column(UnicodeText(), nullable=False)
    #articles      = relationship("Content", backref=backref('license'))

    __table_args__ = (
        CheckConstraint("length(id) > 0"),
        {}
    )

    __to_dict__ = copy.deepcopy(Base.__to_dict__)
    __to_dict__.update({
        'default': {
            'id'           : None ,
            'name'         : None ,
            'url'          : None ,
            'description'  : None ,
        },
    })
    __to_dict__.update({
        'full'   : copy.deepcopy(__to_dict__['default'])
    })


    def __init__(self, id=None, name=None, description=None, url=None):
        self.id = id
        self.name = name
        self.description = description
        self.url = url

    def __unicode__(self):
        return self.id


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
    name          = Column(Unicode(250), nullable=False, index=True)
    #type          = Column(Unicode(250), nullable=False, default=u"Topic")
    #children      = relationship("Tag", backref=backref('parent', remote_side=id))
    parent_id     = Column(Integer(),    ForeignKey('tag.id'), nullable=True, index=True)
    parent        = relationship('Tag',      backref=backref('children'), remote_side='tag.c.id')

    __table_args__ = (
        CheckConstraint("length(name) > 0"),
        UniqueConstraint('parent_id', 'name'),
        {}
    )

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
    content_id    = Column(Integer(),     ForeignKey('content.id'), nullable=False, index=True)
    member_id     = Column(Integer(),     ForeignKey('member.id'),  nullable=False, index=True)
    timestamp     = Column(DateTime(),    nullable=False, default=func.now())
    source        = Column(Unicode(250),  nullable=False, default="other", doc="civicboom, mobile, another_webpage, other service")
    text_change   = Column(UnicodeText(), nullable=False)


class FlaggedContent(Base):
    __tablename__ = "flagged_content"
    _flag_type = Enum("offensive", "spam", "copyright", "automated", "other", name="flag_type")
    id            = Column(Integer(),     primary_key=True)
    content_id    = Column(Integer(),     ForeignKey('content.id'), nullable=False, index=True)
    member_id     = Column(Integer(),     ForeignKey('member.id') , nullable=True )
    timestamp     = Column(DateTime(),    nullable=False, default=func.now())
    type          = Column(_flag_type,    nullable=False)
    comment       = Column(UnicodeText(), nullable=False, default="", doc="optional should the user want to add additional details")

    def __str__(self):
        return "%s - %s (%s)" % (self.member.username if self.member else "System", self.comment, self.type)
