"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from civicboom.model import meta
from civicboom.model.content import Content, CommentContent, DraftContent, UserVisibleContent, ArticleContent, AssignmentContent, SyndicatedContent, FlaggedContent, Boom
from civicboom.model.content import License, Tag, ContentEditHistory, Media
from civicboom.model.content import MemberAssignment, Rating
from civicboom.model.member  import Member, User, UserLogin, Group, GroupMembership, Follow, PaymentAccount, account_types
from civicboom.model.message import Message
from civicboom.model.media   import Media
from civicboom.model.feed    import Feed


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
