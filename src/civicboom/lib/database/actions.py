from pylons.templating  import render_mako as render #for rendering emails
from pylons.i18n.translation import _

from civicboom.model.meta import Session
from civicboom.model         import Rating
from civicboom.model.content import MemberAssignment, AssignmentContent, FlaggedContent, Boom, Content
from civicboom.model.member  import *
from civicboom.model.payment import *

from civicboom.lib.database.get_cached import get_member, get_group, get_membership, get_content, update_content, update_accepted_assignment, update_member

from civicboom.lib.communication           import messages
from civicboom.lib.communication.email_lib import send_email

from cbutils.text import strip_html_tags
from civicboom.lib.web  import action_error, url

from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy import select


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

import logging
log = logging.getLogger(__name__)


#-------------------------------------------------------------------------------
# Member Actions
#-------------------------------------------------------------------------------

def upgrade_user_to_group(member_to_upgrade_to_group, new_admins_username, new_group_username=None):
    """
    Only to be called by admins/power users
    This handled the migration of users to groups at an SQL level
    """
    to_group   = get_member(member_to_upgrade_to_group)
    admin_user = get_member(new_admins_username)
    
    # Validation
    if not to_group or to_group.__type__!='user':
        raise action_error('member_to_upgrade_to_group not a group', code=404)
    if get_member(new_group_username):
        raise action_error('new_group_username already taken', code=404)    
    if admin_user:
        raise action_error('new_admins_username already taken', code=404)
    
    # Create new admin user
    admin_user = User()
    admin_user.name              = new_admins_username
    admin_user.username          = new_admins_username
    admin_user.status            = 'active'
    admin_user.email             = to_group.email
    admin_user.email_unverifyed  = to_group.email_unverified
    Session.add(admin_user)
    Session.commit() # needs to be commited to get id
    
    sql_cmds = []
    
    if new_group_username:
        sql_cmds += [
            Member.__table__.update().where(Member.__table__.c.id==to_group.id).values(username=new_group_username),
        ]
    
    sql_cmds += [
        # UPDATE  member set username='gradvine', __type__='group' WHERE id=533;
        Member.__table__.update().where(Member.__table__.c.id==to_group.id).values(__type__='group'),
        
        # Reassign the login details from the old member to the new admin user
        UserLogin.__table__.update().where(UserLogin.__table__.c.member_id==to_group.id).values(member_id=admin_user.id),
        
        # DELETE the matching user record that pairs with the member record
        User.__table__.delete().where(User.__table__.c.id == to_group.id),
        
        # INSERT matching group record to pair group name
        Group.__table__.insert().values(id=to_group.id, join_mode='invite', member_visibility='private', default_content_visibility='public', default_role='admin', num_members=1),
        
        # INSERT admin_user as as admin of the group
        GroupMembership.__table__.insert().values(group_id=to_group.id, member_id=admin_user.id, role='admin', status='active'),
    ]
    
    for sql_cmd in sql_cmds:
        Session.execute(sql_cmd)
    Session.commit()
    
    


def is_follower(a,b):
    """
    True if 'b' is following 'a'
    True if 'b' is a follower of 'a'
    """
    a = get_member(a)
    b = get_member(b)
    #if not a:
    #    raise action_error(_('unable to find followed'), code=404)
    #if not b:
    #    raise action_error(_('unable to find follower'), code=404)
    if not a or not b:
        return False

    try:
        if Session.query(Follow).filter(Follow.member_id == a.id).filter(Follow.follower_id == b.id).filter(Follow.type != 'trusted_invite').one():
            return True
    except:
        pass
    return False


def is_follower_trusted(a,b):
    """
    True if 'b' is following 'a' and is trusted by 'a'
    True if 'b' is a trusted follower of 'a'
    """
    a = get_member(a)
    b = get_member(b)
    if not a or not b:
        return False
    
    try:
        if Session.query(Follow).filter(Follow.member_id == a.id).filter(Follow.follower_id == b.id).filter(Follow.type == 'trusted').one():
            return True
    except:
        pass
    return False


