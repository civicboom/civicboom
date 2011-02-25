from civicboom.lib.base import *
from civicboom.lib.database.get_cached import get_message
from civicboom.model import Message
import json

from civicboom.lib.misc import str_to_int

from sqlalchemy.orm       import join, joinedload
from sqlalchemy           import or_, and_, null

from civicboom.lib.form_validators.base import DefaultSchema, MemberValidator
import formencode

log = logging.getLogger(__name__)
user_log = logging.getLogger("user")




#-------------------------------------------------------------------------------
# Form Schema
#-------------------------------------------------------------------------------

class NewMessageSchema(DefaultSchema):
    #source                     = MemberValidator()
    target                     = MemberValidator()
    subject                    = formencode.validators.String(not_empty=False, max=255)
    content                    = formencode.validators.String(not_empty=False)

#-------------------------------------------------------------------------------
# Global Functions
#-------------------------------------------------------------------------------

def _get_message(message, is_target=False, is_target_or_source=False):
    message = get_message(message)
    if not message:
        raise action_error(_("Message does not exist"), code=404)
    if is_target and message.target != c.logged_in_persona:
        raise action_error(_("You are not the target of this message"), code=403)
    if is_target_or_source and c.logged_in_persona and not (message.target==c.logged_in_persona or message.source==c.logged_in_persona):
        raise action_error(_("You are not the target or source of this message"), code=403)
    return message

#-------------------------------------------------------------------------------
# Search Filters
#-------------------------------------------------------------------------------

list_filters = {
    'all'         : lambda results: results.filter(or_( Message.source_id==c.logged_in_persona.id , Message.target_id==c.logged_in_persona.id     )) ,
    'to'          : lambda results: results.filter(and_(Message.source_id!=null()                 , Message.target_id==c.logged_in_persona.id     )) ,
    'sent'        : lambda results: results.filter(and_(Message.source_id==c.logged_in_persona.id , Message.target_id!=null()                     )) ,
    'public'      : lambda results: results.filter(and_(Message.source_id==c.logged_in_persona.id , Message.target_id==null()                     )) ,
    'notification': lambda results: results.filter(and_(Message.source_id==null()                 , Message.target_id==c.logged_in_persona.id     )) ,
}



#-------------------------------------------------------------------------------
# Message Controler
#-------------------------------------------------------------------------------

class MessagesController(BaseController):
    """
    @doc messages
    @title Messages
    @desc REST Controller styled on the Atom Publishing Protocol
    """

    @web
    @authorize
    def index(self, **kwargs):
        """
        GET /messages: Get messages related to the user
        
        @api messages 1.0 (WIP)
        
        @param * (see common list return controls)
        @param list  which list to get
               all           all messages the user can see, PMs and notifications
               to            ?
               from          ?
               public        ?
               notification  ?

        @return 200   a list of messages
                list  the list

        @comment Shish   do we want people to see their sent messages? Messages
                         will disappear from this list as the target deletes them,
                         the target may not want their activity known
        @comment Shish   using a list of functions makes it impossible to check
                         that all paths are tested - we can only tell that the
                         lookup table has been referenced at least once :/
        """
        # url('messages')
        
        # Setup search criteria
        if 'list' not in kwargs:
            kwargs['list'] = 'all'
        kwargs['limit']  = str_to_int(kwargs.get('limit'), config['search.default.limit.messages'])
        kwargs['offset'] = str_to_int(kwargs.get('offset')                                        )
        if 'include_fields' not in kwargs:
            kwargs['include_fields'] = ""
            if kwargs.get('list') in ['to']:
                kwargs['include_fields'] = "source, source_name"
            if kwargs.get('list') in ['sent']:
                kwargs['include_fields'] = "target, target_name"
        if 'exclude_fields' not in kwargs:
            kwargs['exclude_fields'] = ""
            #if kwargs.get('list')=='to':
            #    kwargs['exclude_fields'] = "content"
            if kwargs.get('list') in ['sent']:
                kwargs['exclude_fields'] = "read"
        
        results = Session.query(Message)
        
        # Eager loading of linked fields
        #  this could be generifyed and use in members/index and contents/index
        #  the code is simple, but repreative and could be condenced in a sensible way
        if 'source' in kwargs['include_fields']:
            results = results.options(joinedload('source'))
        if 'target' in kwargs['include_fields']:
            results = results.options(joinedload('target'))
        
        
        if 'list' in kwargs:
            if kwargs['list'] in list_filters:
                results = list_filters[kwargs['list']](results)
            else:
                raise action_error(_('list %s not supported') % kwargs['list'], code=400)
                
        # Sort        
        results = results.order_by(Message.timestamp.desc())
        
        # Count
        count = results.count()
        
        # Limit & Offset
        results = results.limit(kwargs['limit']).offset(kwargs['offset']) # Apply limit and offset (must be done at end)
        
        # Return search results
        return action_ok(
            data = {'list': {
                'items' : [message.to_dict(**kwargs) for message in results.all()] ,
                'count' : count ,
                'limit' : kwargs['limit'] ,
                'offset': kwargs['offset'] ,
                'type'  : 'message' ,
                }
            }
        )

    @web
    @auth
    def create(self, target=None, subject=None, content=None, **kwargs):
        """
        POST /messages: Create a new item.
        
        @api messages 1.0 (WIP)
        
        @param target   the username of the target user
        @param subject  message subject
        @param content  message body
        
        @return 201   message sent
                id    the ID of the created message
        @return 400   missing required field
        @return 404   target user doesn't exist
        
        @comment Shish  do we want some sort of "too many messages, stop spamming" response?
        @comment Shish  do we want to support multiple names in the 'target' box?
        """
        # url('messages')
        
        if not (target and subject and content):
            raise action_error('missing / incorrect paramaters', code=400)
        target = get_member(target)
        if not target:
            raise action_error('user does not exist', code=404)
        
        m = Message()
        m.source  = c.logged_in_persona
        m.target  = target
        m.subject = subject
        m.content = content
        Session.add(m)
        Session.commit()
        
        user_log.debug("Sending message to User #%d (%s)" % (target.id, target.username))
        
        return action_ok(_("Message sent"), code=201, data={'id': m.id})



    @web
    def new(self, **kwargs):
        """
        GET /messages/new: Form to create a new item.
        """
        # url('new_message')
        return action_ok()


    @web
    def update(self, id, **kwargs):
        """PUT /messsages/id: Update an existing item."""
        # url('message', id=ID)
        raise action_error(_("Messages cannot be edited"), code=501)


    @web
    @auth
    def delete(self, id, **kwargs):
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
        user_log.info("Deleted Message #%d" % (message.id, ))
        message.delete()
        
        return action_ok(_("Message deleted"))


    @web
    @authorize
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
        
        #c.viewing_user = c.logged_in_persona - swiching persona will mean that logged_in_user is group
        
        message = _get_message(id, is_target_or_source=True)
        if not message.read and message.target_id==c.logged_in_persona.id:
            message.read = True
            Session.commit()
        
        kwargs['list_type']='full'
        return action_ok(data={'message': message.to_dict(**kwargs)})


    @web
    def edit(self, id, **kwargs):
        """GET /messages/id/edit: Form to edit an existing item."""
        # url('edit_message', id=ID)
        raise action_error(_("Messages cannot be edited"), code=501)
