from pylons.i18n.translation import _

from civicboom.model.meta import Session
from civicboom.model.content import MemberAssignment, AssignmentContent

from civicboom.lib.database.get_cached import get_user, get_content, update_content, update_accepted_assignment

"""
Database Actions

Typically these should not be imported by anything in the project.
These power the object actions defined in the model
"""


#-------------------------------------------------------------------------------
# Member Actions
#-------------------------------------------------------------------------------

def follow(followed, follower):
    pass


#-------------------------------------------------------------------------------
# Assignment Actions
#-------------------------------------------------------------------------------
# These are used as the functionality to the AssignmentContent object methods

def assignment_previously_accepted_by(assignment,member):
    try:
        previously_accepted_query = Session.query(MemberAssignment).filter_by(content_id=assignment.id, member_id=member.id)
    except:
        return False
    if previously_accepted_query.count() > 0:
        return previously_accepted_query.one().status
    return False


def accept_assignment(assignment, member, status="accepted", delay_commit=False):
    member     = get_user(member)
    assignment = get_content(assignment)

    if not member                                            : return _("cant find user")
    if not assignment                                        : return _("cant find assignment")
    if not issubclass(assignment.__class__,AssignmentContent): return _("only _assignments can be accepted")
    if assignment_previously_accepted_by(assignment, member) : return _('_assignment has been previously accepted and cannot be accepted again')
    
    assignment_accepted        = MemberAssignment()
    assignment.assigned_to.append(assignment_accepted)
    assignment_accepted.member = member
    assignment_accepted.status = status
    Session.add(assignment_accepted)
    if not delay_commit:
        Session.commit()
    update_accepted_assignment(member)
    return True

def withdraw_assignemnt(assignment, member):
    member     = get_user(member)
    assignment = get_content(assignment)
    
    if not member                                            : return _("cant find user")
    if not assignment                                        : return _("cant find assignment")
    
    try:
        assignment_accepted = Session.query(MemberAssignment).filter_by(member_id=member.id, content_id=assignment.id, status="accepted").one()
        assignment_accepted.status = "withdrawn"
        #Session.update(assignment_accepted)
        Session.commit()
        update_accepted_assignment(member)
        return True
    except:
        pass
    return False



#-------------------------------------------------------------------------------
# Content Actions
#-------------------------------------------------------------------------------

def del_content(content):
    content = get_content(content)    
    update_content(content) #invalidate the cache
    Session.delete(content)
    Session.commit()