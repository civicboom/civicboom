"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from civicboom.model import meta
from civicboom.model.content import Content, CommentContent, DraftContent, UserVisibleContent, ArticleContent, AssignmentContent, SyndicatedContent
from civicboom.model.content import FlaggedContent, Boom, Interest
from civicboom.model.content import License, Tag, ContentEditHistory, Media
from civicboom.model.content import MemberAssignment, Rating
from civicboom.model.member  import Member, User, UserLogin, Group, GroupMembership, Follow, PaymentAccount, account_types
from civicboom.model.message import Message
from civicboom.model.media   import Media
from civicboom.model.feed    import Feed

from cbutils.misc import now
from sqlalchemy     import and_
from sqlalchemy.orm import mapper, dynamic_loader, relationship, backref
import datetime


def init_model(main_engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #
    meta.Session.configure(bind=main_engine)
    meta.engine = main_engine


def init_model_extra():
    """
    The model uses the string based arguments (because the class may not have been defined yet)
    I'm unsure as to wether the problem was with the version of SQLAlchemy but with the string method it was not possible to specify multiple conditions under the primary join param even though the SQL created was correct
    In the future it may be possible to intigrate these with the main class defentions
    """
    period_in_days = 30
    
    Member.active_assignments_period = relationship(AssignmentContent,
        primaryjoin=and_(
            AssignmentContent.creator_id == Member.id,
            AssignmentContent.creation_date > (now() - datetime.timedelta(days=period_in_days))
        ),
        order_by=AssignmentContent.update_date.desc()
    )
    
    Member.interest = dynamic_loader(Content,
        primaryjoin=Member.id==Interest.member_id,
        secondary=Interest.__table__,
        secondaryjoin=Interest.content_id==Content.id,
        foreign_keys=[Interest.member_id,Interest.content_id],
        backref='interested_members',
    )
    
    AssignmentContent.accepted_by = dynamic_loader(Member,
        primaryjoin=and_(
            AssignmentContent.id==MemberAssignment.content_id,
            MemberAssignment.status=="accepted",
        ),
        secondary=MemberAssignment.__table__,
        secondaryjoin=MemberAssignment.member_id==Member.id,
        foreign_keys=[MemberAssignment.content_id,MemberAssignment.member_id],
        backref='assignments_accepted'
    )

    AssignmentContent.unaccepted_by = dynamic_loader(Member,
        primaryjoin=and_(
            AssignmentContent.id==MemberAssignment.content_id,
            MemberAssignment.status=="pending",
        ),
        secondary=MemberAssignment.__table__,
        secondaryjoin=MemberAssignment.member_id==Member.id,
        foreign_keys=[MemberAssignment.content_id,MemberAssignment.member_id],
        backref='assignments_unaccepted'
    )
    
    Member.boomed_content = relationship("Content",
        primaryjoin   = Member.id==Boom.member_id,
        secondary     = Boom.__table__,
        secondaryjoin = Boom.content_id==Content.id,
        backref       = backref('boomed_by'),
        foreign_keys  = [Boom.member_id, Boom.content_id],
        #cascade="all,delete-orphan",
    )
