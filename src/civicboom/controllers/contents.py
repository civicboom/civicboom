# Base controller imports
from civicboom.lib.base import *

# Datamodel and database session imports
from civicboom.model                   import Media, Content, CommentContent, DraftContent, CommentContent, ArticleContent, AssignmentContent, Boom
from civicboom.lib.database.get_cached import update_content, get_licenses, get_license, get_tag, get_assigned_to, get_content as _get_content
from civicboom.model.content           import _content_type as content_types, publishable_types

# Other imports
from civicboom.lib.misc import str_to_int
from civicboom.lib.civicboom_lib import profanity_filter, twitter_global
from civicboom.lib.communication import messages
from civicboom.lib.database.polymorphic_helpers import morph_content_to


# Validation
import formencode
import civicboom.lib.form_validators.base
from civicboom.lib.form_validators.dict_overlay import validate_dict

# Search imports
from civicboom.lib.search import *
from civicboom.lib.database.gis import get_engine
from civicboom.model      import Content, Member
from sqlalchemy           import or_, and_, null
from sqlalchemy.orm       import join, joinedload, defer
import datetime

# Other imports
from sets import Set # may not be needed in Python 2.7+


# Logging setup
log      = logging.getLogger(__name__)



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
    due_date    = civicboom.lib.form_validators.base.IsoFormatDateConverter(not_empty=False)
    event_date  = civicboom.lib.form_validators.base.IsoFormatDateConverter(not_empty=False)
    default_response_license_id  = civicboom.lib.form_validators.base.LicenseValidator(not_empty=False)
    # TODO: need date validators to check date is in future (and not too far in future as well)


class ContentCommentSchema(ContentSchema):
    parent_id   = civicboom.lib.form_validators.base.ContentObjectValidator(not_empty=True, empty=_('comments must have a valid parent'))
    content     = civicboom.lib.form_validators.base.ContentUnicodeValidator(not_empty=True, empty=_('comments must have content'))


#-------------------------------------------------------------------------------
# Global Functions
#-------------------------------------------------------------------------------


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
    
    def append_search_creator(query, creator):
        return query.filter(Content.creator_id==normalize_member(creator))
        #creator = 
        #if isinstance(creator, int):
        #else:
            # AllanC - WARNING this is untested ... all creators should be normalized - I dont think this is ever called
            # THIS WILL NOT WORK UNLESS - select_from(join(Content, Member, Content.creator)).
            #return query.filter(Member.username==creator)
            #raise Exception('unsuported search operation')
    
    def append_search_response_to(query, content_id):
        if isinstance(content_id, Content):
            content_id = content_id.id
        return query.filter(Content.parent_id==int(content_id))

    def append_search_boomed_by(query, member):
        member = normalize_member(member)
        #return query.filter(Boom.member_id==member) #join(Member.boomed_content, Boom)
        return query.filter(Content.id.in_(Session.query(Boom.content_id).filter(Boom.member_id==member)))

    search_filters = {
        'id'         : append_search_id ,
        'creator'    : append_search_creator ,
        'term'       : append_search_text ,
        'location'   : append_search_location ,
        'type'       : append_search_type ,
        'response_to': append_search_response_to ,
        'boomed_by'  : append_search_boomed_by ,
    }
    
    return search_filters

search_filters = _init_search_filters()


list_filters = {
    'all'                 : lambda results: results ,
    'assignments_active'  : lambda results: results.filter(Content.__type__=='assignment').filter(or_(AssignmentContent.due_date>=datetime.datetime.now(),AssignmentContent.due_date==null())) ,
    'assignments_previous': lambda results: results.filter(Content.__type__=='assignment').filter(or_(AssignmentContent.due_date< datetime.datetime.now())) ,
    'assignments'         : lambda results: results.filter(Content.__type__=='assignment') ,
    'drafts'              : lambda results: results.filter(Content.__type__=='draft') ,
    'articles'            : lambda results: results.filter(and_(Content.__type__=='article', ArticleContent.approval=='none')),
    'responses'           : lambda results: results.filter(and_(Content.__type__=='article', ArticleContent.approval!='none')),
}


