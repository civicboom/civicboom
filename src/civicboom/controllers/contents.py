# Base controller imports
from civicboom.lib.base import *

# Datamodel and database session imports
from civicboom.model                   import Media, Content, CommentContent, DraftContent, CommentContent, ArticleContent, AssignmentContent, Boom, UserVisibleContent
from civicboom.lib.database.get_cached import update_content, get_license, get_tag, get_assigned_to, get_content as _get_content
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
    title       = civicboom.lib.form_validators.base.ContentUnicodeValidator(not_empty=True, strip=True, max=250, min=2, html='strip_html_tags')
    content     = civicboom.lib.form_validators.base.ContentUnicodeValidator()
    parent_id   = civicboom.lib.form_validators.base.ContentObjectValidator(not_empty=False)
    location    = civicboom.lib.form_validators.base.LocationValidator(not_empty=False)
    private     = civicboom.lib.form_validators.base.PrivateContentValidator(not_empty=False) #formencode.validators.StringBool(not_empty=False)
    license_id  = civicboom.lib.form_validators.base.LicenseValidator(not_empty=False)
    creator_id  = civicboom.lib.form_validators.base.MemberValidator(not_empty=False) # AllanC - debatable if this is needed, do we want to give users the power to give content away? Could this be abused?
    #tags        = civicboom.lib.form_validators.base.ContentTagsValidator(not_empty=False) # not needed, handled by update method
    # Draft Fields
    target_type = formencode.validators.OneOf(content_types.enums, not_empty=False)
    # Assignment Fields
    due_date    = civicboom.lib.form_validators.base.IsoFormatDateConverter(not_empty=False)
    event_date  = civicboom.lib.form_validators.base.IsoFormatDateConverter(not_empty=False)
    default_response_license_id  = civicboom.lib.form_validators.base.LicenseValidator(not_empty=False)
    # TODO: need date validators to check date is in future (and not too far in future as well)


class ContentCommentSchema(ContentSchema):
    parent_id   = civicboom.lib.form_validators.base.ContentObjectValidator(not_empty=True, empty=_('comments must have a valid parent'))
    content     = civicboom.lib.form_validators.base.ContentUnicodeValidator(not_empty=True, empty=_('comments must have content'), max=config['setting.content.max_comment_length'], html='strip_html_tags')


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
        parts = []
        for word in text.split():
            word = re.sub("[^a-zA-Z0-9_-]", "", word)
            if word:
                parts.append(word)

        if parts:
            text = " | ".join(parts)
            return query.filter("""
                to_tsvector('english', title || ' ' || content) @@
                to_tsquery(:text)
            """).params(text=text)
        else:
            return query
    
    def append_search_location(query, location):
        (lon, lat, radius) = (None, None, 10)
        zoom = 10 # FIXME: inverse of radius? see bug #50
        
        if isinstance(location, basestring):
            location = location.replace(",", " ")
            location_tuple = [i.strip() for i in location.split()]
            if   len(location_tuple) == 2:
                (lon, lat        ) = location_tuple
            elif len(location_tuple) == 3:
                (lon, lat, radius) = location_tuple
        else:
        #if isinstance(location, Point):
            log.warn('location search with objects is not implemented yet')
        
        if lon and lat and radius:
            query = query.add_columns(func.st_distance(Content.location, 'POINT(%d %d)' % (float(lon), float(lat))).label("distance"))
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
        try:
            content_id = int(content_id)
        except:
            raise action_error('response_to must be an integer')
        return query.filter(Content.parent_id==content_id).filter(or_(Content.__type__!='article', and_(Content.__type__=='article', ArticleContent.approval != 'dissassociated')))

    def append_search_boomed_by(query, member):
        member = normalize_member(member)
        #return query.filter(Boom.member_id==member) #join(Member.boomed_content, Boom)
        return query.filter(Content.id.in_(Session.query(Boom.content_id).filter(Boom.member_id==member)))

    def append_search_before(query, date):
        if isinstance(date, basestring):
            date = parse_date(date, dayfirst=True).strftime("%d/%m/%Y")
        return query.filter(Content.update_date <= date)
    
    def append_search_after(query, date):
        if isinstance(date, basestring):
            date = parse_date(date, dayfirst=True).strftime("%d/%m/%Y")
        return query.filter(Content.update_date >= date)
        
    def append_exclude_content(query, ids):
        if isinstance(ids, basestring):
            ids = [int(id) for id in ids.split(',')]
        return query.filter(~Content.id.in_(ids))

    search_filters = {
        'id'             : append_search_id          ,
        'creator'        : append_search_creator     ,
        'term'           : append_search_text        ,
        'location'       : append_search_location    ,
        'type'           : append_search_type        ,
        'response_to'    : append_search_response_to ,
        'boomed_by'      : append_search_boomed_by   ,
        'before'         : append_search_before      ,
        'after'          : append_search_after       ,
        'exclude_content': append_exclude_content    ,
    }
    
    return search_filters

