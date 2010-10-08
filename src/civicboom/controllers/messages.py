
from civicboom.lib.base import *
from civicboom.model import Message
import json

log = logging.getLogger(__name__)
user_log = logging.getLogger("user")


index_lists = {
    'to'          : lambda member: member.messages_to ,
    'from'        : lambda member: member.messages_from ,
    'public'      : lambda member: member.messages_public ,    
    'notification': lambda member: member.messages_notification ,
}


class MessagesController(BaseController):
    """
    @doc messages
    @title Messages
    @desc REST Controller styled on the Atom Publishing Protocol
    """
    # To properly map this controller, ensure your config/routing.py file has
    # a resource setup:
    #     map.resource('message', 'messages')


    @auto_format_output()
    @web_params_to_kwargs()
    @authorize(is_valid_user)
    def index(self, list='to', **kwargs):
        """
        GET /messages: All items in the collection.
        
        @api messages 1.0 (Draft)
        
        @param list  which list to get
               to            ?
               from          ?
               public        ?
               notification  ?

        @return 200   a list of messages
                list  the list
        """
        # url('messages')
        # AllanC - this feels duplicated from the member controler - humm ... need to think about a sensible stucture
        c.viewing_user = c.logged_in_user
        
        if list not in index_lists: raise action_error(_('list type %s not supported') % list)
        messages = index_lists[list](c.logged_in_user)
        messages = [message.to_dict() for message in messages]
        
        return action_ok(data={'list': messages})


    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def create(self):
        """
        POST /messages: Create a new item.
        
        @api messages 1.0 (Draft)
        
        @param target
        @param subject
        @param content

        @return 201   message sent
        @return 400   missing required field
        @return 404   target user doesn't exist
        """
        # url('messages')
        try:
            target = get_user(request.POST["target"])
            if not target:
                # FIXME: form validator to refresh with the same values?
                raise action_error(_("Can't find user '%s'") % request.POST["target"], code=404)
            m = Message()
            m.source_id = c.logged_in_user.id # FIXME: or from any group they are admin of?
            m.target_id = target.id
            m.subject = request.POST["subject"]
            m.content = request.POST["content"]
            # FIXME: send a notification too?
            user_log.debug("Sending message to User #%d (%s)" % (target.id, target.username))
            Session.add(m)
            Session.commit()
            return action_ok(_("Message sent"), code=201)
        except action_error as ae:
            raise
        except Exception, e:
            log.exception("Error sending message:")
            raise action_error(_("Error sending message"), code=400)


    @auto_format_output()
    def new(self, format='html'):
        """
        GET /messages/new: Form to create a new item.
        """
        # url('new_message')
        raise action_error(_("'New Message' page not implemented - go to somebody's profile page to message them"), code=501)


    @auto_format_output()
    def update(self, id):
        """PUT /messsages/id: Update an existing item."""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(h.url('message', id=ID), method='put')
        # url('message', id=ID)
        raise action_error(_("Messages cannot be edited"), code=501)


    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def delete(self, id):
        """
        DELETE /messages/{id}: Delete an existing item.

        @api messages 1.0 (Draft)

        @return 200  deleted
        @return 404  message belongs to somebody else
        @return 404  message does not exist
        """
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(h.url('message', id=ID), method='delete')
        # url('message', id=ID)
        c.viewing_user = c.logged_in_user
        msg = Session.query(Message).filter(Message.id==int(id)).first()
        if not msg:
            raise action_error(_("Message does not exist"), code=404)

        redir = None
        if msg.target == c.viewing_user: # FIXME messages to groups?
            # FIXME: test that delete-orphan works, and removes the
            # de-parented message
            if msg.source: # source exists = message, no source = notification
                user_log.debug("Deleting message")
                c.viewing_user.messages_to.remove(msg)
            else:
                user_log.debug("Deleting notification")
                c.viewing_user.messages_notification.remove(msg)
            Session.commit()
            return action_ok(_("Message deleted"))
        else:
            user_log.warning("User tried to delete somebody else's message") # FIXME: details
            raise action_error(_("You are not the target of this message"), code=403)


    @auto_format_output()
    @authorize(is_valid_user)
    def show(self, id, format='html'):
        """
        GET /messages/{id}: Show a specific item.

        @api messages 1.0 (Draft)

        @return  200       show the message
                 id        message id
                 source    username (None if system notification)
                 subject   ?
                 timestamp ?
                 content   ?
        """
        # url('message', id=ID)
        c.viewing_user = c.logged_in_user

        msg = Session.query(Message).filter(Message.id==id).first()
        if not msg:
            raise action_error(_("Message does not exist"), code=404)

        if msg.target == c.viewing_user: # FIXME messages to groups?
            c.msg = msg
        else:
            raise action_error(_("You are not the target of this message"), code=403)

        return action_ok(
            template = 'messages/show',
            data = {
                "id": c.msg.id,
                "source": str(c.msg.source),
                "subject": c.msg.subject,
                "timestamp": str(c.msg.timestamp),
                "content": c.msg.content,
            }
        )


    @auto_format_output()
    def edit(self, id, format='html'):
        """GET /messages/id/edit: Form to edit an existing item."""
        # url('edit_message', id=ID)
        raise action_error(_("Messages cannot be edited"), code=501)
