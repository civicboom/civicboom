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
            #if member.__type__ == 'user': # AllanC - not needed as all members should be 'User' objects and not 'Groups' by this point anyway.
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
    
    for member in get_members(members):
        _send_notification_to_user(member, **kwargs)
    
    Session.commit()