search_filters = _init_search_filters()


list_filters = {
    'all'                 : lambda results: results ,
    'assignments_active'  : lambda results: results.filter(Content.__type__=='assignment').filter(or_(AssignmentContent.due_date>=now(),AssignmentContent.due_date==null())) ,
    'assignments_previous': lambda results: results.filter(Content.__type__=='assignment').filter(or_(AssignmentContent.due_date< now())) ,
    'assignments'         : lambda results: results.filter(Content.__type__=='assignment') ,
    'drafts'              : lambda results: results.filter(Content.__type__=='draft').filter(Content.creator == c.logged_in_persona) ,
    'articles'            : lambda results: results.filter(and_(Content.__type__=='article', ArticleContent.parent_id==null())),
    'responses'           : lambda results: results.filter(and_(Content.__type__=='article', ArticleContent.parent_id!=null())),
    'not_drafts'          : lambda results: results.filter(Content.__type__!='draft'),
}


def sqlalchemy_content_query(include_private=False, trusted_follower= False, **kwargs):
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
        if not trusted_follower:
            results = results.filter(Content.private==False) # public content only
        results = results.filter(Content.__type__!='draft')
    
    if 'creator' in kwargs.get('include_fields',[]):
        #results = results.options(joinedload('creator'))
        results = results.options(joinedload(Content.creator))
    
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

    
    @web
    def index(self, union_query=None, **kwargs):
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
        @param response_to  content_id of parent
        @param boomed_by    username or user_id of booming user
        @param before       update date before "%d/%m/%Y"
        @param after        update date after  "%d/%m/%Y"
        @param exclude_content a list of comma separated content id's to exclude from the content returned
        @param private      if set and creator==logged_in_persona both public and private content will be returned
        @param sort         comma separated list of fields, prefixed by '-' for decending order (default) '-update_date'
        @param * (see common list return controls)
        
        @return 200      list ok
            list list of content objects
        
        @example https://test.civicboom.com/contents.json?creator=unittest&limit=2
        @example https://test.civicboom.com/contents.rss?list=assignments_active&limit=2
        @example https://test.civicboom.com/contents.json?limit=1&list_type=empty&include_fields=id,views,title,update_date&exclude_fields=creator
        
        @comment AllanC use 'include_fields=attachments' for media
        @comment AllanC if 'creator' not in params or exclude list then it is added by default to include_fields:
        
        """
        # url('contents')
        
        # Permissions
        # AllanC - to aid cacheing we need permissions to potentially be a decorator
        #          TODO: we need maybe a separte call, or something to identify a private call
        trusted_follower  = False
        logged_in_creator = False
        creator = None
        try:
            # Try to get the creator of the whole parent chain or creator of self
            # This models the same permission view enforcement as the 
            parent_root = get_content(kwargs['response_to'])
            parent_root = parent_root.root_parent or parent_root
            creator = parent_root.creator
            kwargs['list'] = 'not_drafts' # AllanC - HACK!!! when dealing with responses to .. never show drafts ... there has to be a better when than this!!! :( sorry
        except:
            pass
        try:
            creator = get_member(kwargs['creator'])
            kwargs['creator'] = normalize_member(creator) # normalize creator param for search
        except:
            pass
        
        if creator:
            #if c.logged_in_persona and kwargs['creator'] == c.logged_in_persona.id:
            if c.logged_in_persona == creator:
                logged_in_creator = True
            else:
                trusted_follower = creator.is_follower_trusted(c.logged_in_persona)
        # If we've gone though the hassle of identifying if this is actually the user then show the private content ... this may not be the correct way, we may want to see always default to public .. need to consider
        if trusted_follower or logged_in_creator:
            kwargs['private'] = True
        
        
        # Location - 'me' - replace 'me' with current location
        # NOTE: Cache warning! this is not a public cacheable item
        if kwargs.get('location') == 'me':
            location = None
            if c.logged_in_persona:
                location = c.logged_in_persona.location_home
            if hasattr(c.logged_in_persona, 'location_current') and c.logged_in_persona.location_updated > now() - datetime.timedelta(days=2):
                location = c.logged_in_persona.location_current
            if location:
                kwargs['location'] = location
            else:
                return to_apilist(None, obj_type='content', **kwargs) # AllanC - if no location and 'me' specifyed return nothing as it would be confising to return seeming random content
        
        # --- the below should be publicly cacheable ---
        
        # Setup search criteria
        if 'include_fields' not in kwargs:
            kwargs['include_fields'] = ""
        if 'exclude_fields' not in kwargs:
            kwargs['exclude_fields'] = ""
            
        # Defaults
        if 'creator' not in kwargs and 'creator' not in kwargs['exclude_fields']:
            kwargs['include_fields'] += ",creator"
            kwargs['exclude_fields'] += ",creator_id"
        # HACK - AllanC - mini hack, this makes the API behaviour slightly unclear, but solves a short term problem with creating response lists - it is common with responses that you have infomation about the parent
        if kwargs.get('list') == 'responses':
            kwargs['include_fields'] += ",parent"
        
        
        # AllanC - TEMP HACK!!!!! the line below means a trusted follower can see drafts!! this is NOT the correct behaviour.
        #include_private_content = 'private' in kwargs and (logged_in_creator or trusted_follower)
        results = sqlalchemy_content_query(include_private = logged_in_creator, trusted_follower=trusted_follower, **kwargs)

        if union_query:
            results = results.union(union_query)

        # union and add_column are mutually exclusive; union is functional while
        # add_column is visual, so disable add_column if union is there
        #if not union_query:
        #    if 'term' in kwargs:
        #        results = results.add_column(
        #            func.ts_headline('pg_catalog.english',
        #                func.strip_tags(Content.content),
        #                func.plainto_tsquery(kwargs['term']),
        #                'MaxFragments=3, FragmentDelimiter=" ... ", StartSel="<b>", StopSel="</b>", MinWords=7, MaxWords=15',
        #                type_= Unicode
        #            )
        #        )
        #    else:
        #        results = results.add_column(
        #            func.substr(func.strip_tags(Content.content), 0, 100)
        #        )

        for sort_field in kwargs.get('sort', '-update_date').split(','):
            direction = asc
            if sort_field[0] == "-":
                direction = desc
                sort_field = sort_field[1:]

            if sort_field in [col["name"] for col in results.column_descriptions]:
                results = results.order_by(direction(sort_field))
        
#        def merge_snippet(content, snippet):
#            content = content.to_dict(**kwargs)
#            content['content_short'] = snippet
#            return content

        #if not union_query:
        #    results = [merge_snippet(co, sn) for co, sn in results]

        return to_apilist(results, obj_type='content', **kwargs)


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
                content = morph_content_to(content, kwargs['type'])
        
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
        # AllanC - not used yet .. but could be in future
        for extra_field in []:
            if extra_field in kwargs: # AllanC - could these have validators at somepoint?
                content.extra_fields[extra_field] = kwargs[extra_field]
        
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
        
        # -- Save to Database --------------------------------------------------
        Session.add(content)
        Session.commit()
        update_content(content)  # Invalidate any cache associated with this content
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
