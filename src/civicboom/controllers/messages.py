from civicboom.lib.base import *
import civicboom.lib.communication.messages as messages
from civicboom.model import Message

from civicboom.lib.cache import _cache, get_cache_key, normalize_kwargs_for_cache

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
    subject = civicboom.lib.form_validators.base.UnicodeStripHTMLValidator(not_empty=False, max=255)
    content = civicboom.lib.form_validators.base.CleanHTMLValidator(not_empty=True)

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

def message_dict_insert_type(message):
    if message['source_id']==c.logged_in_persona.id and message['target_id']                        :
        message['type'] = 'sent'
    if message['source_id']                         and message['target_id']==c.logged_in_persona.id:
        message['type'] = 'to'
    if message['source_id']==None                   and message['target_id']==c.logged_in_persona.id:
        message['type'] = 'notification'
    if message['source_id']==c.logged_in_persona.id and message['target_id']==None                  :
        message['type'] = 'public'


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
        @param converation_with member_id to have conversation with

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
        
        # Pre-process kwargs ---------------------------------------------------
        
        kwargs['_logged_in_persona'] = c.logged_in_persona.id
        
        # Setup search criteria
        if 'list' not in kwargs and 'conversation_with' not in kwargs:
            kwargs['list'] = 'all'
        if 'include_fields' not in kwargs:
            kwargs['include_fields'] = ""
            if kwargs.get('list') in ['to']:
                kwargs['include_fields'] = "source, source_name"
            if kwargs.get('list') in ['sent']:
                kwargs['include_fields'] = "target, target_name"
        if 'sort' not in kwargs:
            kwargs['sort'] = '-timestamp'
        if 'conversation_with' in kwargs and 'limit' not in kwargs:
            #kwargs['limit'] = 5
            kwargs['include_fields'] += "source"
        
        # Create Cache key based on kwargs -------------------------------------
        
        cache_key = get_cache_key('messages_index', kwargs)
        cache_key = None # AllanC - temp addition to ensure no messages lists are cached until they are tested properly
        
        # Construct Query with provided kwargs ---------------------------------
        # Everything past here can be cached based on the kwargs state
        
        def messages_index(**kwargs):
            results = Session.query(Message)
            # Eager loading of linked fields
            #  this could be generifyed and use in members/index and contents/index
            #  the code is simple, but repreative and could be condenced in a sensible way
            if 'source' in kwargs['include_fields']:
                results = results.options(joinedload('source'))
            if 'target' in kwargs['include_fields']:
                results = results.options(joinedload('target'))
            if 'conversation_with' in kwargs:
                results = results.filter(
                    or_(
                        and_(Message.source_id==c.logged_in_persona.id    , Message.target_id==kwargs['conversation_with']) ,
                        and_(Message.source_id==kwargs['conversation_with'], Message.target_id==c.logged_in_persona.id    ) ,
                    )
                )
            elif 'list' in kwargs:
                if kwargs['list'] in list_filters:
                    results = list_filters[kwargs['list']](results)
                else:
                    raise action_error(_('list %s not supported') % kwargs['list'], code=400)
                    
            # Sort
            # AllanC - botched, this is not implmented properly
            if kwargs['sort'] == '-timestamp':
                results = results.order_by(Message.timestamp.desc())
            elif kwargs['sort'] == 'timestamp':
                results = results.order_by(Message.timestamp.asc())
            
            apilist = to_apilist(results, obj_type='messages', **kwargs)
            
            # Post processing of list
            # AllanC - the model is not aware of the currently logged in user
            #          we are performing logic to identify what each message is
            #          we cant have this as a object method because it's already turned into a dict by this point.
            for message in apilist['data']['list']['items']:
                message_dict_insert_type(message)
            
            return apilist
            
        cache      = _cache.get('messages_index')
        cache_func = lambda: messages_index(**kwargs)
        if cache and cache_key:
            return cache.get(key=cache_key, createfunc=cache_func)
        return cache_func()


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
        #messages.send_notification(members, message)
        # AllanC - DANG!! cant do a batch one here ... while this is efficent, we cant get the id of the message to the email - this is needed to allow replys to the message
        #          not really send_notification ... but this is used to trigger the 'email' route for the message
        for message in messages_sent:
            messages.send_notification(message.target, message)
        
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
        c.html_action_fallback_url = url('messages', list=message.__type__(c.logged_in_persona)) # AllanC - if the message is fetuched successfuly then the fallback needs to be overriden as the profile, because on success the mssage will not exisit anymore
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
        message_dict = message.to_dict(**kwargs)
        message_dict_insert_type(message_dict)
        
        return action_ok(data={'message': message_dict})


    @web
    def edit(self, id, **kwargs):
        """GET /messages/id/edit: Form to edit an existing item."""
        # url('edit_message', id=ID)
        raise action_error(_("Messages cannot be edited"), code=501)
