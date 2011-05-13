import logging
log = logging.getLogger(__name__)

from civicboom.lib.database.get_cached import get_members

from civicboom.model.meta              import Session
from civicboom.model.message           import Message
from civicboom.lib.database.get_cached import update_member_messages
from civicboom.lib.communication.email_lib import send_email


def _send_notification_to_user(member, name='', default_route='', rendered_message={}, **kwargs):
    """
    Internal call
    Must be passed member object
    Actually sends a message
    """
    
    # Get propergate settings - what other technologies is this message going to be sent over
    # Attempt to get routing settings from the member's config; if that fails, use the
    # message's default routing
    message_tech_options = member.config.get("route_"+name, default_route)
    
    # Iterate over each letter of tech_options - each letter is a code for the technology to send it to
    # e.g 'c'  will send to Comufy
    #     'et' will send to email and twitter
    #     'n'  is a normal notification
    #     ''   will dispose of the message because it has nowhere to go
    for route in message_tech_options:
        if route == 'c': # Send to Comufy
            pass
        if route == 'e' and 'e' in rendered_message: # Send to Email
            if member.__type__ == 'user': # Only send emails to individual users
                send_email(member, **rendered_message['e'])
        if route == 'n' and 'n' in rendered_message: # Save message in message table (to be seen as a notification)
            m = Message()
            m.subject = rendered_message['n']['subject']
            m.content = rendered_message['n']['content']
            m.target  = member
            Session.add(m)
            #member.messages_to.append(m)
            update_member_messages(member)
    
    log.info("%s was sent the message '%s', routing via %s" % (
        member.name, name, message_tech_options
    ))


def send_notification(members, **kwargs): #members, rendered_message
    """
    Threaded message system, save and handles propogating the message to different technologies for all members of a group or an indvidual
    """
    
    #rendered_message['n']['subject'] = str(member)+': '+rendered_message['n']['subject']
    #rendered_message['n']['content'] = str(member)+': '+rendered_message['n']['content']
    
    for member in get_members(members, expand_group_members=True):
        # TODO - append 'to' to messages
        _send_notification_to_user(member, **kwargs)
        #if member.__type__ == 'group':
        #    send_notification(get_group_member_username_list(member), **kwargs)
            
    
    Session.commit()



#-------------------------------------------------------------------------------


def temp():

    """
    Takes - either
        a comma separated list of members as string
            (WARNING if this strings contains group names the notification wont propergate to all members,
            if passing a string list it is assumed that all group links have been followed)
        a list of member objets (this can contains groups and will call this method recursivly)
        a single member - if group get all sub members
        
    message can be a MessageData object or a dict with name, default_route, subject and content

    """
    
    single_member = None
    
    
    
    # If 'members' is not a list it is either a sting username or a member object
    #  deal with a single member
    #  if a group, get list of all submembers
    if not isinstance(members, list):
        # get member object
        member = _get_member(members)
        single_member = member
        if not member:
            log.error('unable to find member (%s) to send a message to' % 'TODO')
            return
    
        # Save the notification for this member
        #  - although the message will be threaded to agregate, we need to save the notification for the actual destination user (without the appended str bits)
        #  - see 'if user' below for remove notification from thred aggregation for single member
        m = Message()
        m.subject = message.get('subject')
        m.content = message.get('content')
        m.target  = member
        Session.add(m)
        update_member_messages(member)
        
        # AllanC - bit of a botch here. if a notificaiton is sent to a group and needs to be propergated to members, we nee to record who the message was origninally too.
        message['subject'] = str(member)+': '+message.get('subject')
        message['content'] = str(member)+': '+message.get('content')
        
        # Pre generate list of members 'too'
        members = []
        if member.__type__ == 'user':
            members.append(member)
        elif member.__type__ == 'group':
            members = member.all_sub_members()
    
    # If there are any groups in the list of members too, then send to all submembers recursivly
    # As the message dict subject and contnet gets appended too for each group
    for group in [m for m in members if hasattr(m, 'all_sub_members')]:
        send_notification(group, message, delay_commit=True)
        members.remove(group) # no need to have group in this send list any longer as all members have been notifyed by the call above
        

    #

    
    # Because we saved the actual notification above, if we have a single user we don't need to save the notification in the worker thread
    if single_member and single_member.__type__ == 'user':
        del rendered_message['n']
