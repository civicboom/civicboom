# Base controller imports
from civicboom.lib.base import *

# Datamodel and database session imports
from civicboom.model                   import Media, Content, CommentContent, DraftContent, CommentContent, ArticleContent, AssignmentContent, Boom, UserVisibleContent
from civicboom.lib.database.get_cached import invalidate_content, get_license, get_tag, get_assigned_to, get_content as _get_content
from civicboom.model.content           import _content_type as content_types, publishable_types

# Other imports
from civicboom.lib.communication import messages
from civicboom.lib.database.polymorphic_helpers import morph_content_to
from civicboom.lib.database.actions             import respond_assignment

# Validation
import formencode
import civicboom.lib.form_validators.base
from civicboom.lib.form_validators.dict_overlay import validate_dict


# Search imports
from civicboom.model.filters import *
from civicboom.model      import Content, Member
from sqlalchemy           import or_, and_, null, func, Unicode, asc, desc
from sqlalchemy.orm       import join, joinedload, defer
from geoalchemy import Point
import datetime
from dateutil.parser import parse as parse_date

# Other imports
import re
from cbutils.text import strip_html_tags
import cbutils.worker as worker
from time import time

# Logging setup
log      = logging.getLogger(__name__)

_cache = {}

#-------------------------------------------------------------------------------
# Form Schema
#-------------------------------------------------------------------------------

class AutoPublishTriggerDatetimeValidator(civicboom.lib.form_validators.base.IsoFormatDateConverter):
    messages = {
        'require_upgrade'   : x_('You require a paid account to use this feature, please contact us!'),
        'date_past'         : x_('The auto publish date must be in the future'),
    }

    def _to_python(self, value, state):
        auto_publish_trigger_datetime = super(AutoPublishTriggerDatetimeValidator, self)._to_python(value, state)
        if not c.logged_in_persona.has_account_required('plus'):
            raise formencode.Invalid(self.message('require_upgrade', state), value, state)
        if auto_publish_trigger_datetime <= now():
            raise formencode.Invalid(self.message('date_past', state), value, state)
        return auto_publish_trigger_datetime


class ContentSchema(civicboom.lib.form_validators.base.DefaultSchema):
    allow_extra_fields  = True
    filter_extra_fields = False
    ignore_key_missing  = True
    type        = formencode.validators.OneOf(content_types.enums, not_empty=False)
    title       = civicboom.lib.form_validators.base.ContentUnicodeValidator(not_empty=True, strip=True, max=250, min=2, html='strip_html_tags')
    content     = civicboom.lib.form_validators.base.ContentUnicodeValidator()
    parent_id   = civicboom.lib.form_validators.base.ContentObjectValidator(not_empty=False)
    location    = civicboom.lib.form_validators.base.LocationValidator(not_empty=False)
    private     = civicboom.lib.form_validators.base.PrivateContentValidator(not_empty=False) #formencode.validators.StringBool(not_empty=False)
    license_id  = civicboom.lib.form_validators.base.LicenseValidator(not_empty=False)
    #creator_id  = civicboom.lib.form_validators.base.MemberValidator(not_empty=False) # AllanC - debatable if this is needed, do we want to give users the power to give content away? Could this be abused? # AllanC - The answer is .. YES IT COULD BE ABUSED!! ... dumbass ...
    #tags        = civicboom.lib.form_validators.base.ContentTagsValidator(not_empty=False) # not needed, handled by update method
    # Draft Fields
    target_type = formencode.validators.OneOf(content_types.enums, not_empty=False)
    # Assignment Fields
    due_date    = civicboom.lib.form_validators.base.IsoFormatDateConverter(not_empty=False)
    event_date  = civicboom.lib.form_validators.base.IsoFormatDateConverter(not_empty=False)
    auto_publish_trigger_datetime = AutoPublishTriggerDatetimeValidator(not_empty=False)
    default_response_license_id  = civicboom.lib.form_validators.base.LicenseValidator(not_empty=False)
    # TODO: need date validators to check date is in future (and not too far in future as well)