def is_follow_trusted_invitee(a,b): # Was is_follower_invited_trust
    """
    True if 'b' has been invited to follow 'a' as a trusted follower
    True if 'b' is the invitee to follow 'a' as a trusted follower
    """
    a = get_member(a)
    b = get_member(b)
    if not a or not b:
        return False
    
    try:
        if Session.query(Follow).filter(Follow.member_id == a.id).filter(Follow.follower_id == b.id).filter(Follow.type == 'trusted_invite').one():
            return True
    except:
        pass
    return False


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
    
    # GregM: Change invite to follow if is invited, otherwise follow:
    if follower.is_follow_trusted_inviter(followed):
        follow = Session.query(Follow).filter(Follow.member_id == followed.id).filter(Follow.follower_id == follower.id).filter(Follow.type == 'trusted_invite').one()
        follow.type = 'trusted'
    else:
        #follower.following.append(followed)
        follow = Follow()
        follow.member   = followed
        follow.follower = follower
        Session.add(follow)
    
    if not delay_commit:
        Session.commit()
    
    update_member(follower)
    update_member(followed)

    followed.send_notification(messages.followed_by(member=follower, you=followed))

    return True


def unfollow(follower, followed, delay_commit=False):
    followed = get_member(followed)
    follower = get_member(follower)
    
    if not followed:
        raise action_error(_('unable to find followed'), code=404)
    if not follower:
        raise action_error(_('unable to find follower'), code=404)
    #if followed not in follower.following:
    # GregM: can unfollow to remove trusted invite
    if not follower.is_following(followed) and not follower.is_follow_trusted_inviter(followed):
        raise action_error(_('not currently following'), code=400)
    
    #follower.following.remove(followed)
    follow = Session.query(Follow).filter(Follow.member_id==followed.id).filter(Follow.follower_id==follower.id).one()
    Session.delete(follow)
    
    if not delay_commit:
        Session.commit()
    
    update_member(follower)
    update_member(followed)

    followed.send_notification(messages.follow_stop(member=follower, you=followed))

    return True


def follower_trust(followed, follower, delay_commit=False):
    followed = get_member(followed)
    follower = get_member(follower)
    
    if not followed:
        raise action_error(_('unable to find followed'), code=404)
    if not follower:
        raise action_error(_('unable to find follower'), code=404)
    if not follower.is_following(followed):
        raise action_error(_('not currently following'), code=400)
    
    follow = Session.query(Follow).filter(Follow.member_id==followed.id).filter(Follow.follower_id==follower.id).one()
    if follow.type == 'normal':
        follow.type = 'trusted'
    elif follow.type == 'trusted_invite':
        raise action_error(_('follower still has pending invite'), code=400)
    elif follow.type == 'trusted':
        raise action_error(_('follower already trusted'), code=400)
       
    if not delay_commit:
        Session.commit()
    
    update_member(follower)
    update_member(followed)
    
    follower.send_notification(messages.follower_trusted(member=followed, you=follower))
    
    return True


def follower_distrust(followed, follower, delay_commit=False):
    followed = get_member(followed)
    follower = get_member(follower)
    
    if not followed:
        raise action_error(_('unable to find followed'), code=404)
    if not follower:
        raise action_error(_('unable to find follower'), code=404)
    if not follower.is_following(followed):
        raise action_error(_('not currently following'), code=400)
    
    follow = Session.query(Follow).filter(Follow.member_id==followed.id).filter(Follow.follower_id==follower.id).one()
    if not follow:
        raise action_error(_('member is not a follower'), code=404)
    if follow.type == 'trusted':
        follow.type = 'normal'
    elif follow.type == 'trusted_invite':
        raise action_error(_('follower still has pending invite'), code=400)
    elif follow.type == 'normal':
        raise action_error(_('follower was not trusted'), code=400)
    
    if not delay_commit:
        Session.commit()
    
    # update_member(follower) # GregM: Needed?
    # update_member(followed) # GregM: Needed?
    
    follower.send_notification(messages.follower_distrusted(member=followed, you=follower))
    
    return True


