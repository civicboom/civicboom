import logging
log = logging.getLogger(__name__)

from civicboom.lib.database.get_cached import get_member, get_members


from civicboom.model.meta              import Session
from civicboom.model.message           import Message
from civicboom.lib.cache               import invalidate_list_version
from civicboom.lib.communication.email_lib import send_email
import civicboom.lib.helpers as helpers

import collections
import os


# AllanC - sorry Shish - this broke notifications before the KM demo and we needed it working
from pylons.templating  import render_mako
from mako.template import Template
from mako.lookup import TemplateLookup


def send_notification(members, message): #members, rendered_message
    """
    Threaded message system
    Save and handles propogating the message to different technologies for all members of a group or an indvidual
    """
    
    from cbutils.worker import config

    message['source'] = get_member(message.get('source') or message.get('source_id')) or message.get('source') # Attempt to normalize source member

    # Multiple memebrs
    if isinstance(members, list):
        
        for member in get_members(members, expand_group_members=True):
            message['target_username'] = member.id # Overlay the direct target member of this message as an additional param
            send_notification(member, message)
            #if member.__type__ == 'group':
            #    send_notification(get_group_member_username_list(member), **kwargs)
        Session.commit() # No need to commits as all workers commit at end by default
        
    # Single member
    else:
        member = get_member(members)
        
        # AllanC - Messages can be passed without a default_route or name if they are not auto generated notifications
        #          in this case they are deemed "user to user" messages and have enforced default template and route
        if 'default_route' not in message:
            message['default_route'] = 'e'
        if 'name' not in message:
            message['name'] = 'message'
        
        # Get propergate settings - what other technologies is this message going to be sent over
        # Attempt to get routing settings from the member's config; if that fails, use the
        # message's default routing
        message_tech_options = member.config.get("route_"+message.get('name','default'), message.get('default_route'))
        
        # Iterate over each letter of tech_options - each letter is a code for the technology to send it to
        # e.g 'c'  will send to Comufy
        #     'et' will send to email and twitter
        #     'n'  is a normal notification
        #     ''   will dispose of the message because it has nowhere to go
        for route in message_tech_options:
            
            # -- Comufy --------------------------------------------------------
            if route == 'c':
                pass
            
            # -- Email ---------------------------------------------------------
            if route == 'e':
                if member.__type__ == 'user': # Only send emails to individual users
                    
                    # Feature #498 - Check for existing email template and attempt to render
                    def notification_template(template):
                        template_path = os.path.join("email", "notifications", template+".mako")
                        #if os.path.exists(os.path.join(config['path.templates'], template_path)):
                        if os.path.exists(os.path.join("civicboom/templates", template_path)):
                            return template_path
                        return 'email/notifications/default.mako'
                    
                    #if config['debug'] == True or config['debug'] == "true": # debug is a string, so config['debug'] == "false" == Trues
                    if config['worker.queue.type'] == 'inline':
                        c = render_mako(
                            notification_template(message.get('name')) ,
                            extra_vars ={
                                "kwargs": message,
                            }
                        )
                    else:  # pragma: no cover - test mode uses inline rendering, this is stand-alone
                        l = TemplateLookup(
                            directories=['.', 'civicboom/templates'],
                            input_encoding='utf-8',
                            output_encoding='utf-8'
                        )
                        f = os.path.join("civicboom/templates", notification_template(message.get('name')))
                        t = Template(filename=f, lookup=l)
                        c = t.render_unicode(kwargs=message, h=helpers)
                    send_email(
                        member,
                        subject      = message.get('subject'), #, _('_site_name notification')
                        content_html = c,
                    )

            # -- Notification --------------------------------------------------
            # Save message in message table (to be seen as a notification)
            if route == 'n':
                m = Message()
                m.subject = message['subject']
                m.content = message['content']
                m.target  = member
                Session.add(m)
                #member.messages_to.append(m)
                #invalidate_list_version('mesages_index', 'notification', m.target.id) # AllanC - we can replace this invalidation with a sqlalchemy list watching trigger maybe?
            
            # ------------------------------------------------------------------
        
        log.debug("%s was sent the message '%s', routing via %s" % (
            member.username, message.get('name'), message_tech_options
        ))

    return True