class ContentCommentSchema(ContentSchema):
    parent_id   = civicboom.lib.form_validators.base.ContentObjectValidator(not_empty=True, empty=_('comments must have a valid parent'))
    content     = civicboom.lib.form_validators.base.ContentUnicodeValidator(not_empty=True, empty=_('comments must have content'), max=config['setting.content.max_comment_length'], html='strip_html_tags')


#-------------------------------------------------------------------------------
# Global Functions
#-------------------------------------------------------------------------------

list_filters = {
    'all'                 : lambda: AndFilter([
    ]),
    'assignments_active'  : lambda: AndFilter([
        TypeFilter('assignment'),
        OrFilter([
            DueDateFilter(">", "now()"),
            DueDateFilter("IS", "NULL")
        ])
    ]),
    'assignments_previous': lambda: AndFilter([
        TypeFilter('assignment'),
        DueDateFilter("<", "now()")
    ]),
    'assignments'         : lambda: AndFilter([
        TypeFilter('assignment'),
    ]),
    'drafts'              : lambda: AndFilter([
        TypeFilter('draft'),
        CreatorFilter(c.logged_in_persona.id if c.logged_in_persona else None)
    ]),
    'articles'            : lambda: AndFilter([
        TypeFilter('article'),
        ParentIDFilter(False)
    ]),
    'responses'           : lambda: AndFilter([
        TypeFilter('article'),
        ParentIDFilter(True)
    ]),
    'not_drafts'          : lambda: AndFilter([
        NotFilter(TypeFilter('draft')),
    ]),
}


