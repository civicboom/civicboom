from civicboom.lib.base                import config, c
from civicboom.lib.messages.email      import send_email
from civicboom.model                   import Message, Member
from civicboom.model.meta              import Session
from civicboom.lib.database.get_cached import update_user_messages

#, get_function_name
#import indicofb.lib.helpers as h

import re

import logging
log = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# Global Variables
#-------------------------------------------------------------------------------

message_default_route = {}
message_title         = {}


#-------------------------------------------------------------------------------
# Message Markup processor
#-------------------------------------------------------------------------------
def term_replace(message):
  def term_lookup(m):
    term_type = m.group(1)
    if term_type in config['terminology']:
      return config['terminology'][term_type]
    return term_type
  term_regex = re.compile(r'term:(.+?)\b',re.DOTALL)
  return term_regex.sub(term_lookup, message)

#-------------------------------------------------------------------------------
# Message Sender
#-------------------------------------------------------------------------------
"""
  None of these methods should EVER be imported by another module
  Only message_generator to access these directly
   - each message is a shot string
   - any linkable items (such as articles and assignments) are identifyed and link tags automatically put in
   - the message is then stored as text with a timestamp so the user to be alerted to the NEW messages since last login
   - because the messages are text they can be propergated to a range of communication technologies e.g. email, msn, opensocial alerts, twitter
   - there are default routes for these messages as well as allowing the user to override these defaults customising how they recive the message or even not at all

  Use:
   - This module should not be used directly, use message_generator to generate messages
     - messages are created with message_to and message_to_from
  
  Example:
    Don't use this module directly, see message_generator
   
"""

#-------------------------------------------------------------------------------
# Generate Messages - 3 ways of sending messages
#-------------------------------------------------------------------------------
def message_to_from(reporter_to, reporter_from, message, type='reporter'):
    """
    
    """
    if not (isinstance(reporter_to,Reporter) and isinstance(reporter_from,Reporter)): #and isinstance(message,str)
        log.debug(__name__+' - Message send failed: passed inapproriate types')
        return False
    m = Message()
    m.destination = reporter_to
    m.source      = reporter_from
    m.messageText = h.clean_article_html(str(message))
    m.type        = type
    message_send(m)

# message_to can be passed a single reporter or a list of reporters. The message will then be sent to all recipients
def message_to(reporter, message, type):
    """
    
    """
    # If reporter is a Reporter object then send the message
    if (isinstance(reporter,Reporter) and isinstance(type,str)):
        m = Message()
        m.destination = reporter
        m.messageText = h.clean_article_html(str(message))
        m.type        = type
        message_send(m)
    # If reporter is not a Reporter object it may be a list, process the message for the list
    #   unfortunatly the SQLAlchemy object is not identifyable with "if type(reporter) is list"
    #   so we need to do a botch and put it in a try to process the list ... if you can do this in a better way.
    else:
        try   :
            for r in reporter: message_to(r, message, type)
        except:
            log.debug(__name__+' - Message send failed: passed inapproriate types')
            #print "reporter: %s - %s" % (reporter.ReporterName, isinstance(reporter,Reporter))
            #print "message: %s - %s" % (message, isinstance(message,str))
            #print "type: %s - %s" % (type, isinstance(type,str))
            return False

def message_public(reporter_from, message, type=''):
    """
    
    """
    if not (isinstance(reporter_from,Reporter) and isinstance(type,str)):
        log.debug(__name__+':'+get_function_name()+' - failed: passed inapproriate types')
        return False
    #m = MessagePublic()
    m = Message()
    m.source      = reporter_from
    m.messageText = h.clean_article_html(str(message))
    m.type        = type
    Session.save(m)
    #update_reporter_messages_public(m.source) #not implemented yet


#-------------------------------------------------------------------------------
# Message Send
#-------------------------------------------------------------------------------
def message_send(m):
    """
    private guts to the message system, save and handels propergeting the message to differnt technologies
    """
    if not (type(m) is Message and hasattr(m,'destination') and hasattr(m,'messageText') and hasattr(m,'type')):
        log.debug('Message send failed: message data incomplete')
        return False
  
    # Get propergate settings - what other technologies is this message going to be sent over
    message_tech_options = ''
    message_description  = m.type
    if m.type in message_default_route:
        message_tech_options = message_default_route[m.type] # Default technologys to send this message type over
    if hasattr(m.destination, 'messageOptions') and type in m.destination.messageOptions:
        message_tech_options = m.destination.messageOptions[m.type]  # if user has own setting override default
    
    # Iterate over each letter of tech_options - each letter is a code for the technology to send it to
    # e.g 'c'  will send to Comufy
    #     'et' will send to email and twitter
    #     'n'  is a normal notification
    #     ''   will dispose of the message because it has nowhere to go
    save_message = False
    for i in range(len(message_tech_options)):
        if message_tech_options[i] == 'c': #Send to Comufy
            pass 
        if message_tech_options[i] == 'e': #Send to Email
            send_email(m.destination, subject=message_title[m.type] ,content_html=m.messageText)
        if message_tech_options[i] == 't': #Send to Twitter
            pass
        if message_tech_options[i] == 'n': #Save message in message table (to be seen as a notification)
            save_message = True
  
    if save_message:
        Session.save(m)
        update_reporter_messages(m.destination)
    else:
        Session.expunge(m)

#-------------------------------------------------------------------------------
# Message Creator
#-------------------------------------------------------------------------------
def message_creator(message, **kargs):
    """
    Used to process the mini markup of the message system and put in links
    
    Takes a string with custom markup and peices together a complete message
     - replaces terminology e.g turns term:article into 'article' (or whatever the global terminolgy is currently set to)
     - looks at arg:article or arg:reporter and replaces it with a <a href="">Correct Name</a> by looking at kargs
      - message propergator code (for twitter or sms) may remove these <a> tags later to fit 160 chars but the full message will be saved to be seen on the site later
    """
    #Replace arg:??? with formatted link type from kargs
    def arg_formater(m):
        arg_type = m.group(1)
        if arg_type in kargs:
            def format_link_to(o):
                def url_for_absolute(**kargs):
                    return url_for(host=c.host_name, **kargs)
                def link(href,text):
                    return '<a href="%s">%s</a>' % (href,text)
                if isinstance(o,Reporter):
                    return link(url_for_absolute(controller='reporter', action='profile', id=o.ReporterName),o.ReporterName)
                if isinstance(o,NewsArticle):
                    return link(url_for_absolute(controller='article',action='view',id=o.id),o.Title)
                if isinstance(o,Assignment):
                    return link(url_for_absolute(controller='assignment',action='view_assignment',id=o.id),o.title)
                if isinstance(o,TipoffTo):
                    o = o.tipoff
                if isinstance(o,Tipoff):
                    return h.truncate(o.description, length=60, indicator='...', whole_word=True)  #AllanC - cant currently link directly to tipoffs, may be useful in future
                if isinstance(o,str):
                    return o
                return str(o)
            return format_link_to(kargs[arg_type])
        log.debug(__name__+': Investigate! Unknown arg type'+arg_type)
        return arg_type
    arg_regex = re.compile(r'arg:(.+?)\b',re.DOTALL)
    message = arg_regex.sub(arg_formater, message)

    return message