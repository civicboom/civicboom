from civicboom.model.member  import Member, User, Group, GroupMembership
from civicboom.model.content import Content, Tag, License, MemberAssignment
from civicboom.model.media   import Media
from civicboom.model.message import Message
from civicboom.model.meta    import Session

from sqlalchemy         import and_,  select
from sqlalchemy.orm     import joinedload
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc     import InvalidRequestError

from sqla_hierarchy import *


from cbutils.misc import make_username, debug_type


import logging
log = logging.getLogger(__name__)

# This global variable is set by parent calling modles. If this is set, the module will use the cache
#  cache regions instances are added to the cache dictonary
from civicboom.lib.cache import _cache




#-------------------------------------------------------------------------------
# Database Object Gets
#-------------------------------------------------------------------------------

def get_media(id=None, hash=None):
    if id:
        return Session.query(Media).get(id)
    if hash:
        try:
            return Session.query(Media).filter_by(hash=hash).first()
        except NoResultFound:
            return None
    
    

#@cache_this
def get_licenses():
    return Session.query(License).all()


# AllanC - primarly used in setup of test data, not normally used in main site operation
def get_license(code):
    code = code or u"Unspecified" # get_license(None) should return the default
    assert type(code) in [str, unicode], debug_type(code)
    return Session.query(License).get(code)



# TODO: it might be nice to specify eager load fields here, so getting the logged in user eagerloads group_roles and groups to be show in the title bar with only one query
def get_member(member, search_email=False, **kwargs):
    if not member:
        return None
    if isinstance(member, Member):
        return member

    assert type(member) in [str, unicode], debug_type(member)

    member = make_username(member)

    # AllanC - TODO!! URGENT!! What happens to search_email in tests!!!? Lets have a separte call get_member_email or this is going to get nasty to cache

    def get_member_nocache(member_id):
        get_member_querys = []
        
        #return Session.query(Member).with_polymorphic('*').get(make_username(member)) # AllanC - .get() returns object based on primary key - else None
        get_member_querys.append( Session.query(Member).with_polymorphic('*').filter_by(id=member_id) )
        if search_email:
            get_member_querys.append( Session.query(User).filter_by(email=member_id) )
        
        for query in get_member_querys:
            try :
                result = query.one()
                #Session.expunge(result)
                return result
            except NoResultFound:
                pass
        
        return None
    
    cache      = _cache.get('member')
    cache_func = lambda: get_member_nocache(member)
    if cache:
        result = cache.get(key='member:%s' % member, createfunc=cache_func)
        #try:
            #Session.add(result)
            #return result
        #except InvalidRequestError:
        return Session.merge(result, load=False)
    return cache_func()


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
    members = [member if not hasattr(member, 'id') else member.id for member in members]
    
    member_objects = Session.query(Member).with_polymorphic('*').filter(Member.id.in_(members)).all()
    
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


def get_message(message_id):
    assert str(message_id).isdigit(), debug_type(message_id)
    return Session.query(Message).options(joinedload('source')).options(joinedload('target')).get(int(message_id))




def get_content(content):
    if not content:
        return None
    if isinstance(content,Content):
        return content
    
    try:
        content = int(content)
    except:
        return None
    
    def get_content_nocache(content_id):
        #http://www.sqlalchemy.org/docs/mappers.html#controlling-which-tables-are-queried
        # could use .with_polymorphic([DraftContent, ArticleContent, AssignmentContent]), will see if this is needed
        
        #assert str(content_id).isdigit(), debug_type(content_id)

        try:
            result = Session.query(Content).with_polymorphic('*').get(content_id) #Session.query(Content).with_polymorphic('*').filter_by(id=int(content_id)).one()
            #Session.expunge(result)
            return result
        except NoResultFound:
            return None  # used to have NoResultFound but didnt want a 500 error raised, the caller code can detect NONE and just say "not found" neatly

    cache      = _cache.get('content')
    cache_func = lambda: get_content_nocache(content)
    if cache:
        result = cache.get(key='content:%s' % content, createfunc=cache_func)
        #try:
            #Session.add(result)
            #return result
        #except InvalidRequestError:
            #log.warn('Content object already in session, but how do we get a reference to the exisitng object in the session?')
        return Session.merge(result, load=False)

    return cache_func()


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

