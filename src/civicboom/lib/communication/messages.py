"""
A collection of MessageData subclasses, which can be sent to members like so

import civicboom.lib.communication.messages as messages

m1 = Member()
m2 = Member()
m1.send_notification(messages.tipoff(member=m2, tipoff="there is a bomb"))
"""

#from pylons import config
from pylons.i18n          import lazy_ugettext as _
from webhelpers.html      import HTML

import cbutils.worker as worker


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
        from cbutils.worker import config # AllanC - HACK!!! could be worker config or pylons config - import here is bad - we need a better way of doing this
        if config['feature.notifications']: # Only generate messages if notifications enabled - required to bypass requireing the internationalisation module to be activated
            linked = {}
            for key in kwargs:
                if hasattr(kwargs[key], "__link__"):
                    linked[key] = HTML.a(unicode(kwargs[key]), href=kwargs[key].__link__())
                else:
                    linked[key] = HTML.span(unicode(kwargs[key])) # the span here is for security, it does HTML escaping
            if 'you' not in linked:
                linked['you'] = 'you'
            if 'your' not in linked:
                if linked['you'] == 'you':
                    linked['your'] = 'your'
                else:
                    linked['your'] = linked['you']+"'s"
            
            try:
                self.subject = unicode(self.subject) % linked
                self.content = unicode(self.content) % linked
            except ValueError as e:
                log.error("Error formatting message: %s: %s [%s]" % (self.subject, self.content, linked))
                raise
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
    ["followed_by",                          "ne", _("new follower"),                _("%(member)s is now following %(you)s")],
    ["followed_on_signup",                   "ne", _("new sign up via widget"),      _("%(member)s has signed up via your widget and is now following %(you)s")],
    ["follow_stop",                          "",   _("lost a follower"),             _("%(member)s has stopped following %(you)s")],
    
    # GregM: Follow action notifications
    ["follower_trusted",                     "ne", _("trusted follower"),             _("%(member)s has made %(you)s a trusted follower, you can now see their private content")],
    ["follower_distrusted",                  "ne", _("no longer a trusted follower"), _("%(member)s has stopped %(you)s being a trusted follower, %(you)s will not be able to see their private content")],
    ["follow_invite_trusted",                "ne", _("trusted follower invite"),      _("%(member)s has invited %(you)s to follow them as a trusted follower, if you accept you will be able see their private content")],

    # New Content
    ["article_published_by_followed",        "ne", _("new _article"),                _("%(creator)s has written new _article : %(article)s")],
    #["article_published_by_followed_mobile", "ne", _("new mobile _article"),         _("%(member)s has uploaded mobile _article : %(article)s")],
    
    # Content Actions
    ["article_rated",                        "",   _("_article rated"),              _("%(your)s _article %(article)s was rated a %(rating)s")],
    ["comment",                              "n",  _("comment made on _article"),    _("%(member)s commented on %(you)s _article %(content)s")],  #TODO Also passes comment.contents as a string and could be used here

    # Content Responses
    # AllanC- we don't distingusih mobile responses anymore #["assignment_response_mobile",           "ne", _("_assignment mobile response"), _("%(member)s has uploaded mobile _article titled %(article)s based on your _assignment %(assignment)s")],
    ["new_response",                         "ne", _("new response"),                _("%(member)s has published a response to %(your)s content %(parent)s called %(content)s ")],
    
    # Assignment Actions
    ["assignment_created",                   "ne", _("new _assignment"),             _("%(creator)s created a new _assignment %(assignment)s")],
    ["assignment_updated",                   "ne", _("_assignment updated"),         _("%(creator)s has updated their _assignment %(assignment)s")],
    ["assignment_canceled",                  "ne", _("_assignment you previously accepted has been cancelled"), _("%(member)s cancelled the _assignment %(assignment)s")],
    ["assignment_accepted",                  "ne", _("_assignment accepted"),        _("%(member)s accepted %(your)s _assignment %(assignment)s")],
    ["assignment_interest_withdrawn",        "n", _("_assignment interest withdrawn"), _("%(member)s withdrew their interest in %(your)s _assignment %(assignment)s")],
    ["assignment_invite",                    "ne", _("closed _assignment invitation") , _("%(member)s has invited %(you)s to participate in the _assignment %(assignment)s")],

    # Assignment Timed Tasks
    ["assignment_due_7days",                 "ne", _("_assignment alert: due next week"),   _("The _assignment %(you)s accepted %(assignment)s is due next week")],
    ["assignment_due_1day",                  "ne", _("_assignment alert: due tomorrow"),    _("The _assignment %(you)s accepted %(assignment)s is due tomorrow")],

    # Response Actions
    # NOTE: Don't set these to default email because these action create emails themselfs - AllanC
    ["article_disassociated_from_assignment","n",  _("_article disassociated from _assignment"), _("%(member)s disassociated %(your)s _article %(article)s from the _assignment %(assignment)s")],
    ["article_approved",                     "n",  _("_article approved by organisation"), _("%(member)s has approved %(your)s _article %(content)s in the response to their _assignment %(parent)s. Check your email for more details")],
      # TODO: response seen

    # Groups to group
    ["group_new_member",                     "ne" , _("_member joined group"),        _("%(member)s has joined %(group)s")],
    ["group_role_changed",                   "ne" , _("_member role changed"),        _("%(admin)s changed %(member)s's role for %(group)s to %(role)s")],
    ["group_remove_member_to_group",         "ne", _("_member removed from _group"), _("%(admin)s removed %(member)s from %(group)s")],
    ["group_join_request",                   "ne" , _("join request"),                _("%(member)s has requested to join %(group)s")],
    
    # Groups to members
    ["group_deleted",                        "ne", _("_group deleted"),              _("The _group %(group)s has been deleted by %(admin)s")],
    ["group_invite",                         "ne", _("_group invitation"),           _("Congratulations! You have been invited to %(group)s with the role %(role)s by %(admin)s")],
    ["group_request_declined",               "n" , _("_group membership request declined"), _("%(your)s membership request to join %(group)s was declined")],
    ["group_invitation_declined",            ""  , _("_group membership invitation declined"), _("%(member)s declined the invitation to join %(group)s")],
    ["group_request_accepted",               "ne" , _("_group request accepted"),     _("%(admin)s accepted %(your)s _group membership request. You are now a member of %(group)s")],
    ["group_remove_member_to_member",        "n", _("removed from _group"),         _("%(admin)s removed %(your)s membership to %(group)s")],
    
    # Aggregation
    #["boom_article",                         "ne", _("_article boomed"),               _("%(member)s thinks %(you)s might find this _article interesting %(article)s")],
    #["boom_assignment",                      "ne", _("_assignment boomed"),            _("%(member)s thinks %(you)s might want to add your opinion to this _assignment %(assignment)s")],
    ["boom_article",                         "ne", _("interesting _article"),               _("%(member)s wants to share %(article)s with you")],
    ["boom_assignment",                      "ne", _("get involved with this _assignment"), _("%(member)s wants you to get involved with %(assignment)s")],

    # Syndication
    #["syndicate_accept",                     "n",  _("_article was syndicated"),     _("%(member)s has accepted %(your)s syndication request for _article %(article)s. Check your email for the details")],
    #["syndicate_decline",                    "ne", _("_article was declined syndication"), _("%(member)s declined %(your)s syndication request for _article %(article)s. %(your)s _article is now publicly visible")],
    #["syndicate_expire",                     "ne", _("_article was not syndicated"), _("Your syndication request for %(article)s was unsuccessful. Your _article is now publicly visible")],
    
    # Inter-user messages
    ["message_received",                     "e",  _("message received from another member"), _("%(you)s has received a message from %(member)s, '$(message)s'. Respond ")],
]

