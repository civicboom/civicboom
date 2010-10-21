from civicboom.lib.base import *
from civicboom.lib.database.get_cached import get_message
from civicboom.model import Message
import json

log = logging.getLogger(__name__)
user_log = logging.getLogger("user")


#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------

index_lists = {
    'to'          : lambda member: member.messages_to ,
    'from'        : lambda member: member.messages_from ,
    'public'      : lambda member: member.messages_public ,    
    'notification': lambda member: member.messages_notification ,
}

#-------------------------------------------------------------------------------
# Global Functions
#-------------------------------------------------------------------------------

def _get_message(message, is_target=False):
    message = get_message(message)
    if not message:
        raise action_error(_("Message does not exist"), code=404)
    if is_target and message.target != c.logged_in_user:
        raise action_error(_("You are not the target of this message"), code=403)
    return message


#-------------------------------------------------------------------------------
# Message Controler
#-------------------------------------------------------------------------------

class MessagesController(BaseController):
    """
    @doc messages
    @title Messages
    @desc REST Controller styled on the Atom Publishing Protocol
    """

    @auto_format_output()
    @web_params_to_kwargs()
    @authorize(is_valid_user)
    def index(self, **kwargs):
        """
        GET /messages: All items in the collection.
        
        @api messages 1.0 (WIP)
        
        @param * (see common list return controls)
        @param list  which list to get
               to            ?
               from          ?
               public        ?
               notification  ?

        @return 200   a list of messages
                list  the list

        @comment Shish   do we want people to see their sent messages? Messages
                         will disappear from this list as the target deletes them,
                         the target may not want their activity known
        @comment Shish   are public messages used yet? if they aren't used, IMHO
                         they should be left undocumented
        @comment Shish   using a list of functions makes it impossible to check
                         that all paths are tested - we can only tell that the
                         lookup table has been referenced at least once :/
        """
        # url('messages')
        
        if 'list' not in kwargs:
            kwargs['list'] = 'to'
        list = kwargs['list']
        
        if list not in index_lists:
            raise action_error(_('list %s not supported') % list, code=400)
        
        messages = index_lists[list](c.logged_in_user)
        messages = [message.to_dict(**kwargs) for message in messages]
        
        return action_ok(data={'list': messages})


    @auto_format_output()
    @web_params_to_kwargs()
    @authorize(is_valid_user)
    @authenticate_form
    def create(self, **kwargs):
        """
        POST /messages: Create a new item.
        
        @api messages 1.0 (WIP)
        
        @param target   the username of the target user
        @param subject  message subject
        @param content  message body
        
        @return 201   message sent
        @return 400   missing required field
        @return 404   target user doesn't exist
        
        @comment Shish  do we want some sort of "too many messages, stop spamming" response?
        @comment Shish  do we want to support multiple names in the 'target' box?
        """
        # url('messages')
        
        # FIXME: form validator to refresh with the same values?
        if not set(["target", "subject", "content"]).issubset(request.POST.keys()):
            raise action_error(_("Missing inputs"), code=400)
        target = get_member(request.POST["target"])
        if not target:
            raise action_error(_("Can't find user '%s'") % request.POST["target"], code=404)
        
        m = Message()
        m.source_id = c.logged_in_user.id # FIXME: or from any group they are admin of?
        m.target_id = target.id
        m.subject = request.POST["subject"]
        m.content = request.POST["content"]
        user_log.debug("Sending message to User #%d (%s)" % (target.id, target.username))
        Session.add(m)
        Session.commit()
        return action_ok(_("Message sent"), code=201)



    @auto_format_output()
    def new(self, format='html'):
        """
        GET /messages/new: Form to create a new item.
        """
        # url('new_message')
        return action_ok()


    @auto_format_output()
    def update(self, id):
        """PUT /messsages/id: Update an existing item."""
        # url('message', id=ID)
        raise action_error(_("Messages cannot be edited"), code=501)


    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def delete(self, id):
        """
        DELETE /messages/{id}: Delete an existing item.

        @api messages 1.0 (WIP)

        @return 200  deleted
        @return 403  message belongs to somebody else
        @return 404  message does not exist
        """
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(h.url('message', id=ID), method='delete')
        # url('message', id=ID)
        
        message = _get_message(id, is_target=True) 
        message.delete()
        
        return action_ok(_("Message deleted"))


    @auto_format_output()
    @web_params_to_kwargs()
    @authorize(is_valid_user)
    def show(self, id, **kwargs):
        """
        GET /messages/{id}: Show a specific item.
        
        @api messages 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200       show the message
                id        message id
                source    username (None if system notification)
                timestamp time that the message was sent
                subject   message subject
                content   message body
        @return 403       current user is not the message target
        @return 404       the message does not exist

        @comment Shish  do we want to return permission denied, or
                        should we pretend the message doesn't exist
                        at all?
        """
        # url('message', id=ID)
        
        #c.viewing_user = c.logged_in_user - swiching persona will mean that logged_in_user is group
        
        message = _get_message(id, is_target=True)
        return action_ok(data=message.to_dict(**kwargs))


    @auto_format_output()
    def edit(self, id):
        """GET /messages/id/edit: Form to edit an existing item."""
        # url('edit_message', id=ID)
        raise action_error(_("Messages cannot be edited"), code=501)