def follower_invite_trusted(followed, follower, delay_commit=False):
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
    if follower.is_follow_trusted_inviter(followed):
        raise action_error(_('already invited to follow as trusted'))
    
    follow = Follow()
    follow.member   = followed
    follow.follower = follower
    follow.type        = 'trusted_invite'
    Session.add(follow)
   
    if not delay_commit:
        Session.commit()
    
    update_member(follower)
    update_member(followed)
    
    follower.send_notification(messages.follow_invite_trusted(member=followed, you=follower))
    
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
            group.send_notification(messages.group_join_request(member=member, group=group))
            
    # If user has actually become a member (open or reply to invite) then notify group
    if return_value == True:
        group.send_notification(messages.group_new_member(member=member, group=group))
        
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
            membership.member.send_notification(messages.group_remove_member_to_member(admin=c.logged_in_user, group=group))
        group.send_notification(messages.group_remove_member_to_group( admin=c.logged_in_user, group=group, member=member))
    elif membership.status == "invite": # invitation declined
        group.send_notification(messages.group_invitation_declined(member=member, group=group))
    elif membership.status == "request": # request declined
        membership.member.send_notification(messages.group_request_declined(group=group))
    
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
    member.send_notification(messages.group_invite(admin=c.logged_in_user, group=group, role=membership.role, you=member))
    
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
        member.send_notification(messages.group_request_accepted(admin=c.logged_in_user, group=group, you=member))
        group.send_notification(messages.group_new_member(member=member, group=group))
    else:
        group.send_notification(messages.group_role_changed(admin=c.logged_in_user, member=member, group=group, role=role))

    if not delay_commit:
        Session.commit()
    
    update_member(group)
    update_member(member)
    
    return True


def del_group(group):
    group = get_group(group)
    from pylons import tmpl_context as c
    for member in [member_role.member for member_role in group.members_roles]:
        member.send_notification(messages.group_deleted(group=group, admin=c.logged_in_user)) # AllanC - We cant use the standard group.send_notification because the group wont exisit after this line!
    Session.delete(group)
    Session.commit()
    update_member(group)


def del_member(member):
    member = get_member(member)
    Session.delete(member)
    Session.commit()
    update_member(member)


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
    # all permissins hendled by controler action - so this is unneeded here
    #if not assignment.viewable_by(c.logged_in_persona):
    #    raise action_error(_('_assignment is not visible to your user and therefor cannot be accepted'), code=403)
    if assignment_previously_accepted_by(assignment, member):
        raise action_error(_('_assignment has been previously accepted and cannot be accepted again'), code=400)
    #if assignment.creator == member:
    #    raise action_error(_("cannot accept your own _assignment"), code=400)

    
    assignment_accepted        = MemberAssignment()
    assignment.assigned_to.append(assignment_accepted)
    assignment_accepted.member = member
    assignment_accepted.status = status
    Session.add(assignment_accepted)
    
    if not delay_commit:
        Session.commit()
    update_accepted_assignment(member)
    
    if status=="accepted":
        assignment.creator.send_notification(messages.assignment_accepted(member=member, assignment=assignment, you=assignment.creator))
    if status=="pending":
        member.send_notification(messages.assignment_invite  (member=assignment.creator, assignment=assignment, you=member)            )
    
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
        Session.commit()
        update_accepted_assignment(member)
        
        assignment.creator.send_notification(messages.assignment_interest_withdrawn(member=member, assignment=assignment, you=assignment.creator))
        
        return True
    except:
        pass
    return False


def respond_assignment(parent_content, member, delay_commit=False):
    """
    When creating a response, the accepted record should be flagged as responded
    """
    member         = get_member(member)
    parent_content = get_content(parent_content)
    
    if not member:
        raise action_error(_("cant find user"), code=404)
    if not parent_content:
        raise action_error(_("cant find parent content"), code=404)
        
    if parent_content.__type__!='assignment':
        return # Nothing to do if parent is not assignment
    
    try:
        # upgrade an 'accepted' record to 'responded'
        member_assignment = Session.query(MemberAssignment).filter_by(member_id=member.id, content_id=parent_content.id).one()
        member_assignment.status = "responded"
    except:
        # otherwise create 'responded' record
        member_assignment         = MemberAssignment()
        member_assignment.content = parent_content
        member_assignment.member  = member
        #assignment_accepted.member_id = member.id
        member_assignment.status = "responded"
        Session.add(member_assignment)

    if not delay_commit:
        Session.commit()
        
    update_accepted_assignment(member)
    return True

    

#-------------------------------------------------------------------------------
# Content Actions
#-------------------------------------------------------------------------------

def del_content(content):
    content = get_content(content)
    # TODO - AllanC - send notification to group members?
    update_content(content) #invalidate the cache
    Session.delete(content)
    Session.commit()
    

def del_member(member):
    member = get_member(member)
    update_member(member) #invalidate the cache
    Session.delete(member)
    Session.commit()


