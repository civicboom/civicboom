"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from civicboom.model import meta
from civicboom.model.content import Content, CommentContent, DraftContent, UserVisibleContent, ArticleContent, AssignmentContent
from civicboom.model.content import License, Tag, ContentEditHistory, Media
from civicboom.model.content import MemberAssignmentMapping
from civicboom.model.member import Member, User, Group, GroupMembership
from civicboom.model.message import Message

def init_model(main_engine, log_engine, legacy_engine=None):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #
    meta.Session.configure(bind=main_engine)
    meta.LogSession.configure(bind=log_engine)
    if legacy_engine:
        meta.LegacySession.configure(bind=legacy_engine)
    meta.engine = main_engine


