# Base controller imports
from civicboom.lib.base import *

# Datamodel and database session imports
from civicboom.model                   import Media, CommentContent, DraftContent, CommentContent, ArticleContent, AssignmentContent
from civicboom.lib.database.get_cached import get_content, update_content, get_licenses
from civicboom.model.content           import _content_type as content_types

# Other imports
from civicboom.lib.civicboom_lib import get_content_media_upload_key, profanity_filter, twitter_global
from civicboom.lib.communication import messages
from civicboom.lib.helpers       import call_action
from civicboom.lib.database.polymorphic_helpers import morph_content_to

# Validation
import formencode
import civicboom.lib.form_validators.base
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
    allow_extra_fields  = True
    filter_extra_fields = False
    ignore_key_missing  = True
    type        = formencode.validators.OneOf(content_types.enums, not_empty=False)
    title       = formencode.validators.String(not_empty=False, strip=True, max=250, min=2)
    content     = civicboom.lib.form_validators.base.ContentUnicodeValidator()
    parent_id   = civicboom.lib.form_validators.base.ContentObjectValidator(not_empty=False)
    location    = civicboom.lib.form_validators.base.LocationValidator(not_empty=False)
    private     = formencode.validators.StringBool(not_empty=False)
    license_id  = civicboom.lib.form_validators.base.LicenseValidator(not_empty=False)
    creator_id  = civicboom.lib.form_validators.base.MemberValidator(not_empty=False) # AllanC - debatable if this is needed, do we want to give users the power to give content away? Could this be abused?
    tags        = civicboom.lib.form_validators.base.ContentTagsValidator(not_empty=False)
    # Draft Fields
    target_type = formencode.validators.OneOf(content_types.enums, not_empty=False)
    # Assignment Fields
    due_date    = formencode.validators.DateConverter(not_empty=False, month_style='dd/mm/yyyy')
    event_date  = formencode.validators.DateConverter(not_empty=False, month_style='dd/mm/yyyy')
    # TODO: need date validators to check date is in future (and not too far in future as well)


class ContentCommentSchema(ContentSchema):
    parent_id   = civicboom.lib.form_validators.base.ContentObjectValidator( not_empty=True, empty=_('comments must have a valid parent'))
    content     = civicboom.lib.form_validators.base.ContentUnicodeValidator(not_empty=True, empty=_('comments must have content'))

    


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
            #raise action_error(_("_content not found"), code=404)
            # AllanC - originaly viewing a comment was an error, we may want in the future to display comments and sub comments, for now we redirect to parent
            return redirect(url('content', id=content.parent.id))
    if is_editable and not content.editable_by(c.logged_in_persona):
        # AllanC TODO: need to check role in group to see if they can do this
        raise action_error(_("You do not have permission to edit this _content"), code=403)
    if is_parent_owner and not content.is_parent_owner(c.logged_in_persona):
        raise action_error(_("not parent owner"), code=403)
    return content

#-------------------------------------------------------------------------------
# Decorators 
#-------------------------------------------------------------------------------

#@decorator
#def can_publish(target, *args, **kwargs):
#    #c.logged_in_persona_role
#    result = target(*args, **kwargs) # Execute the wrapped function
#    return result


#-------------------------------------------------------------------------------
# Search Filters
#-------------------------------------------------------------------------------
def _init_search_filters():
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