def sort_results(results, sort_fields):
    def valid_sort_field(field):
        if field in [col["name"] for col in results.column_descriptions]:
            return field
        if hasattr(Content           , field):
            return getattr(Content           , field)
        if hasattr(UserVisibleContent, field):
            return getattr(UserVisibleContent, field)
        if hasattr(AssignmentContent, field):
            return getattr(AssignmentContent, field)
        return None

    for sort_field in sort_fields:
        direction = asc
        if sort_field[0] == "-":
            direction = desc
            sort_field = sort_field[1:]

        # check that the sort string is the name of a column in the result
        # set, rather than some random untrusted SQL statement
        f = valid_sort_field(sort_field)
        if f:
            #log.debug("Sorting by %s %s" % (direction, f))
            results = results.order_by(direction(f))

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

    
    @web
    def index(self, _filter=None, **kwargs):
        """
        GET /contents: Content Search
        @type list
        @api contents 1.0 (WIP)
        
        @param list
            'all'                    (default) all content
            'assignments_active'     assignments with a due date in the future
            'assignments_previous'   assignments with a due date in the past
            'assignments'            all assignments reguardless of due date
            'drafts'                 drafts
            'articles'               articles that do not have a parent
            'responses'              articles that have a parent
        @param creator      username or user_id of creator
        @param term         text to search for (searchs title and body text)
        @param location     TODO use 'me' to use logged in personas current location
        @param type
            'article'
            'assignment'
            'draft'
        @param due_date     find the due date of an assignment, eg "due_date=<2000/11/01" for old assignments, "due_date=>now" for open ones
        @param update_date  search by most recent update date, eg "update_date=<2000/11/01" for old articles
        @param response_to  content_id of parent
        @param boomed_by    username or user_id of booming user
        @param exclude_content a list of comma separated content id's to exclude from the content returned
        @param private      if set and creator==logged_in_persona both public and private content will be returned
        @param sort         comma separated list of fields, prefixed by '-' for decending order (default '-update_date')
        @param * (see common list return controls)
        
        @return 200      list ok
            list list of content objects
        
        @example https://test.civicboom.com/contents.json?creator=unittest&limit=2
        @example https://test.civicboom.com/contents.rss?list=assignments_active&limit=2
        @example https://test.civicboom.com/contents.json?limit=1&list_type=empty&include_fields=id,views,title,update_date
        
        @comment AllanC use 'include_fields=attachments' for media
        @comment AllanC if 'creator' not in params or exclude list then it is added by default to include_fields:
        """

        # Pre-process kwargs ---------------------------------------------------
        #
        # This must be done before caching - we assertain if private content can be shown to this user

        kwargs['_is_logged_in_as_creator'] = False # Setup placeholder kwargs for permissions options - this must be done because a cheeky user might try and pass them
        kwargs['_is_trusted_follower'    ] = False

        # Setup default search criteria
        if 'include_fields' not in kwargs:
            kwargs['include_fields'] = "creator"
        if kwargs.get('list') == 'responses': # HACK - AllanC - mini hack, this makes the API behaviour slightly unclear, but solves a short term problem with creating response lists - it is common with responses that you have infomation about the parent
            kwargs['include_fields'] += ",parent"


        creator = None

        try:
            # If displaying responses - Try to get the creator of the whole parent chain or creator of self
            # This models the same permission view enforcement as the 'show' private content API call
            if kwargs.get('response_to'):
                parent_root = get_content(kwargs['response_to'])
                parent_root = parent_root.root_parent or parent_root
                creator     = parent_root.creator
                kwargs['list'] = 'not_drafts' # AllanC - HACK!!! when dealing with responses to .. never show drafts ... there has to be a better when than this!!! :( sorry
        except Exception as e:
            user_log.exception("Error searching:")

        #try:
        if kwargs.get('creator'):
            creator = get_member(kwargs['creator'])
            if creator:
                kwargs['creator'] = creator.username
            #kwargs['creator'] = normalize_member(creator) # normalize creator param for search # AllanC - will be normalize with the other fields later
        #except Exception as e:
        #    user_log.exception("Error searching:")
        
        if creator:
            if c.logged_in_persona == creator:
                kwargs['_is_logged_in_as_creator'] = True
            else:
                kwargs['_is_trusted_follower'    ] = creator.is_follower_trusted(c.logged_in_persona)


        # Normalize kwargs -----------------------------------------------------
        #  do not allow db objects to be used as params
        
        for key, value in kwargs.iteritems():
            if not key.startswith('_'): # skip keys beggining with '_' as these have already been processed
                #try   : value = value.__db_index__() # AllanC if it has an id use it. This should work for all db objects and not require the __db_index__ function
                try   : value = value.id
                except: pass
                # AllanC: Suggestion - do we want to allow primitive types to pass through, e.g. int's and floats, maybe dates as well?
                value = str(value).strip()
            kwargs[key] = value
        
        cache_key = ''
        keys_sorted = [k for k in kwargs.keys()]
        keys_sorted.sort()
        for key in keys_sorted:
            cache_key += str(kwargs[key]) + '|'
        if _filter:
            cache_key += sql(_filter) # Create a string representation of the passed filters so that they form part of the cache key
        

        # Construct Query with provided kwargs ---------------------------------
        # Everything past here can be cached based on the kwargs state

        def contents_index(_filter=None, **kwargs):

            time_start = time()
            
            results = Session.query(Content).with_polymorphic('*') # TODO: list
            results = results.filter(Content.__type__!='comment').filter(Content.visible==True)
    
            if kwargs['_is_logged_in_as_creator']:
                pass # allow private content
            else:
                if not kwargs['_is_trusted_follower']:
                    results = results.filter(Content.private==False) # public content only
                results = results.filter(Content.__type__!='draft') # Don't show drafts to anyone other than the creator
    
            # AllanC - Optimise joined loads - sub fields that we know are going to be used in the query return should be fetched when the main query fires
            for col in ['creator', 'attachments', 'tags']:
                if col in kwargs.get('include_fields', []):
                    results = results.options(joinedload(getattr(Content, col)))
    
            parts = []
    
            try:
                if _filter:
                    parts.append(_filter)
    
                filter_map = {
                    'creator'    : CreatorFilter   ,
                    'due_date'   : DueDateFilter   ,
                    'update_date': UpdateDateFilter,
                    'type'       : TypeFilter      ,
                    'response_to': ParentIDFilter  ,
                    'boomed_by'  : BoomedByFilter  ,
                    'term'       : TextFilter      ,
                    'location'   : LocationFilter  ,
                }
    
                if 'list' in kwargs:
                    if kwargs['list'] in list_filters:
                        parts.append(list_filters[kwargs['list']]())
                    else:
                        raise action_error(_('list %s not supported') % kwargs['list'], code=400)
    
                if 'feed' in kwargs and kwargs['feed']:
                    parts.append(Session.query(Feed).get(int(kwargs['feed'])).query)
    
                for filter_name in filter_map:
                    val = kwargs.get(filter_name, '') # AllanC - should already be a string as the normaize decorator should have fired - this strips and strings the input arguments
                    #val = str(kwargs.get(filter_name, '')).strip()
                    if val:
                        f = filter_map[filter_name].from_string(val)
                        if hasattr(f, 'mangle'):
                            results = f.mangle(results)
                        parts.append(f)
    
                if 'include_content' in kwargs and kwargs['include_content']:
                    parts.append(IDFilter([int(i) for i in kwargs['include_content'].split(",")]))
    
                if 'exclude_content' in kwargs and kwargs['exclude_content']:
                    parts.append(NotFilter(IDFilter([int(i) for i in kwargs['exclude_content'].split(",")])))
            except FilterException as fe:
                raise action_error(code=400, message=str(fe))
    
            feed = AndFilter(parts)
    
            # FIXME: these brackets are a hack, SQLAlchemy does "blah AND filter", not "(blah) AND (filter)",
            # so filter="x OR y" = "blah AND x OR y" = "(blah AND x) OR y"
            results = results.filter("("+sql(feed)+")")
            results = sort_results(results, kwargs.get('sort', '-update_date').split(','))
            
            results = to_apilist(results, obj_type='contents', **kwargs)
            
            # hacky benchmarking just to get some basic idea of how each feed performs
            time_end = time()
            log.debug("Searching contents: %s [%f]" % (sql(feed), time_end - time_start))
    
            return results
        
        cache_func = lambda: contents_index(_filter, **kwargs)
        if _cache.get('contents_index'):
            return _cache.get('contents_index').get(key=cache_key, createfunc=cache_func)
        return cache_func()



    @web
    @auth
    @role_required('contributor')
    def new(self, **kwargs):
        """
        GET /contents/new: Form to create a new item

        As file-upload and such require an existing object to add to,
        we create a blank object and redirect to "edit-existing" mode
        """
        #url_for('new_content')
        create_ = ContentsController().create(**kwargs)
        # AllanC TODO - needs restructure - see create
        if create_['data'].get('id') and (c.format=='html' or c.format=='redirect'):
            return redirect(url('edit_content', id=create_['data']['id']))

        if isinstance(create_, action_error):
            raise create_
        else:
            return create_


    @web
    @auth
    #@role_required('contributor') # AllanC - this is handled internally and would have prevented observers from commenting
    def create(self, **kwargs):
        """
        POST /contents: Create a new item
        @type action
        @api contents 1.0 (WIP)

        @param type
        @param *  see "PUT /contents/id"

        @return 201   content created
                id    new content id
        @return *     see update return types
        
        @comment AllanC The prefered way of posting comments from a remote site is http://test.civicboom.com/contents?type=comment&format=redirect
                        currently the action being performed is recodnised by the string /contents?type=comment
                        the format=redirect is a cool way to return you to your site at the end of posting usinging the http_referer
                        (unless they have to signup, at witch point the redirect will be lost)
        """
        # url('contents') + POST

        user_log.info("Creating new content: %s" % kwargs.get('title', '[no title]'))
        
        if kwargs.get('type') == None:
            kwargs['type'] = 'draft'

        # GregM: Set private flag to user or hub setting (or public as default)
        kwargs['private'] = kwargs.get('private', (c.logged_in_persona.default_content_visibility == 'private' if c.logged_in_persona.__type__ == 'group' else False)) # Set drafts visability to default to private

        if c.logged_in_persona.__type__ == 'group' and kwargs['private'] and not c.logged_in_persona.has_account_required('plus'):
            flash_message = {'status':'error', 'message':_('Your group is set to create private content, however you need to upgrade your account in order to use the private content feature')}
            set_flash_message(flash_message)
            if c.format == 'redirect' or c.format == 'html':
                return redirect(current_referer())
            else:
                raise action_error(message=flash_message['message'], code=400)

        # Create Content Object
        if   kwargs['type'] == 'draft':
            raise_if_current_role_insufficent('contributor')
            content = DraftContent()
        elif kwargs['type'] == 'comment':
            raise_if_current_role_insufficent('observer') # Check role, in adition the content:update method checks for view permission of parent
            content = CommentContent()
            kwargs['private'] = False                          # Comments are always public
            content.creator = c.logged_in_user          # Comments are always made by logged in user
        elif kwargs['type'] == 'article':
            raise_if_current_role_insufficent('editor') # Check permissions
            content = ArticleContent()                  # Create base content
            kwargs['submit_publish'] = True             # Ensure call to 'update' publish's content
        elif kwargs['type'] == 'assignment':
            raise_if_current_role_insufficent('editor') # Check permissions
            content = AssignmentContent()               # Create base content
            kwargs['submit_publish'] = True             # Ensure call to 'update' publish's content
        
        # Set create to currently logged in user
        if not content.creator:
            content.creator = c.logged_in_persona
        
        # GregM: Set private flag to user or hub setting (or public as default)
        #content.private = is_private
        
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
            if kwargs['type'] != 'comment':
                # If parent is an assignment then 'auto accept' it - ignore all errors, except 403 - propergate it up
                from civicboom.controllers.content_actions import ContentActionsController
                content_accept = ContentActionsController().accept
                try:
                    content_accept(id=parent)
                except action_error as ae:
                    if ae.original_dict.get('code') == 403:
                        raise ae
                

        # comments are always owned by the writer; ignore settings
        # and parent preferences
        if type == 'comment':
            content.license = get_license(None)

        # Flush to database to get ID field
        # AllanC - if the update fails on validation we do not want a ghost record commited
        # Shish - the "no id" error is back, adding a flush seems to fix it, and doesn't commit
        Session.flush()
        
        # Use update behaviour to save and commit object
        update_response = self.update(id=content, **kwargs)
        
        if update_response['status'] != 'ok':
            return update_response
        
        return action_ok(message=_('_content created'), data={'id':content.id}, code=201)


    @web
    @auth
    #@role_required('contributor') - AllanC see comment for cretate
    def update(self, id, **kwargs):
        """
        PUT /contents/{id}: Update an existing item
        @type action
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
        
        # AllanC - there was confution over when content was 'created'
        #  It used to be done by checking if the content object type had changed e.g. draft -> article
        #  this is insufficent for objects created directly as 'assignmen' etc.
        #  This variable stores if this call to updae has come from a create method.
        called_from_create_method = False 
        
        # -- Get Content -------------------------------------------------------
        if isinstance(id, Content):
            content = id
            called_from_create_method = True # AllanC - see above - only create calls pass the id as a content object
            # AllanC - note! normal users cannot pass a content object. passing an object does NOT check the c.logged_in_persona permissions, this is needed for some autopublish behaviour but should be kept in mind by other developers passing objects
        else:
            content = get_content(id, is_editable=True)
        assert content
        
        # -- Validate ----------------------------------------------------------
        
        # Select Validation Schema (based on content type)
        schema = ContentSchema()
        if kwargs.get('type', content.__type__) == 'comment':
            schema = ContentCommentSchema()
            # AllanC - HACK! the validators cant handle missing fields .. so we botch an empty string field in here
            if 'parent_id' not in kwargs:
                kwargs['parent_id'] = ''
        
        # Validation needs to be overlayed oved a data dictonary, so we wrap kwargs in the data dic - will raise invalid if needed
        data       = {'content':kwargs}
        data       = validate_dict(data, schema, dict_to_validate_key='content', template_error='contents/edit')
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
        #  if no submit_???? is provided and the content type = draft -> article or assignment - submit type is set to 'publish'
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
        
        # If 'assignment' and creator has permissions to publish - it has to be 'creator' rather than c.logged_in_persona because this might be auto publishing and the user may not be logged in
        if kwargs.get('type') == 'assignment' and not content.creator.can_publish_assignment():
            permissions['can_publish'] = False
            error                      = errors.error_account_level()
            #user_log.info('insufficent prvilages to - publish assignment %d' % content.id) # AllanC - unneeded as we log all errors in @auto_format_output now
            
        
        # -- Set Content fields ------------------------------------------------
        
        # TODO: dont allow licence type change after publication - could this be part of validators?
        
        # Auto Convert Responses to comments if too short. - AllanC -
        # Special behaviour for updating drafts to articles. Some users don't understand the concept of responses are deep responsese.
        # IF
        # 1.) Draft -> Article
        # 2.) Has parent
        # 3.) publishing
        # 4.) No Media attached
        # 5.) content length <= comment max length
        # THEN
        # make it a comment rather than an article
        #
        # NOTE: This is the ONLY way comments can be made from a group.
        # This was also made with the asumption that users of the API would use the site properly - this code will trigger a 'not in db' warning from polymorphic helpers
        #   maybe bits need to be added to 'create' to avoid this issue
        if content.__type__ == 'draft' and kwargs.get('type')=='article' and \
           content.parent_id and \
           submit_type == 'publish' and \
           not content.attachments and not kwargs.get('media_file') and \
           len(kwargs.get('content', content.content)) <= config['setting.content.max_comment_length']:
            kwargs['type']    = 'comment' # This will trigger polymorphic helpers below to convert it to a comment
            kwargs['content'] = strip_html_tags(kwargs.get('content', content.content)) # HACK - AllanC - because the content validator has already triggered so I  manually force the removal of html tags - we dont want html in comments
        
        # Morph Content type - if needed (only appropriate for data already in DB)
        if 'type' in kwargs:
            if kwargs.get('type') not in publishable_types or \
               kwargs.get('type')     in publishable_types and permissions['can_publish']:
                extra_fields = dict(content.extra_fields)
                content = morph_content_to(content, kwargs['type'])
                # AllanC - when upgrading content from draft to published content there may be stored extra_fields that need transfering to actual fields. e.g due_date etc
                #          the cool thing is that the extra_fields submitted to the drafts have already been through the validator
                #          but they are strings .. and need to be converted ... ARARARRA!!
                for key, value in extra_fields.iteritems():
                    if hasattr(content, key):
                        try:
                            if value == "None": # hacky hack, because due_date=None was being stored as extra_fields={"due_date": "None"}
                                setattr(content, key, None)
                            elif value.isdigit(): # digits should be stored as digits to start with >_<
                                setattr(content, key, int(value))
                            else:
                                setattr(content, key, value)
                        except:
                            log.debug('unable to convert %s=%s to actual field - need to convert it from a string' % (key, value))
        
        # Set content fields from validated kwargs input
        for field in schema.fields.keys():
            if field in kwargs and hasattr(content,field):
                #log.debug("set %s as %s" % (field, kwargs[field]))
                setattr(content,field,kwargs[field])
        
        # Set the parent parent object manually as the content oject may not have been commited yet
        if not content.parent and content.parent_id:
            content.parent = get_content(content.parent_id)
            
        # Enforcing prvacy - if the parent is private so are all children
        #                    this is because if the parent is deleted we dont want all the children content to become visable to all users.
        if content.parent and content.parent.private:
            content.private = True
        
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
            tags_input   = set([tag.strip().lower() for tag in kwargs['tags_string'].split(config['setting.content.tag_string_separator']) if tag.strip()!=""]) # Get tags from form removing any empty strings
            tags_current = set([tag.name for tag in content.tags]) # Get tags form current content object
            content.tags = [tag for tag in content.tags if not tag.name in tags_current - tags_input] # remove unneeded tags
            for new_tag_name in tags_input - tags_current: # add new tags
                content.tags.append(get_tag(new_tag_name))
        
        # Extra fields
        permitted_extra_fields = ['due_date', 'event_date'] # AllanC - this could be customised depending on content.__type__ if needed at a later date
        for extra_field in [f for f in permitted_extra_fields if f in kwargs and not hasattr(content, f)]:
            if kwargs[extra_field] == None: # if due_date=None, we don't want to store due_date="None"
                if extra_field in content.extra_fields:
                    del content.extra_fields[extra_field]
            else:
                content.extra_fields[extra_field] = str(kwargs[extra_field])
            #AllanC - we need the str() here because when the extra_fields obj is serised to Json, it cant deal with objects.
            #         This is NOT acceptable for ints, floats, longs, or None
            #         I wanted to override __setitem__ in the extra fields object to do this conversion in the same day obj_to_dict works, but alas SQLAlchemy does some magic
        
        # -- Publishing --------------------------------------------------------
        if  submit_type=='publish'     and \
            permissions['can_publish'] and \
            content.__type__ in publishable_types:
            
            # GregM: Content can now stay private after publishing :)
            #content.private = False # TODO: all published content is currently public ... this will not be the case for all publish in future
            
            # Notifications ----------------------------------------------------
            # AllanC - as notifications not need commit anymore this can be done after?
            message_to_all_creator_followers = None
            if starting_content_type != content.__type__ or called_from_create_method:
                # Send notifications about NEW published content
                if   content.__type__ == "article"   :
                    message_to_all_creator_followers = messages.article_published_by_followed(creator=content.creator, article   =content)
                elif content.__type__ == "assignment":
                    message_to_all_creator_followers = messages.assignment_created           (creator=content.creator, assignment=content)
                
                # if this is a response - notify parent content creator
                if content.parent:
                    content.parent.creator.send_notification(
                        messages.new_response(member=content.creator, content=content, parent=content.parent, you=content.parent.creator)
                    )
                    
                    # if it is a response, mark the accepted status as 'responded'
                    respond_assignment(content.parent, content.creator, delay_commit=True)
                
                content.comments = [] # Clear comments when upgraded from draft to published content? we dont want observers comments 
                
                user_log.info("published new Content #%d" % (content.id, ))
                # Aggregate new content
                content.aggregate_via_creator() # Agrigate content over creators known providers
            else:
                # Send notifications about previously published content has been UPDATED
                if   content.__type__ == "assignment":
                    if content.update_date < now() - datetime.timedelta(days=1): # AllanC - if last updated > 24 hours ago then send an update notification - this is to stop notification spam as users update there assignment 10 times in a row
                        message_to_all_creator_followers = messages.assignment_updated(creator=content.creator, assignment=content)
                # going straight to publish, content may not have an ID as it's
                # not been added and committed yet (this happens below)
                #user_log.info("updated published Content #%d" % (content.id, ))
                
            if message_to_all_creator_followers:
                content.creator.send_notification_to_followers(message_to_all_creator_followers, private=content.private)
        
        # AllanC - is this the correct place to have comment notifications created?, as they cant be updated .. we can just gen the notifications safly once here?
        if content.__type__ == "comment":
            content.parent.creator.send_notification(
                messages.comment(member=content.creator, content=content, you=content.parent.creator)
            )
        
        # -- Save to Database --------------------------------------------------
        Session.add(content)
        Session.commit()
        invalidate_content(content)  # Invalidate any cache associated with this content
        user_log.debug("updated Content #%d" % (content.id, )) # todo - move this so we dont get duplicate entrys with the publish events above
        
        # Profanity Check --------------------------------------------------
        if config['feature.profanity_filter']:
            if (submit_type=='publish' and content.private==False) or content.__type__ == 'comment':
                worker.add_job({
                    'task'     : 'profanity_check',
                    'content_id': content.id,
                    'url_base' : url('',qualified=True) #'http://www.civicboom.com/' , # AllanC - get this from the ENV instead please
                })
        
        # -- Redirect (if needed)-----------------------------------------------
        
        # We raise any errors at the end because we still want to save any draft content even if the content is not published
        if error:
            #log.debug("raising the error")
            #log.debug(error)
            raise error
        
        if not content_redirect:
            if   submit_type == 'publish' and permissions['can_publish']:
                # Added prompt aggregate to new content url
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
    @role_required('editor')
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
        
        # AllanC - Short term hack
        #    We removed the concept of accepting an assignment as this was too complicated for users
        #    This is now a problem because we have removed the accept and withdraw buttons
        #    When content is created as a response accept() is automatically run
        #    There is no way users can withdraw() from assignments
        #
        #    This hack is here so that when a draft is removed the corresponding withdraw is performed too.
        #    Not a long term solution - we need to consider user flow - maybe removing the concept of accept altogether?
        #    We could just use drafts as the indicatior of number accepted.
        try:
            if content.__type__ == 'draft':
                from civicboom.controllers.content_actions import ContentActionsController
                ContentActionsController().withdraw(id=content.parent)
        except:
            pass
        
        content.delete()
        
        return action_ok(_("_content deleted"), code=200)


    @web
    def show(self, id, **kwargs):
        """
        GET /content/{id}: Show a specific item
        @type object
        @api contents 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200      page ok
                content  content object
        @return 403      permission denied
        @return 404      content not found
        
        @example https://test.civicboom.com/contents/1.json
        @example https://test.civicboom.com/contents/1.rss
        """
        # url('content', id=ID)
       
        content = get_content(id) #, is_viewable=True) # This is done manually below we needed some special handling for comments
        
        if content.__type__ == 'comment':
            if c.format == 'html' or c.format == 'redirect':
                return redirect(url('content', id=content.parent.id))
            if c.format == 'frag':
                content = content.parent # Bit of a HACK - if we try to read a content frag for a comment, just return the parent
        
        if not content.viewable_by(c.logged_in_persona):
            raise errors.error_view_permission()
        
        if 'lists' not in kwargs:
            kwargs['lists'] = 'comments, responses, contributors, actions, accepted_status'
        
        data = {'content':content.to_dict(list_type='full', **kwargs)}
        
        # AllanC - cant be imported at top of file because that creates a coupling issue
        from civicboom.controllers.content_actions import ContentActionsController
        content_actions_controller = ContentActionsController()
        
        for list in [list.strip() for list in kwargs['lists'].split(',')]:
            if hasattr(content_actions_controller, list):
                data[list] = getattr(content_actions_controller, list)(content.id, **kwargs)['data']['list']
        
        # Increase content view count
        if hasattr(content,'views'):
            content_view_key = 'content_%s' % content.id
            if not session_get(content_view_key):
                session_set(content_view_key, True)
                content.views += 1
                Session.commit()
                # AllanC - invalidating the content on EVERY view does not make scence
                #        - a cron should invalidate this OR the templates should expire after X time
                #invalidate_content(content)
        
        # Corporate plus customers want to be able to see what members have looked at an assignment
        if content.__type__=='assignment' and content.closed==True:
            member_assignment = get_assigned_to(content, member)
            if not member_assignment:
                return False
            if not member_assignment.member_viewed:
                member_assignment.member_viewed = True
                Session.commit()
            return True
        
        return action_ok(data=data)


    @web
    @authorize
    @role_required('contributor')
    def edit(self, id, **kwargs):
        """
        GET /contents/{id}/edit: Form to edit an existing item
        """
        # url('edit_content', id=ID)
        
        content = get_content(id, is_editable=True)
        
        return action_ok(
            data={
                'content': content.to_dict(list_type='full'),
                'actions': content.action_list_for(c.logged_in_persona, role=c.logged_in_persona_role),
            }
        ) # Automatically finds edit template
