from pylons import config, url
from pylons.templating  import render_mako as render #for rendering emails
from pylons.i18n.translation import _

from civicboom.model.meta import Session
from civicboom.model         import Rating
from civicboom.model.content import MemberAssignment, AssignmentContent, FlaggedContent, Boom
from civicboom.model.member  import GroupMembership, group_member_roles, PaymentAccount, account_types, Follow


from civicboom.lib.database.get_cached import get_member, get_group, get_membership, get_content, update_content, update_accepted_assignment, update_member

from civicboom.lib.communication           import messages
from civicboom.lib.communication.email_lib import send_email

from civicboom.lib.text import strip_html_tags
from civicboom.lib.web  import action_error

from sqlalchemy.orm.exc import NoResultFound


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
    
    if not followed:
        raise action_error(_('unable to find followed'), code=404)
    if not follower:
        raise action_error(_('unable to find follower'), code=404)
    if follower == followed:
        raise action_error(_('may not follow yourself'), code=400)
    #if followed in follower.following:
    if follower.is_following(followed):
        raise action_error(_('already following'), code=400)
    
    # AllanC - I wanted to use is_following and remove the following reference - but as this code is run by base test populator before the site is running it cant be
    
    #follower.following.append(followed)
    follow = Follow()
    follow.member_id   = followed.id
    follow.follower_id = follower.id
    Session.add(follow)
    
    followed.send_message(messages.followed_by(member=follower), delay_commit=True)
    
    if not delay_commit:
        Session.commit()
    
    update_member(follower)
    update_member(followed)

    return True

def unfollow(follower, followed, delay_commit=False):
    followed = get_member(followed)
    follower = get_member(follower)
    
    if not followed:
        raise action_error(_('unable to find followed'), code=404)
    if not follower:
        raise action_error(_('unable to find follower'), code=404)
    #if followed not in follower.following:
    if not follower.is_following(followed):
        raise action_error(_('not currently following'), code=400)
    
    #follower.following.remove(followed)
    follow = Session.query(Follow).filter(Follow.member_id==followed.id).filter(Follow.follower_id==follower.id).one()
    Session.delete(follow)
        
    followed.send_message(messages.follow_stop(member=follower), delay_commit=True)
    
    if not delay_commit:
        Session.commit()
    
    update_member(follower)
    update_member(followed)

    return True

#-------------------------------------------------------------------------------
# Message Actions
#-------------------------------------------------------------------------------

def del_message(message):
    Session.delete(message)
    Session.commit()
    #update_member() # invalidate needed lists!!!



#-------------------------------------------------------------------------------
# Group Actions
#-------------------------------------------------------------------------------

def join_group(group, member, delay_commit=False):
    return_value = True
    
    group      = get_group(group)
    member     = get_member(member)
    membership = get_membership(group, member)
    
    if not group:
        raise action_error(_('unable to find group'), code=404)
    if not member:
        raise action_error(_('unable to find member to add'), code=404)
    # AllanC - join permissions moved to controller

        
    if membership and membership.status=="invite":
        membership.status = "active"
    else:
        membership = GroupMembership()
        membership.group  = group
        membership.member = member
        membership.role   = group.default_role
        group.members_roles.append(membership)
        
        # If a join request
        if group.join_mode == "invite_and_request":
            membership.status = "request"
            return_value = "request"
            group.send_message(messages.group_join_request(member=member, group=group), delay_commit=True)
            
    # If user has actually become a member (open or reply to invite) then notify group
    if return_value == True:
        group.send_message(messages.group_new_member(member=member, group=group))
        
    if not delay_commit:
        Session.commit()
    
    update_member(group)
    update_member(member)
    
    return return_value
    