def flag_content(content, member=None, type="automated", comment=None, url_base=None, delay_commit=False, moderator_address=None):
    """
    if url_base is included an alternate URL generator to avert the use of the pylons one
    """
    flag = FlaggedContent()
    flag.member  = get_member(member)
    flag.content = get_content(content)
    flag.comment = strip_html_tags(comment)
    flag.type    = type
    Session.add(flag)
    if not delay_commit:
        Session.commit()
    else:
        Session.flush()
    
    # Send email to alert moderator
    member_username = 'profanity_filter'
    try:
        member_username = flag.member.username
    except:
        pass
    
    content_text = """
--- Report ---

Reporter: %(reporter)s
Category: %(type)s

%(comment)s


--- Reported Content ---

Title:  %(content_title)s
        %(content_url)s
Author: %(member_name)s
        %(member_url)s

%(content_body)s


--- Actions ---

If the content is ok, click here to remove the flag:
  %(action_ignore)s

If the content is not ok, click here to hide it from the site:
  %(action_delete)s
""" % {
        "reporter"     : member_username,
        "type"         : type,
        "comment"      : flag.comment,
        "member_name"  : flag.content.creator.username,
        "member_url"   : url('member', id=flag.content.creator.username, qualified=True, sub_domain="www"),
        "content_url"  : url('content', id=flag.content.id, qualified=True, sub_domain="www"),
        "content_title": flag.content.title,
        "content_body" : flag.content.content,
        "action_ignore": url("admin/moderate?kay=yay&content_id="+str(flag.content.id), qualified=True), #sub_domain="www"),
        "action_delete": url("admin/moderate?kay=nay&content_id="+str(flag.content.id), qualified=True), #sub_domain="www"),
    }
    
    send_email(
        moderator_address,
        subject      = 'flagged content [%s]' % type,
        content_text = content_text,
        content_html = "<pre>"+content_text+"</pre>",
    )


def boom_content(content, member, delay_commit=False):
    
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
    #boom.content_id = content.id
    #boom.member_id  = member.id
    boom.content = content
    boom.member  = member
    Session.add(boom)

    if not delay_commit:
        Session.commit()

    if   content.__type__ == 'article':
        member.send_notification_to_followers(messages.boom_article(   member=member, article   =content))
    elif content.__type__ == 'assignment':
        member.send_notification_to_followers(messages.boom_assignment(member=member, assignment=content))
    



def parent_seen(content, delay_commit=False):
    content.edit_lock     = "parent_owner"
    content.approval = "seen"
    
    # AllanC - TODO generate notification
    #content.creator.send_notification(???, delay_commit=True)
    
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
    #content.creator.send_notification(messages.article_approved(member=content.parent.creator, parent=content.parent, content=content), delay_commit=True)
    # AllanC - TODO - need to generate notification

    if not delay_commit:
        Session.commit()
        
    update_content(content)
    return True
    
    
def parent_disassociate(content, delay_commit=False):
    if not content.parent:
        return False
    
    # Update has to be done before the commit in this case bcause the parent is needed
    update_content(content.parent) # Could update responses in the future, but for now we just invalidate the whole content
    update_content(content)        # this currently has code to update parents reponses, is the line above needed?

    content.creator.send_notification(messages.article_disassociated_from_assignment(member=content.parent.creator, article=content, assignment=content.parent))
    
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

    # AllanC - TODO - rate notification needed
    

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

    return True


#-------------------------------------------------------------------------------
# Set Payment Account
#-------------------------------------------------------------------------------
def set_payment_account(member, value, delay_commit=False):
    member = get_member(member)
    #account = None
    if isinstance(value, PaymentAccount):
        member.payment_account = value
    elif value in account_types.enums:
        if value == 'free':
            account = None
        else:
            account = PaymentAccount()
            account.type = value
            Session.add(account)
        member.payment_account = account
    else:
        raise action_error('unknown account type: %s' % value)
    if not delay_commit:
        Session.commit()
    return True


# hack for admin panel use
def validate_user(username, password):
    m = get_member(username)
    m.status = "active"
    m.email = m.email_unverified
    m.email_unverified = None
    "insert into member_user_login(member_id, type, token) values((select id from member where username='%s'), 'password', 'cbfdac6008f9cab4083784cbd1874f76618d2a97');"


def payment_member_add(payment_account, member):
    member = get_member(member)
    if member.payment_account:
        return False
    member.payment_account = payment_account
    Session.commit()
    return True


def payment_member_remove(payment_account, member):
    member = get_member(member)
    if not member.payment_account == payment_account:
        return False
    member.payment_account = None
    Session.commit()
    return True
