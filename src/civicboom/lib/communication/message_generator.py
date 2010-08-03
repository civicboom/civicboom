from pylons.i18n.translation import _, ungettext

from message_sender import term_replace, message_to, message_to_from, message_public, message_creator
from message_sender import message_default_route, message_title



message_content = {}

#-------------------------------------------------------------------------------
# Message Generator
#-------------------------------------------------------------------------------
"""
 Adding method calls here with decorators will automatically update any message setting page as it will look at the data gererated by the decorators
 Use:
    Call commit after sending message

"""

#-------------------------------------------------------------------------------
# Message Mehtod Decorators
#-------------------------------------------------------------------------------
#
# Used to set paramiters for the message def, this sets the dictonarys in message_send to create the right message to the right place

class messageDeafultRoute(object):
  def __init__(self, arg1):
    self.arg1 = arg1
  def __call__(self, f):
    message_default_route[f.__name__] = self.arg1
    def wrapped_f(*args,**kargs):
      return f(*args,**kargs)
    wrapped_f.__name__ = f.__name__
    return wrapped_f

class messageTitle(object):
  def __init__(self, arg1):
    self.arg1 = arg1
  def __call__(self, f):
    message_title[f.__name__] = term_replace(self.arg1)
    def wrapped_f(*args,**kargs):
      return f(*args,**kargs)
    wrapped_f.__name__ = f.__name__
    return wrapped_f

class messageContent(object):
  def __init__(self, arg1):
    self.arg1 = arg1
  def __call__(self, f):
    message_content[f.__name__] = term_replace(self.arg1)
    def wrapped_f(*args,**kargs):
      return f(*args,**kargs)
    wrapped_f.__name__ = f.__name__
    return wrapped_f

def messageSend(f):
  def new_f(*args, **kargs):
    message_type = f.__name__
    message      = message_creator(message_content[message_type],**kargs)
    if 'message_public_source' in kargs:
      message_public(kargs['message_public_source'], message)
    message_to(args, message, message_type)
    f_return = f(*args, **kargs)
    if f_return:
      return f_return
    return message
  new_f.__name__ = f.__name__
  return new_f

#def messagePublic(f):
#  def new_f(*args, **kargs):
#    message_type = f.__name__
#    message      = message_creator(message_content[message_type],**kargs)
#    if 'public_source_reporter' in kargs:
#      message_public(kargs['public_source_reporter'], message)
#    f_return = f(*args, **kargs)
#    if f_return:
#      return f_return
#    return message
#  new_f.__name__ = f.__name__
#  return new_f


#-------------------------------------------------------------------------------
# Reporter to Reporter Messages
#-------------------------------------------------------------------------------

# Placeholder
#'reporter'  'message from another term:reporter'


#-------------------------------------------------------------------------------
# System Messages
#-------------------------------------------------------------------------------