search_filters = _init_search_filters()



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
    def create(self, type='draft', **kwargs):
        """
        POST /contents: Create a new item

        @api contents 1.0 (WIP)

        @param type
        @param *  see "PUT /contents/id"

        @return 201   content created
                id    new content id
        @return x     see update return types
        """
        # url('contents') + POST
        
        # Create Content Object
        if   type == 'draft':
            content = DraftContent()
        elif type == "comment":
            content = CommentContent()
        elif type == "article":
            content = ArticleContent()
        elif type == "assignment":
            content = AssignmentContent()
        
        # Set create to currently logged in user
        content.creator = c.logged_in_persona
        
        # Commit to database to get ID field
        # DEPRICATED
        #Session.add(content)
        #Session.commit()
        # AllanC - if the update fails on validation we do not want a ghost record commited
        
        # Use update behaviour to save and commit object
        self.update(content, **kwargs)
        
        return action_ok(message=_('_content created ok'), data={'id':content.id}, code=201)


    @auto_format_output
    @web_params_to_kwargs
    @authorize(is_valid_user)
    @authenticate_form
    def update(self, id, **kwargs):
        """
        PUT /contents/{id}: Update an existing item

        @api contents 1.0 (WIP)

        @return 200   success
        @return 403   lacking permission to edit
        @return 404   no content to be edited

        @comment Shish paramaters need filling out
        """
        # url('content', id=ID)
        
        # -- Get Content -------------------------------------------------------
        if isinstance(id, Content):
            content = id
        else:
            content = _get_content(id, is_editable=True)
        assert content
        
        # -- Publish Permission-------------------------------------------------
        # TODO - need to check role in group to see if they have permissions to do this
        # TODO - Publish Permission for groups (to be part of is editable?)
        # return 403

        # -- Decode Action -----------------------------------------------------
        # AllanC - could this be turned into a validator?
        def normalise_submit(kwargs):
            submit_keys = [key.replace("submit_","") for key in kwargs.keys() if key.startswith("submit_") and kwargs[key]!=None and kwargs[key]!='']
            if len(submit_keys) == 0:
                return None
            if len(submit_keys) == 1:
                return submit_keys[0]
            raise action_error(_('multiple submit types submited'), code=400)
        submit_type = normalise_submit(kwargs)

        # -- Validate ----------------------------------------------------------
        
        # Select Validation Schema (based on content type)
        schema = ContentSchema()
        if kwargs.get('type') == 'comment':
            schema = ContentCommentSchema()
        
        try:
            kwargs = schema.to_python(kwargs) # Validate
        except formencode.Invalid, error: # Failed Validation - Raise Error
            dict_validated        = error.value
            dict_validated_errors = error.error_dict or {}
            print ""
            print "content validation failed --------------------------"
            print dict_validated_errors
            raise action_error(
                status   = 'invalid' ,
                code     = 400 ,
                message  = _('failed validation') ,
                data     = {'invalid':dict_validated_errors} # TODO: we need to consider how this is returned to the user
            )
        
        # -- Set Content fields ------------------------------------------------
        
        # TODO: dont allow licence type change after publication - could this be part of validators?
        
        # Morph Content type - if needed (only appropriate for data already in DB)
        starting_content_type = content.__type__
        if submit_type == 'publish' and 'type' not in kwargs: # If publishing set 'type' (as this is submitted from the form as 'target_type')
            if hasattr(content, 'target_type'):
                kwargs['type'] = content.target_type
            if 'target_type' in kwargs:
                kwargs['type'] = kwargs['target_type']                
        if 'type' in kwargs:
            content = morph_content_to(content, kwargs['type'])
        
        # Set content fields from validated kwargs input
        for field in schema.fields.keys():
            if field in kwargs and hasattr(content,field):
                #print "set %s as %s" % (field, kwargs[field])
                setattr(content,field,kwargs[field])
        
        # Update Existing Media - Form Fields
        for media in content.attachments:
            # Update media item fields
            caption_key = "media_caption_%d" % (media.id)
            if caption_key in kwargs:
                media.caption = kwargs[caption_key]
            credit_key = "media_credit_%d"   % (media.id)
            if credit_key in kwargs:
                media.credit = kwargs[credit_key]
            # Remove media if required
            if "file_remove_%d" % media.id in kwargs:
                content.attachments.remove(media)
        
        # Add Media - if file present in form post
        if 'media_file' in kwargs and kwargs['media_file'] != "":
            form_file = kwargs["media_file"]
            media = Media()
            media.load_from_file(tmp_file=form_file, original_name=form_file.filename, caption=kwargs["media_caption"], credit=kwargs["media_credit"])
            content.attachments.append(media)
            #Session.add(media) # is this needed as it is appended to content and content is in the session?
        
        # -- Publishing --------------------------------------------------------
        if submit_type == 'publish':
            # Profanity Check
            profanity_filter(content) # Filter any naughty words and alert moderator TODO: needs to be threaded (raised on redmine)
            
            content.private = False # TODO: all published content is currently public ... this will not be the case for all publish in future
            
            # Notifications
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


        # -- Save to Database --------------------------------------------------
        Session.add(content)     
        Session.commit()         
        update_content(content)  #   Invalidate any cache associated with this content
        user_log.info("updated Content #%d" % (content.id, )) # todo - move this so we dont get duplicate entrys with the publish events above 
        
        # -- Redirect ----------------------------------------------------------
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
        
        #c.content                  = form_to_content(kwargs, c.content)
        c.content_media_upload_key = get_content_media_upload_key(c.content)
        
        return action_ok() # Automatically finds edit template

