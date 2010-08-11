from civicboom.model.meta   import Session

from civicboom.lib.database.get_cached import get_content

#-------------------------------------------------------------------------------
# Database Actions - Database functions to get objects or perform simple data actions
#-------------------------------------------------------------------------------


def follow(followed, follower):
    pass

def accept_assignment(user, assignment):
    pass

def del_content(content):
    content = get_content(content)
    print "unimplmented del %s" % content.id
    # send messages
    #del content
    #update_content(?)