@messageDeafultRoute('ne')
@messageTitle('new follower')
@messageContent('arg:reporter is now following you')
@messageSend
def followed(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('new sign up via widget')
@messageContent(_('%(user) has signed up via your widget and is now following you'))
@messageSend
def followed_on_signup(to,**kargs):
  pass


@messageDeafultRoute('')
@messageTitle('lost a follower')
@messageContent('arg:reporter has stopped following you')
@messageSend
def follow_stop(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('tipoff')
@messageContent('You have been tipped off by arg:reporter - arg:tipoff')
@messageSend
def tipoff(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('tipoff accepted')
@messageContent('arg:reporter has accepted your term:tipoff - arg:tipoff')
@messageSend
def tipoff_accepted(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('tipoff declined')
@messageContent('arg:reporter has declined your tipoff - arg:tipoff')
@messageSend
def tipoff_declined(to,**kargs):
  pass

@messageDeafultRoute('')
@messageTitle('tipoff deleted')
@messageContent('arg:reporter has withdrawn their tipoff')
@messageSend
def tipoff_deleted(to,**kargs):
  pass

@messageDeafultRoute('n')
@messageTitle('term:reporter has updated their instant news')
@messageContent('arg:reporter has updated their instant news: arg:instant_news')
@messageSend
def instant_news_update(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('interview has been used')
@messageContent('arg:reporter has written a term:article in response to the interview with you called arg:article')
@messageSend
def interview_used(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('new term:article')
@messageContent('arg:reporter has written new term:article : arg:article')
@messageSend
def article_published_by_followed(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('new mobile term:article')
@messageContent('arg:reporter has uploaded mobile term:article : arg:article')
@messageSend
def article_published_by_followed_mobile(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('term:assignment response')
@messageContent('arg:reporter has published a term:report called arg:article based on your term:assignment arg:assignment')
@messageSend
def assignment_response(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('term:assignment mobile response')
@messageContent('arg:reporter has uploaded mobile term:article titled arg:article based on your term:assignment arg:assignment')
@messageSend
def assignment_response_mobile(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('topic update to an term:article')
@messageContent('arg:reporter wrote a topic update for your term:report arg:partent_article titled arg:article')
@messageSend
def topic_update(to,**kargs):
  pass

@messageDeafultRoute('')
@messageTitle('term:article rated')
@messageContent('your term:article arg:article was rated a arg:rating')
@messageSend
def article_rated(to,**kargs):
  pass

@messageDeafultRoute('n')
@messageTitle('comment made on term:article')
@messageContent('arg:reporter commented on your term:article arg:article') #Also passes comment.contents as a string and could be used here
@messageSend
def comment(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('new eyewhitness')
@messageContent('arg:reporter wrote an eyewitness for your term:article arg:article')
@messageSend
def eyewhitness_report(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('new term:assignment')
@messageContent('arg:reporter created a new term:assignment arg:assignment')
# AllanC: ok ... all messages are strings, great, flexable, however, the mobile needs to know if a notification is an assignment or not so it can display extra info
#         but all it is, is a string ... so we either hard code the text to search for into the mobile (BAD IDEA), or, seeing as the server is holding all the cards anyway, the server could do it
#         but here is the snag, this string checking is hourse crap, what about multi lingual?
#         bottom line, we need some kind of tiny enum id to tag a range of special notifications with a type
#         one of these types is "New Assignment" - Response "Accept" or "Decline"
#         for now the Message object in indicofb.lib.indiconews.py has hard coded string to search for, this is a short term botch! and should be looked at in the refactoring July2010
#         Bottom line - DO NOT MODIFY THIS MESSAGE CONTENT WITHOUT MODIFYING indicofb/lib/json_maker:json_messages:response_type
#@messagePublic
@messageSend
def assignment_created(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('term:assignment updated')
@messageContent('arg:reporter has updated their term:assignment arg:assignment')
#@messagePublic
@messageSend
def assignment_updated(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('term:assignment accepted')
@messageContent('arg:reporter accepted your term:assignment arg:assignment')
@messageSend
def assignment_accepted(to,**kargs):
  pass

@messageDeafultRoute('')
@messageTitle('term:assignment interest withdrawn')
@messageContent('arg:reporter withdrew their interest in your term:assignment arg:assignment')
@messageSend
def assignment_interest_withdrawn(to,**kargs):
  pass

@messageDeafultRoute('n')
@messageTitle('term:article dissasociated from term:assignment')
@messageContent('arg:reporter dissasociated your term:article arg:article from the term:assignment arg:assignment')
@messageSend
def article_disasociated_from_assignment(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('term:assignment you previously accepted has been canceled')
@messageContent('arg:reporter canceled the term:assignment arg:assignment')
@messageSend
def assignment_canceled(to,**kargs):
  pass

@messageDeafultRoute('n') #This only has a notifcation route because a full explanitary email is generated for the user
@messageTitle('term:article approved by organisation')
@messageContent('arg:reporter has approved your term:article arg:article in the response to their term:assignment arg:assignment. Check your email for more details')
@messageSend
def article_approved(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('term:article boom')
@messageContent('arg:reporter thinks you might find this term:article interesting arg:article')
@messageSend
def boom_article(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('term:assignment boom')
@messageContent('arg:reporter thinks you might want to add your opinion to this term:assignment arg:assignment')
@messageSend
def boom_assignment(to,**kargs):
  pass

@messageDeafultRoute('n') #By default just a notification because a full detailed email is sent
@messageTitle('term:article was syndicated')
@messageContent('arg:reporter has accepted your syndication request for term:article arg:article. Check your email for the details')
@messageSend
def syndicate_accept(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('term:article was declined syndication')
@messageContent('arg:reporter declined your syndication request for term:article arg:article. Your term:article is now publicly visable')
@messageSend
def syndicate_decline(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('term:article was not syndicated')
@messageContent('Your syndication request for arg:article was unsuccessful. Your term:article is now publicly visable')
@messageSend
def syndicate_expire(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('term:assignment due next week')
@messageContent('The term:assignment you accepted arg:assignment is due next week')
@messageSend
def assignment_due_7days(to,**kargs):
  pass

@messageDeafultRoute('ne')
@messageTitle('term:assignment due tomorrow')
@messageContent('The term:assignment you accepted arg:assignment is due tomorrow')
@messageSend
def assignment_due_1day(to,**kargs):
  pass


#Interview request
#respond to interview