def remove_member(group, member, delay_commit=False):
    group      = get_group(group)
    member     = get_member(member)
    membership = get_membership(group, member)
    
    if not group:
        raise action_error(_('unable to find group') , code=404)
    if not member:
        raise action_error(_('unable to find member'), code=404)
    if not membership:
        raise action_error(_('not a member of group'), code=400)
    # AllanC - permissions moved to controller
    #if member!=c.logged_in_persona and not group.is_admin(c.logged_in_persona):
    #    raise action_error('current user has no permissions for this group', 403)
    #AllanC - integrety moved to model
    #if membership.role=="admin" and num_admins<=1:
    #    raise action_error('cannot remove last admin', 400)
    
    # Notifications
    if membership.status == "active": # member removed
        from pylons import tmpl_context as c
        if member!=c.logged_in_user:
            membership.member.send_message(messages.group_remove_member_to_member(admin=c.logged_in_user, group=group), delay_commit=True)
        group.send_message(messages.group_remove_member_to_group( admin=c.logged_in_user, group=group, member=member), delay_commit=True)
    elif membership.status == "invite": # invitation declined
        group.send_message(messages.group_invitation_declined(member=member, group=group), delay_commit=True) 
    elif membership.status == "request": # request declined
        membership.member.send_message(messages.group_request_declined(group=group), delay_commit=True) 
    
    Session.delete(membership)
    
    if not delay_commit:
        Session.commit()
    
    update_member(group)
    update_member(member)
    
    return True


def invite(group, member, role, delay_commit=False):
    group      = get_group(group)
    member     = get_member(member)
    membership = get_membership(group, member)
    role       = role or group.default_role
    
    if not group:
        raise action_error(_('unable to find group'), code=404)
    if not member:
        raise action_error(_('unable to find member'), code=404)
    if membership:
        raise action_error(_('already a member of group'), code=400)
    if role not in group_member_roles.enums:
        raise action_error('not a valid role', code=400)
    # AllanC - permissions moved to controller
    #if not group.is_admin(c.logged_in_persona):
    #    raise action_error(_('no permissions for this group'), 403)

    membership = GroupMembership()
    membership.group  = group
    membership.member = member
    membership.role   = role
    membership.status = "invite"
    group.members_roles.append(membership)
    
    # Notification of invitation
    from pylons import tmpl_context as c
    member.send_message(messages.group_invite(admin=c.logged_in_user, group=group, role=membership.role), delay_commit=True)
    
    if not delay_commit:
        Session.commit()
    
    update_member(group)
    update_member(member)
    
    return True
    
    
def set_role(group, member, role, delay_commit=False):
    group      = get_group(group)
    member     = get_member(member)
    membership = get_membership(group, member)
    role       = role or membership.role or group.default_role
    
    if not group:
        raise action_error(_('unable to find group'), code=404)
    if not member:
        raise action_error(_('unable to find member'), code=404)
    if not membership:
        raise action_error(_('not a member of group'), code=400)
    if role not in group_member_roles.enums:
        raise action_error('not a valid role', code=400)
    # AllanC - permisions moved to controller
    #if not group.is_admin(c.logged_in_persona):
    #    raise action_error(_('no permissions for this group'), 403)
    # AllanC - integrtiy moved to model
    #if membership.role=="admin" and num_admins<=1:
    #    raise action_error('cannot remove last admin', 400)

    from pylons import tmpl_context as c
    membership.role = role
    if membership.status=="request":
        membership.status = "active"
        member.send_message(messages.group_request_accepted(admin=c.logged_in_user, group=group))
        group.send_message(messages.group_new_member(member=member, group=group))
    else:
        group.send_message(messages.group_role_changed(admin=c.logged_in_user, member=member, group=group, role=role), delay_commit=True)

    if not delay_commit:
        Session.commit()
    
    update_member(group)
    update_member(member)
    
    return True


def del_group(group):
    from pylons import tmpl_context as c
    for member in [member_role.member for member_role in group.members_roles]:
        member.send_message(messages.group_deleted(group=group, admin=c.logged_in_user), delay_commit=True)
    Session.delete(group)
    Session.commit()
    update_member(group)

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

    if not member:
        raise action_error(_("cant find user"), code=404)
    if not assignment:
        raise action_error(_("cant find assignment"), code=404)
    if not issubclass(assignment.__class__,AssignmentContent):
        raise action_error(_("only _assignments can be accepted"), code=400)
    if assignment_previously_accepted_by(assignment, member):
        raise action_error(_('_assignment has been previously accepted and cannot be accepted again'), code=400)
    
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
    
    if not member:
        raise action_error(_("cant find user"), code=404)
    if not assignment:
        raise action_error(_("cant find assignment"), code=404)
    
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

