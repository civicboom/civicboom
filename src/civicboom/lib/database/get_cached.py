from civicboom.model.member  import Member, User, Group, GroupMembership
from civicboom.model.content import Content, Tag, License
from civicboom.model.media   import Media
from civicboom.model.message import Message
from civicboom.model.meta    import Session

from sqlalchemy.orm     import join, joinedload
from sqlalchemy         import and_, or_, not_
from sqlalchemy.orm.exc import NoResultFound

from civicboom.lib.misc import make_username

import logging
log = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# Cashe Management - Part 1
#-------------------------------------------------------------------------------
# A collection of functions used to setup + assit with caching
# Part 2 contains all the functions for invalidating the cache and must be defined after the cached functions

from civicboom.lib.database.etag_manager import etag_key_incement, add_etag_dependency_key

add_etag_dependency_key("content")
add_etag_dependency_key("member")
add_etag_dependency_key("member_content")
add_etag_dependency_key("member_assignments_active")


#-------------------------------------------------------------------------------
# Database Object Gets - Cached - Get data from database that is cached
#-------------------------------------------------------------------------------
# Most methods will have a get_stuff and get_stuff_nocache. As the cache is a decorator we can bypass the cache by calling the _nocache variant

def get_media(id=None, hash=None):
    if id:
        try:
            return Session.query(Media).filter_by(id=id).one()
        except NoResultFound:
            return None
    if hash:
        try:
            return Session.query(Media).filter_by(hash=hash).first()
        except NoResultFound:
            return None
    
    

#@cache_this
def get_licenses():
    return Session.query(License).all()


# AllanC - primarly used in setup of test data, not normally used in main site operation
def get_license(license):
    license = license or u"Unspecified" # get_license(None) should return the default
    assert type(license) == unicode

    try:
        return Session.query(License).filter_by(code=license).one()
    except NoResultFound:
        # Shish - as far as I can tell, we will never want to find by name; so
        #         leave the unused code commented out until it is wanted
        #try:
        #    return Session.query(License).filter_by(name=unicode(license)).one()
        #except NoResultFound:
            pass
    return None


def get_member_nocache(member, search_email=False):
    assert type(member) in [int, str, unicode]

    if type(member) == int or member.isdigit():
        try:
            return Session.query(Member).with_polymorphic('*').filter_by(id=int(member)).one()
        except NoResultFound:
            pass
    else:
        try:
            return Session.query(Member).with_polymorphic('*').filter_by(username=make_username(member)).one()
        except NoResultFound:
            if search_email:
                try:
                    return Session.query(User).filter_by(email=member).one()
                except NoResultFound:
                    pass
    return None


#@cache_test.cache() #Cache decorator to go here
# TODO: it might be nice to specify eager load fields here, so getting the logged in user eagerloads group_roles and groups to be show in the title bar with only one query
def get_member(member, **kwargs):
    if not member:
        return None
    if isinstance(member, Member):
        return member
    return get_member_nocache(member, **kwargs)


def get_group(group):
    if isinstance(group, Group):
        return group
    group = get_member(group)
    if isinstance(group, Group):
        return group
    return None


def get_membership(group, member):
    member = get_member(member)
    group  = get_group(group)

    if not (member and group):
        return None

    try:
        return Session.query(GroupMembership).filter(
            and_(
                GroupMembership.group_id  == group.id,
                GroupMembership.member_id == member.id
            )
        ).one()
    except NoResultFound:
        return None

# GregM: Dirty, do not cache, see redmine #414
def get_membership_tree(group, member, iter = 0):
    if iter > 5:
        return None
    member = get_member(member)
    group  = get_group(group)

    if not (member and group):
        return None

    try:
        return Session.query(GroupMembership).filter(
            and_(
                GroupMembership.group_id  == group.id,
                GroupMembership.member_id == member.id
            )
        ).one()
    except NoResultFound:
        try:
            groups = Session.query(GroupMembership).filter(
                and_(
                    GroupMembership.group_id == group.id,
                    GroupMembership.member_id != member.id,
#                    isinstance(GroupMembership.member, Group)
                )
            ).all()
            for p_group in groups:
                p_result = get_membership_tree(p_group.member.id, member.id, iter + 1)
                if p_result:
                    return p_result
            return None
        except NoResultFound:
            return None

def get_follower_type(member, follower):
    member   = get_member(member)
    follower = get_member(follower)

    if not (member and follower):
        return None

    try:
        return Session.query(Follow).filter(
            and_(
                Follow.member_id   == member.id,
                Follow.follower_id == follower.id,
            )
        ).one().type
    except NoResultFound:
        return None

def get_assigned_to(content, member):
    content = get_group(content)
    member  = get_member(member)

    if not (content and member):
        return None
    try:
        return Session.query(MemberAssignment).filter(
            and_(
                MemberAssignment.content_id  == content.id,
                MemberAssignment.member_id   == member.id
            )
        ).one()
    except NoResultFound:
        return None


def get_message(message):
    return Session.query(Message).filter(Message.id==int(message)).options(joinedload('source')).options(joinedload('target')).first()


def get_content_nocache(content_id):
    #http://www.sqlalchemy.org/docs/mappers.html#controlling-which-tables-are-queried
    # could use .with_polymorphic([DraftContent, ArticleContent, AssignmentContent]), will see if this is needed
    try:
        return Session.query(Content).with_polymorphic('*').filter_by(id=int(content_id)).one()
    except: # used to have NoResultFound but didnt want a 500 error raised, the caller code can detect NONE and just say "not found" neatly
        return None


def get_content(content):
    if not content:
        return None
    #if content is Content object or a subclass: return content
    if issubclass(content.__class__,Content):
        return content
    return get_content_nocache(content)


def get_tag(tag):
    """
    Returns a tag object for the string passed to it
    If it does not appear in the database then return a new tag object
    If it does exisit in the data then return the database object
    """
    try:
        return Session.query(Tag).filter_by(name=unicode(tag)).one()
    except NoResultFound as nrf:
        t = Tag(unicode(tag))
        Session.add(t)
        return t



#-------------------------------------------------------------------------------
# Database List Gets - Cached - Get data lists from database that is cached
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Cache Management - Part 2 - Invalidating the Cache
#-------------------------------------------------------------------------------

def update_member(member):
    etag_key_incement("member",member.id)


def update_content(content):
    if not issubclass(content.__class__, Content):
        content = get_content_nocache(content)
    
    etag_key_incement("content",content.id)
    #cache_test.invalidate(get_content, '', content.id)
    
    etag_key_incement("member_content",content.creator.id)
    #cache_test.invalidate(get_content_from, '', article.member.id)
    
    if content.parent:               # If content has parent
        #update_content(content.parent) # Refreshes parent, this is potentialy overkill for just updateing a reposnse tilte, responses will happen so in-frequently that this isnt a problem for now
        # dissasociate has code to separately update the parent, could thoese lines be ignored?
        pass


def update_member_messages(member):
    pass


def update_accepted_assignment(member):
    pass


def update_member_assignments_active(member):
    pass
