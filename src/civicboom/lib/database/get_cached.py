from civicboom.model.member  import Member, User, Group, GroupMembership
from civicboom.model.content import Content, Tag, License
from civicboom.model.media   import Media
from civicboom.model.meta    import Session

from sqlalchemy     import and_, or_, not_

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

#@cache_this
def get_licenses():
    return Session.query(License).all()

def get_member_nocache(member):
    assert type(member) in [int, str, unicode]
    #if type(member) == int:
    try:
        return Session.query(Member).with_polymorphic('*').filter_by(id=int(member)).one()
    except:
        #pass
    #else:
        try:
            return Session.query(Member).with_polymorphic('*').filter_by(username=member).one()   
        except:
            #try:
            #    return Session.query(User).filter_by(email=member).one()
            pass
    return None

#@cache_test.cache() #Cache decorator to go here
def get_member(member):
    if not member:
        return None
    if isinstance(member, Member):
        return member
    return get_member_nocache(member)

def get_group(group):
    if isinstance(group, Group):
        return group
    group = get_member(group)
    if isinstance(group, Group):
        return group
    return None

def get_membership(group, member):
    member = get_member(member)
    try:
        return Session.query(GroupMembership).filter(and_(GroupMembership.group_id==group.id, GroupMembership.member_id==member.id)).one()
    except:
        return None

def get_content_nocache(content_id):
    #http://www.sqlalchemy.org/docs/mappers.html#controlling-which-tables-are-queried
    # could use .with_polymorphic([DraftContent, ArticleContent, AssignmentContent]), will see if this is needed
    try   : return Session.query(Content).with_polymorphic('*').filter_by(id=content_id).one()
    except: return None

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
    try   : return Session.query(Tag).filter_by(name=tag).one()
    except: return Tag(tag)


def get_media_nocache(media_id):
    try   : return Session.query(Media).filter_by(id=media_id).one()
    except: return None


#-------------------------------------------------------------------------------
# Database List Gets - Cached - Get data lists from database that is cached
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Cache Management - Part 2 - Invalidating the Cache
#-------------------------------------------------------------------------------

def update_member(member):
    etag_key_incement("member",member.id)

def update_content(content):
    if not issubclass(content.__class__,Content): content = get_content_nocache(content)
    
    etag_key_incement("content",content.id)
    #cache_test.invalidate(get_content, '', content.id)
    
    etag_key_incement("member_content",content.creator.id)
    #cache_test.invalidate(get_content_from, '', article.reporter.id)
    
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
