# Base controller imports
from civicboom.lib.base import *

# Datamodel and database session imports
from civicboom.model                   import Media, Content, CommentContent, DraftContent, CommentContent, ArticleContent, AssignmentContent, UserVisibleContent # Boom, 
from civicboom.lib.database.get_cached import get_license, get_tag, get_assigned_to, get_content as _get_content
from civicboom.model.content           import _content_type as content_types, publishable_types

# Other imports
from civicboom.lib.database.polymorphic_helpers import morph_content_to

# Cache
from civicboom.lib.cache import _cache, get_cache_key, normalize_kwargs_for_cache, gen_key_for_lists

# Validation
import formencode
import civicboom.lib.form_validators.base
from civicboom.lib.form_validators.dict_overlay import validate_dict

# Search imports
from civicboom.model.filters import *
from sqlalchemy.orm       import joinedload
from sqlalchemy           import asc, desc

# Other imports
from cbutils.misc import substring_in
from cbutils.text import clean_html_markup, strip_html_tags

import markdown

import cbutils.worker as worker
from time import time

# Logging setup
log      = logging.getLogger(__name__)



# Unneeded
#from sqlalchemy.orm       import join,  defer
#from civicboom.model      import Content, Member
#from sqlalchemy           import or_, and_, null, func, Unicode, asc, desc # AllanC unneeded?
#from geoalchemy import Point
#from dateutil.parser import parse as parse_date # AllanC - unneeded?
#import re





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
    title       = civicboom.lib.form_validators.base.UnicodeStripHTMLValidator(not_empty=True, strip=True, max=250, min=2)
    #content     = civicboom.lib.form_validators.base.CleanHTMLValidator()
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
    #content     = civicboom.lib.form_validators.base.UnicodeStripHTMLValidator(not_empty=True, empty=_('comments must have content'), max=config['setting.content.max_comment_length'])


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
        CreatorFilter(c.logged_in_persona.id if c.logged_in_persona else '') # hack; anons should never see drafts
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

    # Normalize sort_fields into a list if needed
    if isinstance(sort_fields, basestring):
        sort_fields = sort_fields.split(",")

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
    @t_log(lambda f,a,k: "content search: "+str(k))
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
        @param comments_to  content_id of parent
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
        @comment AllanC if list='responses' - ",parent" is appended automatically to 'include_fields'
        """

        # Pre-process kwargs ---------------------------------------------------
        #
        # This must be done before caching - we assertain if private content can be shown to this user

        kwargs['_is_logged_in_as_creator'] = False # Setup placeholder kwargs for permissions options - this must be done because a cheeky user might try and pass them
        kwargs['_is_trusted_follower'    ] = False

        # Setup default search criteria
        if 'include_fields' not in kwargs:
            kwargs['include_fields'] = ""
            if 'creator' not in kwargs:
                kwargs['include_fields'] = "creator"
        if kwargs.get('list') == 'responses': # HACK - AllanC - mini hack, this makes the API behaviour slightly unclear, but solves a short term problem with creating response lists - it is common with responses that you have infomation about the parent
            kwargs['include_fields'] += ",parent"
        if 'sort' not in kwargs:
            kwargs['sort'] = '-update_date'

        # Split comma separted fields into lists
        for field in [field for field in ['include_fields', 'exclude_fields'] if isinstance(kwargs.get(field),basestring)]: #'sort' cannot be a list at this point because the list will be sorted by normalize_kwargs and the order of sort is important
            kwargs[field] = [i.strip() for i in kwargs[field].split(",")] # these will be sorted in normalization

        # Replace instances of 'me' with current username
        for key, value in kwargs.iteritems():
            if value == 'me':
                if c.logged_in_persona:
                    kwargs[key] = c.logged_in_persona # Member object will get normalized down to str in normalize for cache later
                else:
                    raise action_error(_("cannot refer to 'me' when not logged in"), code=400)

        creator = None

        try:
            # If displaying responses - Try to get the creator of the whole parent chain or creator of self
            # This models the same permission view enforcement as the 'show' private content API call
            if kwargs.get('response_to'):
                parent_root = get_content(kwargs['response_to'], is_viewable=True) # get_content will fail if current user does not have permission to view it
                parent_root = parent_root.root_parent or parent_root
                creator     = parent_root.creator
                kwargs['list'] = 'not_drafts' # AllanC - HACK!!! when dealing with responses to .. never show drafts ... there has to be a better when than this!!! :( sorry
                # AllanC note - 'creator' is compared against c.logged_in_persona later
        except Exception as e:
            user_log.exception("Error searching:") # AllanC - um? why is this in a genertic exception catch? if get_content fails then we want that exception to propergate

        if kwargs.get('creator'):
            creator = get_member(kwargs['creator'])
        
        if creator:
            if c.logged_in_persona == creator:
                kwargs['_is_logged_in_as_creator'] = True
            else:
                kwargs['_is_trusted_follower'    ] = creator.is_follower_trusted(c.logged_in_persona)


        # Create Cache key based on kwargs -------------------------------------
        
        kwargs = normalize_kwargs_for_cache(kwargs) # This str()'s all kwargs and gets id from any objects - and sorts any lists

        cache_key = ''
        if _filter:
            pass # We cant cache anything with a filter provided because we cant invalidate it afterwards because we cant identify the source
            #if _filter:
            #    cache_key += sql(_filter) # Create a string representation of the passed filters so that they form part of the cache key
        else:
            cache_key = get_cache_key('contents_index', kwargs)
        
        
        # Construct Query with provided kwargs ---------------------------------
        # Everything past here can be cached based on the kwargs state

        def contents_index(_filter=None, **kwargs):

            time_start = time()
            
            results = Session.query(Content).with_polymorphic('*') # TODO: list
            results = results.filter(Content.visible==True)
            # AllanC - not to sure about this comments addition. It would be nice to have it built with the filters? could this be moved down? thoughts?
            if kwargs.get('comments_to'):
                results = results.filter(Content.__type__=='comment')
            else:
                results = results.filter(Content.__type__!='comment')
    
            if kwargs['_is_logged_in_as_creator']:
                pass # allow private content
            else:
                if not kwargs['_is_trusted_follower']:
                    results = results.filter(Content.private==False) # public content only
                results = results.filter(Content.__type__!='draft') # Don't show drafts to anyone other than the creator
    
            # AllanC - Optimise joined loads - sub fields that we know are going to be used in the query return should be fetched when the main query fires
            for col in ['creator', 'attachments', 'tags', 'parent', 'license']:
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
                    'comments_to': ParentIDFilter  ,
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
                    parts.append(IDFilter([int(i) for i in kwargs['include_content'].split(',')]))
    
                if 'exclude_content' in kwargs and kwargs['exclude_content']:
                    parts.append(NotFilter(IDFilter([int(i) for i in kwargs['exclude_content'].split(',')])))
            except FilterException as fe:
                raise action_error(code=400, message=str(fe))
    
            feed = AndFilter(parts)
    
            # FIXME: these brackets are a hack, SQLAlchemy does "blah AND filter", not "(blah) AND (filter)",
            # so filter="x OR y" = "blah AND x OR y" = "(blah AND x) OR y"
            results = results.filter("("+sql(feed)+")")
            results = sort_results(results, kwargs.get('sort'))
            
            results = to_apilist(results, obj_type='contents', **kwargs)
            
            # hacky benchmarking just to get some basic idea of how each feed performs
            time_end = time()
            log.debug("Searching contents: %s [%f]" % (sql(feed), time_end - time_start))
    
            return results
        
        cache      = _cache.get('contents_index')
        cache_func = lambda: contents_index(_filter, **kwargs)
        if cache and cache_key:
            return cache.get(key=cache_key, createfunc=cache_func)
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
            #content.creator_id = c.logged_in_user.id          # Comments are always made by logged in user
            content.creator = c.logged_in_user
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
            #content.creator_id = c.logged_in_persona.id
            content.creator = c.logged_in_persona
        
        # GregM: Set private flag to user or hub setting (or public as default)
        #content.private = is_private
        
        parent = _get_content(int(kwargs.get('parent_id', 0)))
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
                    content_accept(id=parent.id)
                except action_error as ae:
                    if ae.original_dict.get('code') == 403:
                        raise ae
                    log.exception("Strange error while accepting")
                

        # comments are always owned by the writer; ignore settings and parent preferences
        if type == 'comment': #kwargs['type']
            content.parent_id = parent.id if parent else None # The validators take care of enforcing the permissions for response - the parent_id is set inadvance here because cache invalidation needs a parent_id and the flush below triggers this preparation, we cant determin if flushing or commitiing
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

        @param content_text_format the content fields can be in a varity of differnt formats. The dfault is 'html', this will clean the HTML down to allowed tags. 'markdown' can be used and will be converted to html

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
        if kwargs.get('type') == 'assignment' and not (content.creator if content.creator else get_member(content.creator_id)).can_publish_assignment():
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
                extra_fields = dict(content.extra_fields) #if content.extra_fields else {}
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
        
        # Process Content body format
        # AllanC - the content could be submitted in a varity of differnt text formats, by default it's html - that html requires cleaning - else convert input to html
        content_text_format = kwargs.get('content_text_format', 'html') if kwargs.get('content') else None
        if kwargs.get('type') or content.__type__ == 'comment':
            content.content == strip_html_tags(kwargs['content'])  # Comments have all formatting stripped reguardless
        elif content_text_format == 'html':
            content.content = clean_html_markup(kwargs['content']) # HTML is default input, clean it down to allowed tags
        elif content_text_format == 'markdown':
            content.content = markdown.markdown(kwargs['content']) # Markdown needs to be processsed to html
        
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
        media_caption_prefix = "media_caption_"
        media_credit_prefix  = "media_credit_"
        media_remove_prefix  = "file_remove_"
        # Check if media attachments need updating
        if substring_in([media_caption_prefix, media_credit_prefix, media_remove_prefix], kwargs.keys()): # AllanC - bit intesnsive, but content.attachments triggers a commit and query. This is an overhead we want to avoid.
            for media in content.attachments:
                # Update media item fields
                caption_key = "%s%d" % (media_caption_prefix, media.id)
                credit_key  = "%s%d" % (media_credit_prefix , media.id)
                if caption_key in kwargs:
                    media.caption = kwargs[caption_key]
                if credit_key in kwargs:
                    media.credit = kwargs[credit_key]
                # Remove media if required
                if "%s%d" % (media_remove_prefix, media.id) in kwargs:
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
        
        publishing_for_first_time = starting_content_type != content.__type__ or called_from_create_method
        
        if publishing_for_first_time:
            content.comments = [] # Clear comments when upgraded from draft to published content? we dont want observers comments 
        
        # -- Save to Database --------------------------------------------------
        Session.add(content)
        Session.commit()
        
        # -- Optional - abort with error after preserving draft ----------------
        # We raise any errors at the end because we still want to save any draft content even if the content is not published
        if error:
            user_log.info("Content #%d error updating \n %s" % (content.id, error))
            raise error
        
        # -- Log activity ------------------------------------------------------
        if publishing_for_first_time:
            user_log.info("Content #%d created/published" % (content.id, ))
        else:
            user_log.info("Content #%d updated"           % (content.id, ))
        
        # Queue Worker Jobs-- --------------------------------------------------
        def add_job(job_name, **kwargs):
            job_dict = {
                'task'    : job_name,
                'content' : content.id,
            }
            job_dict.update(kwargs)
            worker.add_job(job_dict)
        
        if submit_type=='publish' and permissions['can_publish'] and content.__type__ in publishable_types:
            if not content.private and config['feature.profanity_filter']:
                add_job('profanity_check', url_base=url('',qualified=True))
            # AllanC - GOD DAM IT!!! - we cant have the messages happening in the worker because we cant use the translation. This is ANOYING! I wanted the profanity filter to clean the content BEFORE messages were twittered out etc
            #          for now I have put it back inline .. but this REALLY needs sorting
            #add_job('content_notifications', publishing_for_first_time=publishing_for_first_time)
            from civicboom.worker.functions.content_notifications import content_notifications
            content_notifications(content, publishing_for_first_time=publishing_for_first_time)
            Session.commit() # AllanC - this is needed because the worker auto commits at the end .. running the method on it's own does not.
        
        if content.__type__ == 'comment':
            if config['feature.profanity_filter']:
                add_job('profanity_check', url_base=url('',qualified=True))
            add_job('content_notifications')
        
        
        # -- Redirect (if needed)-----------------------------------------------
        
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
        c.html_action_fallback_url = url(controller='profile', action='index')
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
        
        @param lists A comma separated list of lists to return with this call. Default 'comments, responses, contributors, actions, accepted_status'
        
        @return 200      page ok
                content  content object
        @return 403      permission denied
        @return 404      content not found
        
        @example https://test.civicboom.com/contents/1.json
        @example https://test.civicboom.com/contents/1.rss
        """
        # url('content', id=ID)
        
        if isinstance(kwargs.get('lists'), basestring):
            kwargs['lists'] = [list.strip() for list in kwargs['lists'].split(',')]
        if not isinstance(kwargs.get('lists'), type([])): # have to use type([]) because list is used below and python trys to pre-empt variable use
            kwargs['lists'] = [
                'comments',
                'responses',
                #'contributors',
                'actions', # AllanC - humm .. how can we cache this?
                'accepted_status',
            ]
        kwargs['lists'].sort()
        
        cache_key = gen_key_for_lists(['content']+kwargs['lists'], id, is_etag_master=True) # Get version numbers of all lists involved with this object and generate an eTag key - execution may abort here if the client eTag matches the one that this call generates
        # AllanC - the eTag here is not a security problem before .viewable_by because we are not transmitting any data, just an identifyer key
        # However viewers of an item of content will see the version numbers of the lists and know when something has changed - is this an issue? - we really want the call to terminate before any DB access is done if the eTag matchs
        
        # -- humm, --------
        
        content = get_content(id) #, is_viewable=True) # This is done manually below we needed some special handling for comments
        
        if content.__type__ == 'comment':
            if c.format == 'html' or c.format == 'redirect':
                return redirect(url('content', id=content.parent.id))
            if c.format == 'frag':
                content = content.parent # Bit of a HACK - if we try to read a content frag for a comment, just return the parent
        
        if not content.viewable_by(c.logged_in_persona):
            raise errors.error_view_permission()

        
        # Cache function return
        def contents_show(content, **kwargs):
            lists = kwargs.pop('lists')
            data = {'content':content.to_dict(list_type='full', **kwargs)}
            
            # AllanC - cant be imported at top of file because that creates a coupling issue
            from civicboom.controllers.content_actions import ContentActionsController
            content_actions_controller = ContentActionsController()
            
            for list in [list.strip() for list in lists]:
                if hasattr(content_actions_controller, list):
                    data[list] = getattr(content_actions_controller, list)(content.id, **kwargs)['data']['list']
            
            return action_ok(data=data)
        
        
        # -- These increments and state changes are invisible to the user the call is for .. it may be worth adding these as 'differed processs' to optimise the return time
        
        # Increase content view count
        # AllanC - we should move this to redis with a clever timeout or something
        if hasattr(content,'views'):
            content_view_key = 'content_%s' % content.id
            if not session_get(content_view_key):
                session_set(content_view_key, True)
                content.views += 1
                Session.commit()
                # AllanC - invalidating the content on EVERY view does not make scence
                #        - a cron should invalidate this OR the templates should expire after X time
                # This needs to be considered
        
        # Corporate plus customers want to be able to see what members have looked at an assignment
        if content.__type__=='assignment' and content.closed==True:
            member_assignment = get_assigned_to(content, member)
            if not member_assignment:
                return False
            if not member_assignment.member_viewed:
                member_assignment.member_viewed = True
                Session.commit()
            return True
        
        # Cache return
        cache      = _cache.get('contents_show')
        cache_func = lambda: contents_show(content, **kwargs)
        if cache and cache_key:
            return cache.get(key=cache_key, createfunc=cache_func)
        return cache_func()