def sqlalchemy_content_query(include_private=False, **kwargs):
    """
    Returns an SQLAlchemy query object
    This is used in the main contents/index and also to create a union stream of 2 querys
    """

    # Build Search
    results = Session.query(Content)
    results = results.with_polymorphic('*')
    #results = results.options(defer(Content.content)) # exculude fetch of content field in this query return. we never need the full content in a list TODO: this will only become efficent IF content_short postgress trigger is implemented (issue #257)
    results = results.filter(and_(Content.__type__!='comment', Content.visible==True))
    
    #if 'private' in kwargs and logged_in_creator:
    if include_private:
        pass # allow private content
    else:
        results = results.filter(Content.private==False) # public content only
    if 'creator' in kwargs.get('include_fields',[]):
        results = results.options(joinedload('creator'))
    if 'attachments' in kwargs.get('include_fields',[]):
        results = results.options(joinedload('attachments'))
    if 'tags' in kwargs.get('include_fields',[]):
        results = results.options(joinedload('tags'))
    for key in [key for key in search_filters.keys() if key in kwargs]: # Append filters to results query based on kwarg params
        if kwargs[key]:
            results = search_filters[key](results, kwargs[key])
    if 'list' in kwargs:
        if kwargs['list'] in list_filters:
            results = list_filters[kwargs['list']](results)
        else:
            raise action_error(_('list %s not supported') % kwargs['list'], code=400)
    return results


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
    
    @web
    def index(self, union_query=None, **kwargs):
        """
        GET /contents: All items in the collection

        @api contents 1.0 (WIP)

        @param limit
        @param offset
        @param include_fields   "attachments" for media
        @param sort             comma separted list of col names e.g rating,creator,-update_date (- denotes alternate sorting)
        @param *                (see common list return controls)

        @return 200      list ok
                list     array of content objects
        """
        # url('contents')
        
        # Permissions
        # AllanC - to aid cacheing we need permissions to potentially be a decorator
        #          TODO: we need maybe a separte call, or something to identify a private call
        logged_in_creator = False
        if 'creator' in kwargs:
            kwargs['creator'] = normalize_member(kwargs['creator']) # normalize creator
            if c.logged_in_persona and kwargs['creator'] == c.logged_in_persona.id:
                logged_in_creator = True
        
        # Setup search criteria
        if 'include_fields' not in kwargs:
            kwargs['include_fields'] = ""
        if 'exclude_fields' not in kwargs:
            kwargs['exclude_fields'] = ""
        if 'creator' not in kwargs:
            kwargs['include_fields'] += ",creator"
            kwargs['exclude_fields'] += ",creator_id"
        
        include_private_content = 'private' in kwargs and logged_in_creator
        results = sqlalchemy_content_query(include_private = include_private_content, **kwargs)
        if union_query:
            results = results.union(union_query)

        # Sort
        if 'sort' not in kwargs:
            sort = 'update_date'
        # TODO: use kwargs['sort']
        results = results.order_by(Content.update_date.desc())
        
        # Count
        count = results.count()
        
        # Limit & Offset
        kwargs['limit']  = str_to_int(kwargs.get('limit'), config['search.default.limit.contents'])
        kwargs['offset'] = str_to_int(kwargs.get('offset')                                        )
        results = results.limit(kwargs['limit']).offset(kwargs['offset']) # Apply limit and offset (must be done at end)
        
        # Return search results
        return action_ok(
            data = {'list': {
                'items' : [content.to_dict(**kwargs) for content in results.all()] ,
                'count' : count ,
                'limit' : kwargs['limit'] ,
                'offset': kwargs['offset'] ,
                'type'  : 'content' ,
                }
            }
        )


    @web
    @auth
    def new(self, **kwargs):
        """
        GET /contents/new: Form to create a new item

        As file-upload and such require an existing object to add to,
        we create a blank object and redirect to "edit-existing" mode
        """
        #url_for('new_content')
        create_ = ContentsController().create(**kwargs)
        # AllanC TODO - needs restructure - see create
        if c.format=='html' or c.format=='redirect':
            return redirect(url('edit_content', id=create_['data']['id']))
        return create_


    @web
    @auth
    def create(self, **kwargs):
        """
        POST /contents: Create a new item

        @api contents 1.0 (WIP)

        @param type
        @param *  see "PUT /contents/id"

        @return 201   content created
                id    new content id
        @return *     see update return types
        """
        # url('contents') + POST

        user_log.info("Creating new content")

        if kwargs.get('type') == None:
            kwargs['type'] = 'draft'
        
        # Create Content Object
        if   kwargs['type'] == 'draft':
            raise_if_current_role_insufficent('contributor')
            content = DraftContent()
        elif kwargs['type'] == 'comment':
            raise_if_current_role_insufficent('editor')
            content = CommentContent()
        elif kwargs['type'] == 'article':
            raise_if_current_role_insufficent('editor') # Check permissions
            content = ArticleContent()                  # Create base content
            kwargs['submit_publish'] = True             # Ensure call to 'update' publish's content
        elif kwargs['type'] == 'assignment':
            raise_if_current_role_insufficent('editor') # Check permissions
            content = AssignmentContent()               # Create base content
            kwargs['submit_publish'] = True             # Ensure call to 'update' publish's content
        
        # Set create to currently logged in user
        content.creator = c.logged_in_persona
        
        
        parent = _get_content(kwargs.get('parent_id'))
        if parent:
            # If a license isn't explicitly set, use the parent's preference
            if not kwargs.get('license_id'):
                if parent and parent.__type__ == 'assignment' and parent.default_response_license:
                    content.license = parent.default_response_license
            # if a title isn't set but we have a parent, title = "Re: parent title"
            if not kwargs.get('title'):
                if parent and parent.title:
                    content.title = "Re: "+parent.title

        # comments are always owned by the writer; ignore settings
        # and parent preferences
        if type == 'comment':
            content.license = get_license(None)

        # Commit to database to get ID field
        # DEPRICATED
        #Session.add(content)
        #Session.commit()
        # AllanC - if the update fails on validation we do not want a ghost record commited
        
        # Use update behaviour to save and commit object
        
        update_response = self.update(id=content, **kwargs)
        
        if update_response['status'] != 'ok':
            return update_response
        
        return action_ok(message=_('_content created'), data={'id':content.id}, code=201)


    @web
    @auth
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
        #print("--KWARGS--")
        #print(kwargs)
        #print("")
        
        # -- Variables-- -------------------------------------------------------
        content_redirect = None
        error            = None
        
        # -- Get Content -------------------------------------------------------
        if isinstance(id, Content):
            content = id
        else:
            content = get_content(id, is_editable=True)
        assert content
        
        # -- Validate ----------------------------------------------------------

        # Select Validation Schema (based on content type)
        schema = ContentSchema()
        if kwargs.get('type') == 'comment':
            schema = ContentCommentSchema()
            # AllanC - HACK! the validators cant handle missing fields .. so we botch an empty string field in here
            if 'parent_id' not in kwargs:
                kwargs['parent_id'] = ''
        
        # Validation needs to be overlayed oved a data dictonary, so we wrap kwargs in the data dic
        data       = {'content':kwargs}
        data       = validate_dict(data, schema, dict_to_validate_key='content', template_error='content/edit')
        kwargs     = data['content']

        # -- Decode Action -----------------------------------------------------
        #
        # Takes the form field 'submit_????' and decides operation:
        #            = Save + forward back to editor
        #   preview  = Save + forward to show
        #   publish  = Save + Publish (send notifications) + forward to show
        #   response = Save + show parent
        #
        # Default
        #  Save + (if format = html or redirect -> redirect back to editor)
        #  if no submit_???? is provided and the content type = draft -> article or assignment - pubmit type is set to 'publish'
        #
        
        def normalise_form_submit(kwargs):
            submit_keys = [key.replace("submit_","") for key in kwargs.keys() if key.startswith("submit_") and kwargs[key]!=None and kwargs[key]!='']
            if len(submit_keys) == 0:
                return None
            if len(submit_keys) == 1:
                return submit_keys[0]
            raise action_error(_('Multiple submit types submitted'), code=400)
            
        if content.__type__ not in publishable_types and kwargs.get('type') in publishable_types:
            submit_type = 'publish'
            log.debug ( "AUTO PUBLISH! %s - %s" % (content.__type__, kwargs.get('type')) )
        else:
            submit_type = normalise_form_submit(kwargs)
        
        # Normalize 'type'
        starting_content_type = content.__type__ # This is required later to assertain if this is an update or a new item of content
        if submit_type == 'publish' and 'type' not in kwargs: # If publishing set 'type' (as this is submitted from the form as 'target_type')
            if hasattr(content, 'target_type'):
                kwargs['type'] = content.target_type
            if kwargs.get('target_type'):
                kwargs['type'] = kwargs['target_type']
        

        # -- Publish Permission-------------------------------------------------
        # some permissions like permissions['can_publish'] could be related to payment, we want to still save the data, but we might not want to go through with the whole publish procedure
        # The content will save and the error will be raised at the end.
        permissions = {}
        permissions['can_publish'] = True
        
        if kwargs.get('type') in publishable_types and not has_role_required('editor', c.logged_in_persona_role):
            permissions['can_publish'] = False
            error                      = errors.error_role()
        
        if kwargs.get('type') == 'assignment' and not c.logged_in_persona.can_publish_assignment():
            permissions['can_publish'] = False
            error                      = errors.error_account_level()
            
        
        # -- Set Content fields ------------------------------------------------
        
        # TODO: dont allow licence type change after publication - could this be part of validators?
        
        # Morph Content type - if needed (only appropriate for data already in DB)
        if 'type' in kwargs:
            if kwargs.get('type') not in publishable_types or \
               kwargs.get('type')     in publishable_types and permissions['can_publish']:
                content = morph_content_to(content, kwargs['type'])
        
        # Set content fields from validated kwargs input
        for field in schema.fields.keys():
            if field in kwargs and hasattr(content,field):
                #log.debug("set %s as %s" % (field, kwargs[field]))
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
            media.load_from_file(tmp_file=form_file, original_name=form_file.filename, caption=kwargs.get('media_caption'), credit=kwargs.get('media_credit'))
            content.attachments.append(media)
            #Session.add(media) # is this needed as it is appended to content and content is in the session?

        # Tags
        if 'tags_string' in kwargs:
            separator = config['setting.content.tag_string_separator']
            tags_new     = [tag.strip() for tag in kwargs['tags_string'].split(separator) if tag!=""] # Get tags from form removing any empty strings
            tags_current = [tag.name for tag in content.tags] # Get tags form current content object
            # Add any new tag objects
            for tag in Set(tags_new).difference(tags_current):
                content.tags.append(get_tag(tag))
            # Remove any missing tag objects
            content.tags = [tag for tag in content.tags if tag.name in tags_new]
        
        
        # -- Publishing --------------------------------------------------------
        if  submit_type=='publish'     and \
            permissions['can_publish'] and \
            content.__type__ in publishable_types:
            
            # Profanity Check --------------------------------------------------
            profanity_filter(content) # Filter any naughty words and alert moderator TODO: needs to be threaded (raised on redmine)
            
            content.private = False # TODO: all published content is currently public ... this will not be the case for all publish in future
            
            # Notifications ----------------------------------------------------
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
                
                content.comments = [] # Clear comments when upgraded from draft to published content? we dont want observers comments 
                
                user_log.info("published new Content #%d" % (content.id, ))
                # Aggregate new content
                content.aggregate_via_creator() # Agrigate content over creators known providers
                twitter_global(content) # TODO? diseminate new or updated content?
            else:
                # Send notifications about previously published content has been UPDATED
                if   content.__type__ == "assignment":
                    m = messages.assignment_updated           (creator=content.creator, assignment=content)
                # going straight to publish, content may not have an ID as it's
                # not been added and committed yet (this happens below)
                #user_log.info("updated published Content #%d" % (content.id, ))
            if m:
                # AllanC: TODO this needs to optimised! see issue #258 bulk messages are a blocking call
                content.creator.send_message_to_followers(m, delay_commit=True)


        # -- Save to Database --------------------------------------------------
        Session.add(content)
        Session.commit()
        update_content(content)  # Invalidate any cache associated with this content
        user_log.debug("updated Content #%d" % (content.id, )) # todo - move this so we dont get duplicate entrys with the publish events above
        
        # -- Redirect (if needed)-----------------------------------------------

        # We raise any errors at the end because we still want to save any draft content even if the content is not published
        if error:
            #log.debug("raising the error")
            #log.debug(error)
            raise error

        if not content_redirect:
            if   submit_type == 'publish' and permissions['can_publish']:
                content_redirect = url('content', id=content.id, prompt_aggregate=True)
            elif submit_type == 'preview':
                content_redirect = url('content', id=content.id)
            elif submit_type == 'response':
                content_redirect = url('content', id=content.parent_id)
            else:
                content_redirect = url('edit_content', id=content.id) # Default redirect back to editor to continue editing
        
        if c.format == 'redirect' or c.format == 'html':
            return redirect(content_redirect)
        
        
        return action_ok(_("_content has been saved"))


    @web
    @auth
    def delete(self, id, **kwargs):
        """
        DELETE /contents/{id}: Delete an existing item

        @api contents 1.0 (WIP)

        @return 200   content deleted successfully
        @return 403   lacking permission
        @return 404   no content to delete
        """
        # url('content', id=ID)
        content = get_content(id, is_editable=True)
        user_log.info("Deleting content %d" % content.id)
        content.delete()
        return action_ok(_("_content deleted"), code=200)


    @web
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
        
        content = get_content(id, is_viewable=True)
        
        if 'lists' not in kwargs:
            kwargs['lists'] = 'comments, responses, contributors, actions, accepted_status'
        
        data = {'content':content.to_dict(list_type='full', **kwargs)}
        
        # AllanC - cant be imported at top of file because that creates a coupling issue
        from civicboom.controllers.content_actions import ContentActionsController
        content_actions_controller = ContentActionsController()
        
        for list in [list.strip() for list in kwargs['lists'].split(',')]:
            if hasattr(content_actions_controller, list):
                data[list] = getattr(content_actions_controller, list)(content, **kwargs)['data']['list']
        
        # Increase content view count
        if hasattr(content,'views'):
            content_view_key = 'content_%s' % content.id
            if not session_get(content_view_key):
                session_set(content_view_key, True)
                content.views += 1
                Session.commit()
                # AllanC - invalidating the content on EVERY view does not make scence
                #        - a cron should invalidate this OR the templates should expire after X time
                #update_content(content)
        
        # Corporate plus customers want to be able to see what members have looked at an assignment
        if content.__type__=='assignment' and content.closed==True:
            member_assignment = get_assigned_to(content, member)
            if not member_assignment.member_viewed:
                member_assignment.member_viewed = True
                Session.commit()
        
        return action_ok(data=data)


    @web
    @authorize
    def edit(self, id, **kwargs):
        """
        GET /contents/{id}/edit: Form to edit an existing item
        """
        # url('edit_content', id=ID)
        
        c.content = get_content(id, is_editable=True)
        
        #c.content                  = form_to_content(kwargs, c.content)
        
        return action_ok(data={'content':c.content.to_dict(list_type='full')}) # Automatically finds edit template
