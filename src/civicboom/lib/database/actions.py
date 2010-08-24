from pylons import config, url
from pylons.i18n.translation import _

from civicboom.model.meta import Session
from civicboom.model.content import MemberAssignment, AssignmentContent, FlaggedContent

from civicboom.lib.database.get_cached import get_user, get_content, update_content, update_accepted_assignment, update_member

from civicboom.lib.communication       import messages
from civicboom.lib.communication.email import send_email

from civicboom.lib.text          import strip_html_tags


"""
Database Actions

Typically these should not be imported by anything in the project.
These power the object actions defined in the model

Most actions follow the following structure:
 - Get data from database
 - check everything ok to proceed
 - perform action
 - send relevent messages
 - commit
 - invalidate cache with update methods
 - return True
 
"""


#-------------------------------------------------------------------------------
# Member Actions
#-------------------------------------------------------------------------------

def follow(follower, followed, delay_commit=False):
    followed = get_user(followed)
    follower = get_user(follower)
    
    if not followed: return _('no followed')
    if not follower: return _('no follower')
    
    if followed in follower.following: return _('already following')
    
    follower.following.append(followed)
        
    followed.send_message(messages.followed_by(reporter=follower), delay_commit=True)
    
    if not delay_commit:
        Session.commit()
    
    update_member(follower)
    update_member(followed)

    return True

def unfollow(follower,followed, delay_commit=False):
    followed = get_user(followed)
    follower = get_user(follower)
    
    if not followed: return _('no followed')
    if not follower: return _('no follower')
    
    if followed not in follower.following: return _('not following')
    
    follower.following.remove(followed)
        
    followed.send_message(messages.follow_stop(reporter=follower), delay_commit=True)
    
    if not delay_commit:
        Session.commit()
    
    update_member(follower)
    update_member(followed)

    return True


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
    
    #if status=="accepted":
    #    assignment.creator.send_message(messages.assignment_accepted(member=member, assignment=assignment), delay_commit=True)
    #if status=="pending":
    #    assignment.creator.send_message(messages.assignment_invite  (member=member, assignment=assignment), delay_commit=True)
    
    if not delay_commit:
        Session.commit()
        
    update_accepted_assignment(member)
    return True

def withdraw_assignemnt(assignment, member, delay_commit=False):
    member     = get_user(member)
    assignment = get_content(assignment)
    
    if not member                                            : return _("cant find user")
    if not assignment                                        : return _("cant find assignment")
    
    try:
        assignment_accepted = Session.query(MemberAssignment).filter_by(member_id=member.id, content_id=assignment.id, status="accepted").one()
        assignment_accepted.status = "withdrawn"
        #Session.update(assignment_accepted)
        
        assignment.creator.send_message(messages.assignment_interest_withdrawn(member=member, assignment=assignment), delay_commit=True)
        
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
    
def flag_content(content, member=None, type="automated", comment=None):
    flag = FlaggedContent()
    flag.member  = get_user(member)
    flag.content = get_content(content)
    flag.comment = strip_html_tags(comment)
    flag.type    = type
    Session.add(flag)
    Session.commit()
    
    # Send email to alert moderator
    member_username = 'profanity_filter'
    try   : member_username = flag.member.username
    except: pass
    send_email(config['email.moderator'],
               subject=_('flagged content'),
               content_text="%s flagged %s as %s" % (member_username, url(controller='content', action='view', id=content.id), type)
               )
