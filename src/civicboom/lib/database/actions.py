from pylons import config, url
from pylons.templating  import render_mako as render #for rendering emails
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
    followed = get_member(followed)
    follower = get_member(follower)
    
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
    followed = get_member(followed)
    follower = get_member(follower)
    
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
    member     = get_member(member)
    assignment = get_content(assignment)

    if not member                                            : return _("cant find user")
    if not assignment                                        : return _("cant find assignment")
    if not issubclass(assignment.__class__,AssignmentContent): return _("only _assignments can be accepted")
    if assignment_previously_accepted_by(assignment, member) : return _('_assignment has been previously accepted and cannot be accepted again')
    
    assignment_accepted        = MemberAssignment()
    assignment.assigned_to.append(assignment_accepted)
    assignment_accepted.member_id = member.id
    assignment_accepted.status = status
    Session.add(assignment_accepted)
    
    if status=="accepted":
        assignment.creator.send_message(messages.assignment_accepted(member=member, assignment=assignment), delay_commit=True)
    if status=="pending":
        member.send_message(messages.assignment_invite  (member=assignment.creator, assignment=assignment), delay_commit=True)
    
    if not delay_commit:
        Session.commit()
        
    update_accepted_assignment(member)
    return True

def withdraw_assignemnt(assignment, member, delay_commit=False):
    member     = get_member(member)
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
    flag.member  = get_member(member)
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

def boom_to_all_followers(content, member):
    if   content.__type__ == 'article':
        member.send_message_to_followers(messages.boom_article(   member=member, article   =content), delay_commit=True)
    elif content.__type__ == 'assignment':
        member.send_message_to_followers(messages.boom_assignment(member=member, assignment=content), delay_commit=True)
    Session.commit()


def lock_content(content):
    if content.status == "locked": return False
    
    # Lock content
    content.status = "locked"

    from pylons import tmpl_context as c # Needed for passing varibles to templates
    c.content = content

    # Email content parent
    content.parent.creator.send_email(subject=_('content request'), content_html=render('/email/corporate/lock_article_to_organisation.mako'))

    # Email content creator
    content.creator.send_email(subject=_('content approved'), content_html=render('/email/corporate/lock_article_to_member.mako'))
    content.creator.send_message(messages.article_approved(member=content.parent.creator, parent=content.parent, content=content), delay_commit=True)

    Session.commit()
    update_content(content)
    return True
    
    
def disasociate_content_from_parent(content):
    if not content.parent: return False
    # Update has to be done before the commit in this case bcause the parent is needed
    update_content(content.parent) # Could update responses in the future, but for now we just invalidate the whole content
    update_content(content)        # this currently has code to update parents reponses, is the line above needed?
    
    content.creator.send_message(messages.article_disasociated_from_assignment(member=content.parent.creator, article=content, assignment=content.parent), delay_commit=True)
    content.parent = None
    Session.commit()
    return True
