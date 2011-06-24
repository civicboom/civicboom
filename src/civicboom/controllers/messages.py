from civicboom.lib.base import *
import civicboom.lib.communication.messages as messages
from civicboom.model import Message

from sqlalchemy.orm       import joinedload
from sqlalchemy           import or_, and_, null

import civicboom.lib.form_validators.base
from civicboom.lib.form_validators.dict_overlay import validate_dict

log = logging.getLogger(__name__)


#-------------------------------------------------------------------------------
# Form Schema
#-------------------------------------------------------------------------------

class NewMessageSchema(civicboom.lib.form_validators.base.DefaultSchema):
    filter_extra_fields = False
    #source                     = MemberValidator()
    #target                     = MemberValidator()
    #subject                    = formencode.validators.String(not_empty=False, max=255)
    #content                    = formencode.validators.String(not_empty=False)
    subject = civicboom.lib.form_validators.base.UnicodeStripHTMLValidator(not_empty=True, max=255) 
    content = civicboom.lib.form_validators.base.ContentUnicodeValidator(not_empty=True)

new_message_schema = NewMessageSchema()

#-------------------------------------------------------------------------------
# Global Functions
#-------------------------------------------------------------------------------


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
        
        return to_apilist(results, obj_type='message', **kwargs)


    @web
    @auth
    def create(self, **kwargs):
        """
        POST /messages: Create a new item.
        
        @api messages 1.0 (WIP)
        
        @param target   the username of the target user (can be comma separated list)
        @param subject  message subject
        @param content  message body
        
        @return 201   message sent
                id    list of message id's created
        @return 400   
        @return invalid missing required field
        
        @comment Shish  do we want some sort of "too many messages, stop spamming" response?
        @comment AllanC yes we do, to be implemented - raised on Redmine #474
        """
        # url('messages')
        
        # Validation needs to be overlayed oved a data dictonary, so we wrap kwargs in the data dic - will raise invalid if needed
        data       = {'message':kwargs}
        data       = validate_dict(data, new_message_schema, dict_to_validate_key='message', template_error='messages/new')
        kwargs     = data['message']
        
        #member_to = get_member(kwargs.get('target'), set_html_action_fallback=True)
        
        messages_sent = []
        
        # Construct special message (rather than using a prefab from messages.'message_name')
        message = dict(
            name          = 'message'            ,
            default_route = 'e'                  ,
            source        = c.logged_in_persona.username ,
            target        = kwargs.get('target') ,
            subject       = kwargs.get('subject'),
            content       = kwargs.get('content'),
        )
        
        members = get_members(kwargs.get('target'), expand_group_members=False)
        for member in members:
            m = Message()
            m.target  = member
            m.source  = c.logged_in_persona
            m.subject = message['subject']
            m.content = message['content']
            Session.add(m)
            messages_sent.append(m)
        
        Session.commit()
        
        # Alert via email, MSN, etc - NOTE the message route for message_recived does not generate a notification by default
        messages.send_notification(members, message)
        #send_notification(messages.message_received(member=m.source, message=m, you=m.target))
        
        #user_log.debug("Sending message to User #%d (%s)" % (target.id, target.username))
        user_log.debug("Sent message to %s" % kwargs.get('target'))
        
        if not messages_sent:
            raise action_error(_("Message failed to send"), code=400)
        
        return action_ok(_("Message sent"), code=201, data={'id': [m.id for m in messages_sent]}) #data={'id': m.id}


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
        
        message = get_message(id, is_target=True)
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
        message = get_message(id, is_target_or_source=True)
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
