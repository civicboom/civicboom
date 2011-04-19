"""
A collection of MessageData subclasses, which can be sent to members like so

import civicboom.lib.communication.messages as messages

m1 = Member()
m2 = Member()
m1.send_message(messages.tipoff(member=m2, tipoff="there is a bomb"))
"""

from pylons import config
from pylons.i18n          import lazy_ugettext as _
from webhelpers.html      import HTML

import civicboom.lib.worker as worker

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
        if config['feature.notifications']: # Only generate messages if notifications enabled - required to bypass requireing the internationalisation module to be activated
            linked = {}
            for key in kwargs:
                if hasattr(kwargs[key], "__link__"):
                    linked[key] = HTML.a(unicode(kwargs[key]), href=kwargs[key].__link__())
                else:
                    linked[key] = HTML.span(unicode(kwargs[key])) # the span here is for security, it does HTML escaping
                
            self.subject = unicode(self.subject) % linked
            self.content = unicode(self.content) % linked
        else:
            self.subject = u'notification generation diabled'
            self.content = u'notification generation diabled'

    def to_dict(self):
        return {
            "name": self.name,
            "default_route": self.default_route,
            "subject": self.subject,
            "content": self.content,
        }


generators = [
    # Testing
    ["msg_test",                             "",   _("a test message"),              _("%(text)s")],
    
    # Member actions
    ["followed_by",                          "ne", _("new follower"),                _("%(member)s is now following you")],
    ["followed_on_signup",                   "ne", _("new sign up via widget"),      _("%(member)s has signed up via your widget and is now following you")],
    ["follow_stop",                          "e",   _("lost a follower"),             _("%(member)s has stopped following you")],
    
    # GregM: Follow action notifications
    ["follower_trusted",                     "ne", _("trusted follower"),             _("%(member)s has made you a trusted follower, you can now see their private content")],
    ["follower_distrusted",                  "ne", _("no longer a trusted follower"), _("%(member)s has stopped you being a trusted follower, you will not be able to see their private content")],
    ["follow_invite_trusted",                "ne", _("trusted follower invite"),      _("%(member)s has invited you to follow them as a trusted follower, if you accept you will be able see their private content")],

    # New Content
    ["article_published_by_followed",        "ne", _("new _article"),                _("%(creator)s has written new _article : %(article)s")],
    ["article_published_by_followed_mobile", "ne", _("new mobile _article"),         _("%(member)s has uploaded mobile _article : %(article)s")],
    
    # Content Actions
    ["article_rated",                        "e",   _("_article rated"),              _("your _article %(article)s was rated a %(rating)s")],
    ["comment",                              "ne",  _("comment made on _article"),    _("%(member)s commented on your _article %(article)s")],  #Also passes comment.contents as a string and could be used here

    # Content Responses
    ["assignment_response_mobile",           "ne", _("_assignment mobile response"), _("%(member)s has uploaded mobile _article titled %(article)s based on your _assignment %(assignment)s")],
    ["new_response",                         "ne", _("new response"),                _("%(member)s has published a response to your content %(parent)s called %(content)s ")],
    
    # Assignment Actions
    ["assignment_created",                   "ne", _("new _assignment"),             _("%(creator)s created a new _assignment %(assignment)s")],
    ["assignment_updated",                   "ne", _("_assignment updated"),         _("%(creator)s has updated their _assignment %(assignment)s")],
    ["assignment_canceled",                  "ne", _("_assignment you previously accepted has been cancelled"), _("%(member)s cancel'ed the _assignment %(assignment)s")],
    ["assignment_accepted",                  "ne", _("_assignment accepted"),        _("%(member)s accepted your _assignment %(assignment)s")],
    ["assignment_interest_withdrawn",        "e",   _("_assignment interest withdrawn"), _("%(member)s withdrew their interest in your _assignment %(assignment)s")],
    ["assignment_invite",                    "ne", _("closed _assignment invitation") , _("%(member)s has invited you to participate in the _assignment %(assignment)s")],

    # Assignment Timed Tasks
    ["assignment_due_7days",                 "ne", _("_assignment alert: due next week"),   _("The _assignment you accepted %(assignment)s is due next week")],
    ["assignment_due_1day",                  "ne", _("_assignment alert: due tomorrow"),    _("The _assignment you accepted %(assignment)s is due tomorrow")],

    # Response Actions
    ["article_disassociated_from_assignment","n",  _("_article disassociated from _assignment"), _("%(member)s disassociated your _article %(article)s from the _assignment %(assignment)s")],
    ["article_approved",                     "n",  _("_article approved by organisation"), _("%(member)s has approved your _article %(content)s in the response to their _assignment %(parent)s. Check your email for more details")],
      # TODO: response seen

    # Groups to group
    ["group_new_member",                     "ne" , _("_member joined group"),        _("%(member)s has joined %(group)s")],
    ["group_role_changed",                   "ne" , _("_member role changed"),        _("%(admin)s changed %(member)ss role for %(group)s to %(role)s")],
    ["group_remove_member_to_group",         "ne", _("_member removed from _group"), _("%(admin)s removed %(member)s from %(group)s")],
    ["group_join_request",                   "ne" , _("join request"),                _("%(member)s has requested to join %(group)s")],
    
    # Groups to members
    ["group_deleted",                        "ne", _("_group deleted"),              _("The _group %(group)s has been deleted by %(admin)s")],
    ["group_invite",                         "ne", _("_group invitation"),           _("%(admin)s invited you to join %(group)s as a %(role)s")],
    ["group_request_declined",               "ne" , _("_group membership request declined"), _("your membership request to join %(group)s was declined")],
    ["group_invitation_declined",            "e"  , _("_group membership invitation declined"), _("%(member)s declined the invitation to join %(group)s")],
    ["group_request_accepted",               "ne" , _("_group request accepted"),     _("%(admin)s accepted your _group membership request. You are now a member of %(group)s")],
    ["group_remove_member_to_member",        "ne", _("removed from _group"),         _("%(admin)s removed your membership to %(group)s")],
    
    # Aggregation
    ["boom_article",                         "ne", _("_article boomed"),               _("%(member)s thinks you might find this _article interesting %(article)s")],
    ["boom_assignment",                      "ne", _("_assignment boomed"),            _("%(member)s thinks you might want to add your opinion to this _assignment %(assignment)s")],

    # Syndication
    ["syndicate_accept",                     "n",  _("_article was syndicated"),     _("%(member)s has accepted your syndication request for _article %(article)s. Check your email for the details")],
    ["syndicate_decline",                    "ne", _("_article was declined syndication"), _("%(member)s declined your syndication request for _article %(article)s. Your _article is now publicly visible")],
    ["syndicate_expire",                     "ne", _("_article was not syndicated"), _("Your syndication request for %(article)s was unsuccessful. Your _article is now publicly visible")],
    
    # Inter-user messages
    ["message_received",                     "e",  _("message received from another member"), _("You have received a message from %(member)s, please login to Civicboom and check your messages")],
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


def send_message(member_to, message_data, delay_commit=False):
    # If notifications not enabled return silently
    if not config['feature.notifications']:
        return
    
    worker.add_job({
        'task'        : 'send_message',
        'member'      : member_to.username,
        'message_data': message_data.to_dict(),
    })
