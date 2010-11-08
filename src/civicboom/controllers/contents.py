"""
Content Controller

For managing content:
 - creating/editing
 - attaching media
 - deleting
 - flagging
 - AJAX calls to get media processing status
"""
# Base controller imports
from civicboom.lib.base import *

# Datamodel and database session imports
from civicboom.model                   import Media, CommentContent, DraftContent
from civicboom.lib.database.get_cached import get_content, update_content, get_licenses

from civicboom.model.content import _content_type as content_types

# Other imports
from civicboom.lib.civicboom_lib import form_post_contains_content, form_to_content, get_content_media_upload_key, profanity_filter, twitter_global
from civicboom.lib.communication import messages
from civicboom.lib.helpers       import call_action

# Validation
import formencode
import civicboom.lib.form_validators
#from civicboom.lib.form_validators.dict_overlay import validate_dict

# Search imports
from civicboom.lib.search import *
from civicboom.lib.database.gis import get_engine
from civicboom.model      import Content, Member
from sqlalchemy           import or_, and_
from sqlalchemy.orm       import join


# Logging setup
log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


#-------------------------------------------------------------------------------
# Form Schema
#-------------------------------------------------------------------------------

class ContentSchema(civicboom.lib.form_validators.base.DefaultSchema):
    type        = formencode.validators.OneOf(content_types.enums, not_empty=False)
    title       = formencode.validators.String(not_empty=False, strip=True, max=250, min=2)
    content     = civicboom.lib.form_validators.base.ContentUnicodeValidator()
    parent      = civicboom.lib.form_validators.base.ContentObjectValidator(not_empty=False)
    location    = civicboom.lib.form_validators.base.LocationValidator(not_empty=False)
    private     = formencode.validators.StringBool(not_empty=False, max=250, min=2)
    license     = civicboom.lib.form_validators.base.LicenceValidator(not_empty=False)
    creator     = civicboom.lib.form_validators.base.ContentMemberValidator(not_empty=False) # AllanC - debatable if this is needed, do we want to give users the power to give content away? Could this be abused?
    tags        = civicboom.lib.form_validators.base.ContentTagsValidator(not_empty=False)
    # Draft Fields
    target_type = formencode.validators.OneOf(content_types.enums, not_empty=False)
    # Assignment Fields
    due_date    = formencode.validators.DateConverter(month_style='dd/mm/yyyy')
    event_date  = formencode.validators.DateConverter(month_style='dd/mm/yyyy')


class ContentCommentSchema(ContentSchema):
    parent      = civicboom.lib.form_validators.base.ContentObjectValidator(not_empty=True, empty=_('comments must have a valid parent'))
    content     = civicboom.lib.form_validators.base.ContentUnicodeValidator(empty=_('comments must have content'))

    


#-------------------------------------------------------------------------------
# Global Functions
#-------------------------------------------------------------------------------

def _get_content(id, is_editable=False, is_viewable=False, is_parent_owner=False):
    """
    Shortcut to return content and raise not found or permission exceptions automatically (as these are common opertations every time a content is fetched)
    """
    content = get_content(id)
    if not content:
        raise action_error(_("content not found"), code=404)
    if is_viewable:
        if not content.viewable_by(c.logged_in_persona): 
            raise action_error(_("_content not viewable"), code=403)
        if content.__type__ == "comment":
            user_log.debug("Attempted to view a comment as an article")
            raise action_error(_("_content not found"), code=404)
    if is_editable and not content.editable_by(c.logged_in_persona):
        raise action_error(_("You do not have permission to edit this _content"), code=403)
    if is_parent_owner and not content.is_parent_owner(c.logged_in_persona):
        raise action_error(_("not parent owner"), code=403)
    return content


#-------------------------------------------------------------------------------
# Search Filters
#-------------------------------------------------------------------------------
def _get_search_filters():
    def append_search_text(query, text):
        return query.filter(or_(Content.title.match(text), Content.content.match(text)))
    
    def append_search_location(query, location_text):
        parts = location_text.split(",")
        (lon, lat, radius) = (None, None, None)
        if len(parts) == 2:
            (lon, lat) = parts
            radius = 10
        elif len(parts) == 3:
            (lon, lat, radius) = parts
        zoom = 10 # FIXME: inverse of radius? see bug #50
        if lon and lat and radius:
            location = (lon, lat, zoom)
            return query.filter("ST_DWithin(location, 'SRID=4326;POINT(%d %d)', %d)" % (float(lon), float(lat), float(radius)))
        else:
            return query
    
    def append_search_id(query, id):
        return query.filter(Content.id==int(id))

    def append_search_type(query, type_text):
        return query.filter(Content.__type__==type_text)
    
    def append_search_creator(query, creator_text):
        try:
            return query.filter(Content.creator_id==int(creator_text))
        except:
            return query.filter(Member.username==creator_text)
    
    def append_search_response_to(query, article_id):
        return query.filter(Content.parent_id==int(article_id))

    
    search_filters = {
        'id'         : append_search_id ,
        'creator'    : append_search_creator ,
        'query'      : append_search_text ,
        'location'   : append_search_location ,
        'type'       : append_search_type ,
        'response_to': append_search_response_to ,
    }
    
    return search_filters

