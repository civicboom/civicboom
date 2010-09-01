"""
A collection of MessageData subclasses, which can be sent to members like so

import civicboom.lib.communication.messages as messages

m1 = Member()
m2 = Member()
m1.send_message(messages.tipoff(reporter=m2, tipoff="there is a bomb"))
"""

from civicboom.lib.communication.email import send_email
from civicboom.model      import Message
from civicboom.model.meta import Session
from civicboom.lib.database.get_cached import update_member_messages
from pylons.i18n          import lazy_ugettext as _
from webhelpers.html      import HTML

import re
import logging
log = logging.getLogger(__name__)


class MessageData(object):
    name          = ""
    default_route = ""
    subject       = ""
    content       = ""

    def __init__(self, **kwargs):
        """
        The subclass has already specified a message format, we now put our
        kwargs into that format. If any of the args have a __link__ method,
        we call that to turn it into an HTML link to be put in the message;
        if not, use __unicode__ and include it as a string.
        """
        linked = {}
        for key in kwargs:
            if hasattr(kwargs[key], "__link__"):
                linked[key] = HTML.a(unicode(kwargs[key]), href=kwargs[key].__link__())
            else:
                linked[key] = HTML.span(unicode(kwargs[key])) # the span here is for security, it does HTML escaping
        self.subject = unicode(self.subject) % linked
        self.content = unicode(self.content) % linked


generators = [
    ["msg_test",                             "",   _("a test message"),              _("%(text)s")],
    ["followed_by",                          "ne", _("new follower"),                _("%(reporter)s is now following you")],
    ["followed_on_signup",                   "ne", _("new sign up via widget"),      _("%(reporter)s has signed up via your widget and is now following you")],
    ["follow_stop",                          "",   _("lost a follower"),             _("%(reporter)s has stopped following you")],
    ["tipoff",                               "ne", _("tipoff"),                      _("you have been tipped off by %(reporter)s - %(tipoff)s")],
    ["tipoff_accepted",                      "ne", _("tipoff accepted"),             _("%(reporter)s has accepted your _tipoff - %(tipoff)s")],
    ["tipoff_declined",                      "ne", _("tipoff declined"),             _("%(reporter)s has declined your _tipoff - %(tipoff)s")],
    ["tipoff_deleted",                       "",   _("tipoff deleted"),              _("%(reporter)s has withdrawn their _tipoff")],
    ["instant_news_update",                  "n",  _("_reporter has updated their instant news"), _("%(reporter)s has updated their instant news: %(instant)s_news")],
    ["interview_used",                       "ne", _("interview has been used"),     _("%(reporter)s has written a _article in response to the interview with you called %(article)s")],
    ["article_published_by_followed",        "ne", _("new _article"),                _("%(reporter)s has written new _article : %(article)s")],
    ["article_published_by_followed_mobile", "ne", _("new mobile _article"),         _("%(reporter)s has uploaded mobile _article : %(article)s")],
    ["assignment_response",                  "ne", _("_assignment response"),        _("%(reporter)s has published a _report called %(article)s based on your _assignment %(assignment)s")],
    ["assignment_response_mobile",           "ne", _("_assignment mobile response"), _("%(reporter)s has uploaded mobile _article titled %(article)s based on your _assignment %(assignment)s")],
    ["topic_update",                         "ne", _("topic update to an _article"), _("%(reporter)s wrote a topic update for your _report %(partent)s_article titled %(article)s")],
    ["article_rated",                        "",   _("_article rated"),              _("your _article %(article)s was rated a %(rating)s")],
    ["comment",                              "n",  _("comment made on _article"),    _("%(reporter)s commented on your _article %(article)s")],  #Also passes comment.contents as a string and could be used here
    ["eyewitness_report",                    "ne", _("new eyewitness"),              _("%(reporter)s wrote an eyewitness for your _article %(article)s")],
    ["assignment_created",                   "ne", _("new _assignment"),             _("%(reporter)s created a new _assignment %(assignment)s")],
    ["assignment_updated",                   "ne", _("_assignment updated"),         _("%(reporter)s has updated their _assignment %(assignment)s")],
    ["assignment_accepted",                  "ne", _("_assignment accepted"),        _("%(member)s accepted your _assignment %(assignment)s")],
    ["assignment_interest_withdrawn",        "",   _("_assignment interest withdrawn"), _("%(member)s withdrew their interest in your _assignment %(assignment)s")],
    ["assignment_invite",                    "ne", _("closed _assignment invitation") , _("%(member)s has invited you to participate in the _assignment %(assignment)s")],
    ["article_disasociated_from_assignment", "n",  _("_article dissasociated from _assignment"), _("%(member)s dissasociated your _article %(article)s from the _assignment %(assignment)s")],
    ["assignment_canceled",                  "ne", _("_assignment you previously accepted has been canceled"), _("%(reporter)s canceled the _assignment %(assignment)s")],
    ["article_approved",                     "n",  _("_article approved by organisation"), _("%(member)s has approved your _article %(content)s in the response to their _assignment %(parent)s. Check your email for more details")],
    ["boom_article",                         "ne", _("_article boom"),               _("%(member)s thinks you might find this _article interesting %(article)s")],
    ["boom_assignment",                      "ne", _("_assignment boom"),            _("%(member)s thinks you might want to add your opinion to this _assignment %(assignment)s")],
    ["syndicate_accept",                     "n",  _("_article was syndicated"),     _("%(reporter)s has accepted your syndication request for _article %(article)s. Check your email for the details")],
    ["syndicate_decline",                    "ne", _("_article was declined syndication"), _("%(reporter)s declined your syndication request for _article %(article)s. Your _article is now publicly visable")],
    ["syndicate_expire",                     "ne", _("_article was not syndicated"), _("Your syndication request for %(article)s was unsuccessful. Your _article is now publicly visable")],
    ["assignment_due_7days",                 "ne", _("_assignment due next week"),   _("The _assignment you accepted %(assignment)s is due next week")],
    ["assignment_due_1day",                  "ne", _("_assignment due tomorrow"),    _("The _assignment you accepted %(assignment)s is due tomorrow")],
]

#
# Turn the table into classes
#
for _name, _default_route, _subject, _content in generators:
    class gen(MessageData):
        name          = _name
        default_route = _default_route
        subject       = _subject
        content       = _content
    globals()[_name] = gen


def send_message(member, message_data, delay_commit=False):
    """
    private guts to the message system, save and handles propogating the message to different technologies
    """

    # Get propergate settings - what other technologies is this message going to be sent over
    # Attempt to get routing settings from the member's config; if that fails, use the
    # message's default routing
    message_tech_options = member.config.get("route_"+message_data.name, message_data.default_route)

    # Iterate over each letter of tech_options - each letter is a code for the technology to send it to
    # e.g 'c'  will send to Comufy
    #     'et' will send to email and twitter
    #     'n'  is a normal notification
    #     ''   will dispose of the message because it has nowhere to go
    for c in message_tech_options:
        if c == 'c': # Send to Comufy
            pass
        if c == 'e': # Send to Email
            # groups don't have an email address
            if hasattr(member, "email"):
                send_email(member.email, subject=message_data.subject, content_html=message_data.content)
        if c == 't': # Send to Twitter
            pass
        if c == 'n': # Save message in message table (to be seen as a notification)
            m = Message()
            m.subject = message_data.subject
            m.content = message_data.content
            member.messages_to.append(m)
            update_member_messages(member)
            if not delay_commit:
                Session.commit()

    log.info("%s was sent the message '%s', routing via %s" % (
        member.name, message_data.subject, message_tech_options
    ))
