from civicboom.model.member  import Member, User, Group, GroupMembership
from civicboom.model.content import Content, Tag, License, MemberAssignment
from civicboom.model.media   import Media
from civicboom.model.message import Message
from civicboom.model.meta    import Session

from sqlalchemy         import and_,  select
from sqlalchemy.orm     import joinedload
from sqlalchemy.orm.exc import NoResultFound

from sqla_hierarchy import *

from civicboom.lib.cache.caching_query import FromCache

from cbutils.misc import make_username

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



# TODO: it might be nice to specify eager load fields here, so getting the logged in user eagerloads group_roles and groups to be show in the title bar with only one query
def get_member(member, search_email=False, cache=False, **kwargs):
    if not member:
        return None
    if isinstance(member, Member):
        return member

    assert type(member) in [int, str, unicode]

    get_member_querys = []

    if type(member) == int or member.isdigit():
        get_member_querys.append( Session.query(Member).with_polymorphic('*').filter_by(id=int(member)) )
    else:
        get_member_querys.append( Session.query(Member).with_polymorphic('*').filter_by(username=make_username(member)) )
        if search_email:
            get_member_querys.append( Session.query(User).filter_by(email=member) )

    for query in get_member_querys:
        if cache:
            query = query.options(FromCache("default", "members"))
        if cache == 'invalidate':
            # Invalidate has to be called in the same order as the get_member query
            # Reference - http://www.sqlalchemy.org/trac/browser/examples/beaker_caching/helloworld.py
            # As we were aquireing the member by a varity of methods and querys, I decided to put the invalidate method as part of the get method to reduce the duplucation between the get and invaidate methods
            try   : query.invalidate()
            except: pass # May fail if invalidate is called before item is cached - we dont care in this case - surely, we have to read it before we update it? can this be removed?
        else:
            try                 : return query.one()
            except NoResultFound: pass
    
    return None


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


def get_group_member_username_list(group, members=None, exclude_list=None):
    """
    Get linear list of all members and sub members - list is guaranteeded to
     - contain only user objects
     - have no duplicates
    """
    if members == None:
        members = {}
    if exclude_list == None:
        exclude_list = []
    for member in [mr.member for mr in group.members_roles if mr.status=='active' and mr.member.status=='active' and mr.member.username not in members and mr.member.username not in exclude_list]:
        if   member.__type__ == 'user':
            members[member.username] = member
        elif member.__type__ == 'group':
            exclude_list.append(member.username)
            get_group_member_username_list(member, members, exclude_list)
    return members.keys()


def get_members(members, expand_group_members=True):
    """
    Aquire a list of all submembers e.g
    Group Test1 has 3 members
    Group Test2 has 2 members
    passing [Test1,Test2] will return 5 member objects of the submembers
    
    members can be
      group object - All user member users (including recursive sub members) of a group
      list of username strings
      a comma separated list of strings
      
    AllanC - Note ignors and does not error on members that do not exist? is this right?
    
    TODO - optimisation - lazy load settings and other large feilds from these users
    """
    
    if not members:
        return []
    
    # split comma list of string members
    if isinstance(members, basestring):
        members = [member.strip() for member in members.split(',')]
        #if len(members) == 1 and expand_group_members: # member list has one member, check if this single member is a group
        #    member = get_member(members[0])
        #    if member and member.__type__ == 'group':
        #        members = member
            # else it's a user and is valid, do nothing
    
    if isinstance(members, Group) and expand_group_members:
        members = get_group_member_username_list(members)
    
    # No need to process members list if members is a single member
    #  note: any group object will have been converted into a member list above is needed
    if isinstance(members, Member):
        return [members]
        
    # normalize member names
    members = [member if not hasattr(member, 'username') else member.username for member in members]
    
    member_objects = Session.query(Member).with_polymorphic('*').filter(Member.username.in_(members)).all()
    
    if expand_group_members:
        group_members = []
        for group in [member for member in member_objects if isinstance(member, Group)]:
            group_members += get_group_member_username_list(group) # , exclude_list=group_members
        member_objects += get_members(list(set(group_members)))
        member_objects =              list(set(member_objects))
    
    return member_objects


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
    content = get_content(content)
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


def find_content_root(content):
    content = get_content(content)
    
    if not content:
        raise action_error(_('unable to find content'), code=404)
    
    if not content.parent:
        return False
    
    qry = Hierarchy(
        Session,
        Content.__table__,
        select([Content.__table__.c.id, Content.__table__.c.parent_id]),
        starting_node=content.id,
        return_leaf=True,
    ) # FIXME: Greg
    #print qry
    ev = Session.execute(qry).first()
    
    if ev:
        return get_content(ev.id) or False
    else:
        return False


def get_tag(tag):
    """
    Returns a tag object for the string passed to it
    If it does not appear in the database then return a new tag object
    If it does exisit in the data then return the database object
    """
    tag = tag.lower()
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

def invalidate_member(member):
    get_member(member.id      , cache='invalidate')
    get_member(member.username, cache='invalidate')
    try   : get_member(member.email, cache='invalidate')
    except: pass
    
    etag_key_incement("member",member.id)


def invalidate_content(content):
    if not issubclass(content.__class__, Content):
        content = get_content_nocache(content)
    
    if not content:
        # need to invalidate
        return
    
    etag_key_incement("content",content.id)
    #cache_test.invalidate(get_content, '', content.id)
    
    etag_key_incement("member_content",content.creator.id)
    #cache_test.invalidate(get_content_from, '', article.member.id)
    
    if content.parent:               # If content has parent
        #invalidate_content(content.parent) # Refreshes parent, this is potentialy overkill for just updateing a reposnse tilte, responses will happen so in-frequently that this isnt a problem for now
        # dissasociate has code to separately update the parent, could thoese lines be ignored?
        pass


def invalidate_member_messages(member):
    pass


def invalidate_accepted_assignment(member):
    pass


def invalidate_member_assignments_active(member):
    pass
