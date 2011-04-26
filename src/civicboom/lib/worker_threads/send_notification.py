import logging
log = logging.getLogger(__name__)

def _send_notification_to_user(member, message_data, member_to=None, delay_commit=False):
    """
    Internal call
    Must be passed member object
    Actually sends a message
    """
    from civicboom.model.meta              import Session
    from civicboom.model.message           import Message
    from civicboom.lib.database.get_cached import update_member_messages
    from civicboom.lib.communication.email_lib import send_email
    
    # Get propergate settings - what other technologies is this message going to be sent over
    # Attempt to get routing settings from the member's config; if that fails, use the
    # message's default routing
    message_tech_options = member.config.get("route_"+message_data['name'], message_data['default_route'])
    
    subject = message_data['subject']
    content = message_data['content']
    
    # AllanC - bit of a botch here. if a notificaiton is sent to a group and needs to be propergated to members, we nee to record who the message was origninally too.
    if member_to and member_to!=member:
        subject = str(member_to)+': '+subject
        content = str(member_to)+': '+content
    
    # Iterate over each letter of tech_options - each letter is a code for the technology to send it to
    # e.g 'c'  will send to Comufy
    #     'et' will send to email and twitter
    #     'n'  is a normal notification
    #     ''   will dispose of the message because it has nowhere to go
    for route in message_tech_options:
        if route == 'c': # Send to Comufy
            pass
        if route == 'e': # Send to Email
            if hasattr(member, 'email'):
                send_email(member, subject=subject, content_html=content)
        if route == 't': # Send to Twitter
            pass
        if route == 'n': # Save message in message table (to be seen as a notification)
            m = Message()
            m.subject = subject
            m.content = content
            m.target  = member
            Session.add(m)
            #member.messages_to.append(m)
            update_member_messages(member)
            if not delay_commit:
                Session.commit()
    
    log.info("%s was sent the message '%s', routing via %s" % (
        member.name, subject, message_tech_options
    ))


def send_notification(member, message_data, delay_commit=False):
    """
    Threaded message system, save and handles propogating the message to different technologies for all members of a group or an indvidual
    """
    from civicboom.model.meta              import Session
    from civicboom.lib.database.get_cached import get_member as _get_member

    # get member object
    member_to = _get_member(member)
    if not member_to:
        log.error('unable to find member (%s) to send a message to' % str(member))
        return
    
    members = []
    if member_to.__type__ == 'user':
        members.append(member_to) #.username
    elif member_to.__type__ == 'group':
        members = member_to.all_sub_members() #_get_member_username_list(member_to)
    
    for member in members:
        _send_notification_to_user(member, message_data, member_to=member_to, delay_commit=True)
    
    if not delay_commit:
        Session.commit()