#
# Turn the table into classes
#
for _name, _default_route, _subject, _content in generators:
    # a blank line because pep8 says so

    class gen(MessageData):
        name          = _name
        default_route = _default_route
        subject       = _subject
        content       = _content
    globals()[_name] = gen




def send_notification(members, message):
    """
    """
    from cbutils.worker import config # AllanC - HACK!!! could be worker config or pylons config - import here is bad - we need a better way of doing this
    
    # If notifications not enabled return silently
    if not config['feature.notifications']:
        return
    
    # Normalize list of usernames
    if isinstance(members, basestring):
        members = members.split(',') # split member names if comma separated list
    if not isinstance(members, list): 
        members = [members] # Put single member in list, (it could be a member object)
    members = [m.id if hasattr(m,'id') else m for m in members] # Convert member objects into username strings
    
    # Get message as dict (shallow copy defensivly if nessisary)
    if isinstance(message, dict):
        message = message.copy()
    if hasattr(message, 'to_dict'):
        message = message.to_dict()
    
    # Thread the send operation
    # Each member object is retreved and there message preferences observed (by the message thread) for each type of message
    worker.add_job({
        'task'            : 'send_notification' ,
        'members'         : members ,
        'message'         : message ,
        #'rendered_message': rendered_message ,
        #'default_route'   : message.get('default_route') ,
        #'name'            : message.get('name') ,
    })
