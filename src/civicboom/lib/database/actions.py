from civicboom.model.meta import Session

from civicboom.lib.database.get_cached import get_content, update_content

#-------------------------------------------------------------------------------
# Database Actions - Database functions to get objects or perform simple data actions
#-------------------------------------------------------------------------------


def follow(followed, follower):
    pass

def accept_assignment(user, assignment):
    pass

def del_content(content):
    content = get_content(content)    
    update_content(content) #invalidate the cache
    Session.delete(content)
    Session.commit()