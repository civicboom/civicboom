from civicboom.model.member  import User
from civicboom.model.content import Content, Tag, License
from civicboom.model.meta    import Session


#-------------------------------------------------------------------------------
# Cashe Management - Part 1
#-------------------------------------------------------------------------------
# A collection of functions used to setup + assit with caching
# Part 2 contains all the functions for invalidating the cache and must be defined after the cached functions

from civicboom.lib.database.etag_manager import etag_key_incement, add_etag_dependency_key

add_etag_dependency_key("content")
add_etag_dependency_key("user_content")


#-------------------------------------------------------------------------------
# Database Object Gets - Cached - Get data from database that is cached
#-------------------------------------------------------------------------------
# Most methods will have a get_stuff and get_stuff_nocache. As the cache is a decorator we can bypass the cache by calling the _nocache variant

#@cache_this
def get_licenses():
    return Session.query(License).all()

def get_user_nocache(user):
    user = unicode(user) # AllanC - shish suspects that passing an integer may make the DB go mental
    try:
        return Session.query(User).filter_by(username=user).one()
    except:
        try:
            return Session.query(User).filter_by(email=user).one()
        except:
            try:
                return Session.query(User).filter_by(id=user).one()
            except:
                pass
    return None

#@cache_test.cache() #Cache decorator to go here
def get_user(user):
    if not user              : return None
    if isinstance(user, User): return user
    return get_user_nocache(user)

def get_content_nocache(content_id):
    try   : return Session.query(Content).with_polymorphic([DraftContent, ArticleContent, AssignmentContent]).filter_by(id=content_id).one()
    except: return None

def get_content(content_id):
    if not content_id: return None
    return get_content_nocache(content_id)


def get_tag(tag):
    """
    Returns a tag object for the string passed to it
    If it does not appear in the database then return a new tag object
    If it does exisit in the data then return the database object
    """
    try   : return Session.query(Tag).filter_by(name=tag).one()
    except: return Tag(tag)

#-------------------------------------------------------------------------------
# Database List Gets - Cached - Get data lists from database that is cached
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Cache Management - Part 2 - Invalidating the Cache
#-------------------------------------------------------------------------------

def update_content(content):
  if not issubclass(content.__class__,Content): content = get_content_nocache(content)
  
  etag_key_incement("content",content.id)
  #cache_test.invalidate(get_content, '', content.id)
  
  etag_key_incement("user_content",content.creator.id)
  #cache_test.invalidate(get_content_from, '', article.reporter.id)
  
  if content.parent:               # If content has parent
    #update_content(content.parent) # Refreshes parent, this is potentialy overkill for just updateing a reposnse tilte, responses will happen so in-frequently that this isnt a problem for now
    pass

def update_user_messages(user):
    pass