def boom_content(content, member, delay_commit=False):
    #if   content.__type__ == 'article':
    #    member.send_message_to_followers(messages.boom_article(   member=member, article   =content), delay_commit=True)
    #elif content.__type__ == 'assignment':
    #    member.send_message_to_followers(messages.boom_assignment(member=member, assignment=content), delay_commit=True)
    
    # Validation
    if content.private == True:
        raise action_error(_("cannot boom private content"), code=400)
    boom = None
    try:
        boom = Session.query(Boom).filter(Boom.member_id==member.id).filter(Boom.content_id==content.id).one()
    except:
        pass
    if boom:
        raise action_error(_("You have previously boomed this _content"), code=400)
    
    boom = Boom()
    boom.content_id = content.id
    boom.member_id  = member.id
    Session.add(boom)
    
    if not delay_commit:
        Session.commit()

def parent_seen(content, delay_commit=False):
    content.edit_lock     = "parent_owner"
    content.approval = "seen"
    
    # AllanC - TODO generate notification
    #content.creator.send_message(???, delay_commit=True)
    
    if not delay_commit:
        Session.commit()        
    update_content(content)
    return True

def parent_approve(content, delay_commit=False):

    content.edit_lock     = "parent_owner"
    content.approval = "approved"

    from pylons import tmpl_context as c # Needed for passing varibles to templates
    c.content = content

    # Email content parent
    content.parent.creator.send_email(subject=_('content request'), content_html=render('/email/corporate/lock_article_to_organisation.mako'))

    # Email content creator
    content.creator.send_email(subject=_('content approved'), content_html=render('/email/corporate/lock_article_to_member.mako'))
    content.creator.send_message(messages.article_approved(member=content.parent.creator, parent=content.parent, content=content), delay_commit=True)

    if not delay_commit:
        Session.commit()
        
    update_content(content)
    return True
    
    
def parent_disassociate(content, delay_commit=False):
    if not content.parent: return False
    
    # Update has to be done before the commit in this case bcause the parent is needed
    update_content(content.parent) # Could update responses in the future, but for now we just invalidate the whole content
    update_content(content)        # this currently has code to update parents reponses, is the line above needed?
    
    content.creator.send_message(messages.article_disassociated_from_assignment(member=content.parent.creator, article=content, assignment=content.parent), delay_commit=True)
    
    content.parent = None
    content.approval = "dissassociated"
    
    if not delay_commit:
        Session.commit()
    
    return True

def rate_content(content, member, rating):
    content = get_content(content)
    member  = get_member(member)

    if not content:
        raise action_error(_('unable to find content'), code=404)
    if not member:
        raise action_error(_('unable to find member'), code=404)
    if rating and int(rating)<0 or int(rating)>5:
        raise action_error(_("Ratings can only be in the range 0 to 5"), code=400)

    # remove any existing ratings
    # we need to commit after removal, otherwise SQLAlchemy
    # will optimise remove->add as modify-existing, and the
    # SQL trigger will break
    try:
        q = Session.query(Rating)
        q = q.filter(Rating.content_id==content.id)
        q = q.filter(Rating.member    ==member)
        existing = q.one()
        Session.delete(existing)
        Session.commit()
    except NoResultFound:
        pass

    # add a new one
    if rating:
        rating = int(rating)
        
        # rating = 0 = remove vote
        if rating > 0:
            r = Rating()
            r.content_id = content.id
            r.member     = member
            r.rating     = rating
            Session.add(r)
            Session.commit()

    user_log.debug("Rated Content #%d as %d" % (content.id, int(rating)))

def add_to_interests(member, content, delay_commit=False):
    content = get_content(content)
    member  = get_member(member)

    if not content:
        raise action_error(_('unable to find content'), code=404)
    if not member:
        raise action_error(_('unable to find member'), code=404)
    
    #AllanC - TODO: humm ... if we have a duplicate entry being added it will error ... we want to suppress that error
    
    member.interest.append(content)
    
    # Could update "recomended" feed with new criteria?
    
    if not delay_commit:
        Session.commit()

    user_log.debug("Added to interests #%d" % (content.id))
    
    return True


#-------------------------------------------------------------------------------
# Set Payment Account
#-------------------------------------------------------------------------------
def set_payment_account(member, value, delay_commit=False):
    member = get_member(member);
    account = None
    if isinstance(value, PaymentAccount):
        account = value
    elif value in account_types.enums:
        account = PaymentAccount()
        account.type = value
        Session.add(account)
    member.payment_account = account
    if not delay_commit:
        Session.commit()
    return True