search_filters = _get_search_filters()



#-------------------------------------------------------------------------------
# Content Controler
#-------------------------------------------------------------------------------

class ContentsController(BaseController):
    """
    @title Contents
    @doc contents
    @desc REST Controller styled on the Atom Publishing Protocol
    """
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('content', 'contents')

    @auto_format_output
    @web_params_to_kwargs
    @authorize(is_valid_user)
    def index(self, **kwargs):
        """
        GET /contents: All items in the collection
        @param * (see common list return controls)
        @param limit
        @param offset
        """
        # url('contents')
        
        results = Session.query(Content).select_from(join(Content, Member, Content.creator))
        results = results.filter(and_(Content.__type__!='comment', Content.visable==True, Content.private==False)) #Content.__type__!='draft'
        results = results.order_by(Content.id.desc()) # Setup base content search query - this is mirroed in the member propery content_public
        
        if 'limit' not in kwargs: #Set default limit and offset (can be overfidden by user)
            kwargs['limit'] = 20
        if 'offset' not in kwargs:
            kwargs['offset'] = 0
        if 'include_fields' not in kwargs:
            kwargs['include_fields'] = ",creator"
        if 'exclude_fields' not in kwargs:
            kwargs['exclude_fields'] = ",creator_id"
        if 'list_type' not in kwargs:
            #kwargs['list_type'] = 'default'
            if c.format == 'rss':                       # Default RSS to list_with_media
                kwargs['include_fields'] += ',attachments'
        
        for key in [key for key in search_filters.keys() if key in kwargs]: # Append filters to results query based on kwarg params
            results = search_filters[key](results, kwargs[key])
        results = results.limit(kwargs['limit']).offset(kwargs['offset']) # Apply limit and offset (must be done at end)
        
        return action_ok(
            data     = {'list': [content.to_dict(**kwargs) for content in results.all()]} ,
        ) # return dictionaty of content to be formatted


    @auto_format_output
    @web_params_to_kwargs
    @authorize(is_valid_user)
    @authenticate_form
    def create(self, **kwargs):
        """
        POST /contents: Create a new item

        @api contents 1.0 (WIP)

        @param title
        @param contents
        @param type
        @param ...

        @return 201   content created
                id    new content id
        @return 400   missing data (ie, a type=comment with no parent_id)
        @return 403   can't reply to parent
        @return 404   parent not found

        @comment Shish paramaters need filling out
        """
        # url('contents') + POST
        
        content = form_to_content(kwargs, None)
        Session.add(content)
        Session.commit()
        
        self.update(content.id, **kwargs)
        
        if c.format == 'redirect' and content.parent:
            return redirect(url('content', id=content.parent.id))
        
        return action_ok(message=_('_content created ok'), data={'id':content.id}, code=201)


    @auto_format_output
    @authorize(is_valid_user)
    @authenticate_form
    def new(self):
        """
        GET /contents/new: Form to create a new item

        As file-upload and such require an existing object to add to,
        we create a blank object and redirect to "edit-existing" mode
        """
        #url_for('new_content')
        
        # AllanC TODO - needs restructure - see create
        content_id = call_action(ContentsController().create, format='python')['data']['id']
        return redirect(url('edit_content', id=content_id))




    @auto_format_output
    @web_params_to_kwargs
    @authorize(is_valid_user)
    @authenticate_form
    def update(self, id, **kwargs):
        """
        PUT /contents/{id}: Update an existing item

        @api contents 1.0 (WIP)

        @param *  see "POST /contents"

        @return 200   success
        @return 403   lacking permission to edit
        @return 404   no content to be edited

        @comment Shish needs to check validity of parent if set
        """
        # url('content', id=ID)
        
        content = _get_content(id, is_editable=True)
        
        # Validation -----------
        #   this is the wrong place for this
        #   we need a validation structure for content
        
        # if parent is specified, make sure it is valid
        if 'parent_id' in kwargs:
            parent = get_content(kwargs['parent_id'])
            if not parent:
                raise action_error(message='parent not found', code=404)
            if not parent.viewable_by(c.logged_in_persona):
                raise action_error(message='you do not have permission to respond to this content', code=403)
        
        # if type is comment, it must have a parent
        if kwargs.get('type') == "comment" and 'parent_id' not in kwargs:
            raise action_error(_('comments must have a valid parent'), code=400)
        # ------- Validation end
        
        # AllanC - Publish Permission placeholder for groups
        #          We need to not only know the current user persona, but also the role of that current persona e.g - might be logged in as EvilCorp but only as a 'contributor' or 'observer'
        #if 'submit_publish' in request.POST and :
        #    raise action_error(_("You do not have permission to publish this _content"), code=403)
        
        
        starting_content_type = content.__type__                  # Rember the original content type to see if it has morphed
        content               = form_to_content(kwargs, content)  # Overlay form data over the current content object or return a new instance of an object
        
        def normalise_submit(kwargs):
            submit_keys = [key.replace("submit_","") for key in kwargs.keys() if key.startswith("submit_") and kwargs[key]!=None and kwargs[key]!='']
            if len(submit_keys) == 0:
                return None
            if len(submit_keys) == 1:
                return submit_keys[0]
            raise action_error(_('multiple submit types submited'), code=400)
        submit_type = normalise_submit(kwargs)

        
        # If publishing perform profanity check and send notifications
        if submit_type == 'publish':
            profanity_filter(content) # Filter any naughty words and alert moderator TODO: needs to be threaded (raised on redmine)
            
            content.private = False # TODO: all published content is currently public ... this will not be the case for all publish in future
            
            m = None
            if starting_content_type != content.__type__:
                # Send notifications about NEW published content
                if   content.__type__ == "article"   :
                    m = messages.article_published_by_followed(creator=content.creator, article   =content)
                elif content.__type__ == "assignment":
                    m = messages.assignment_created           (creator=content.creator, assignment=content)
                
                # if this is a response - notify parent content creator
                if content.parent:
                    content.parent.creator.send_message(
                        messages.new_response(member = content.creator, content = content, parent = content.parent), delay_commit=True
                    )
                
                # TODO: Clear comments when upgraded from draft to published content?
                user_log.info("published new Content #%d" % (content.id, ))
                # Aggregate new content
                content.aggregate_via_creator() # Agrigate content over creators known providers
                twitter_global(content) # TODO? diseminate new or updated content?
            else:
                # Send notifications about previously published content has been UPDATED
                if   content.__type__ == "assignment":
                    m = messages.assignment_updated           (creator=content.creator, assignment=content)
                user_log.info("updated published Content #%d" % (content.id, ))
            if m:
                content.creator.send_message_to_followers(m, delay_commit=True)
        
        # AllanC - This was an idea that if the content has not changed then dont commit it, but for now it is simpler to always commit it
        #content_hash_before = content.hash() # Generate hash of content
        #content_hash_after  = "always trigger db commit on post" #content.hash()                # Generate hash of content again
        #if content_hash_before != content_hash_after:         # If content has changed
        Session.add(content)                            #   Save content to database
        Session.commit()                                  #
        update_content(content)                         #   Invalidate any cache associated with this content
        user_log.info("edited Content #%d" % (content.id, )) # todo - move this so we dont get duplicate entrys with the publish events above 
        
        # Set redirect destination
        content_redirect = url('edit_content', id=content.id) # Default redirect back to editor to continue editing
        if submit_type == 'preview':
            content_redirect = url('content', id=content.id)
        if submit_type ==  'publish':
            content_redirect = url('content', id=content.id, prompt_aggregate=True)
        if submit_type == 'response':
            content_redirect = url('content', id=content.parent_id)
        
        if c.format == 'redirect':
            return redirect(content_redirect)
            
        return action_ok(_("_content updated"))


    @auto_format_output
    @authorize(is_valid_user)
    @authenticate_form
    def delete(self, id):
        """
        DELETE /contents/{id}: Delete an existing item

        @api contents 1.0 (WIP)

        @return 200   content deleted successfully
        @return 403   lacking permission
        @return 404   no content to delete
        """
        # url('content', id=ID)
        content = _get_content(id, is_editable=True)
        content.delete()
        return action_ok(_("_content deleted"), code=200)


    @auto_format_output
    @web_params_to_kwargs
    def show(self, id, **kwargs):
        """
        GET /content/{id}: Show a specific item
        
        @api contents 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200      page ok
                content  content object
        @return 403      permission denied
        @return 404      content not found
        """
        # url('content', id=ID)
        """
        View content
        Different content object types require a different view template
        Identify the object type and render with approriate renderer
        """
        if 'list_type' not in kwargs:
            kwargs['list_type'] = 'full+actions'
        
        content = _get_content(id, is_viewable=True)
        
        # Increase content view count
        if hasattr(content,'views'):
            content_view_key = 'content_%s' % content.id
            if session_get(content_view_key):
                session_set(content_view_key, True)
                content.views += 1
                Session.commit()
                # AllanC - invalidating the content on EVERY view does not make scence
                #        - a cron should invalidate this OR the templates should expire after X time
                #update_content(content)
            
        return action_ok(
            data = {'content':content.to_dict(**kwargs)}
        )


    @auto_format_output
    @web_params_to_kwargs
    @authorize(is_valid_user)
    def edit(self, id, **kwargs):
        """
        GET /contents/{id}/edit: Form to edit an existing item
        """
        # url('edit_content', id=ID)
        
        c.content = _get_content(id, is_editable=True)
        
        c.content                  = form_to_content(kwargs, c.content)
        c.content_media_upload_key = get_content_media_upload_key(c.content)
        
        return action_ok()

