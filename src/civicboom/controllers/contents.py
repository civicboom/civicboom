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

# Other imports
from civicboom.lib.civicboom_lib import form_post_contains_content, form_to_content, get_content_media_upload_key, profanity_filter, twitter_global
from civicboom.lib.communication import messages
from civicboom.lib.helpers          import call_action


# Logging setup
log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")

#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------


index_lists = {
    'content'             : lambda member: member.content ,
    'assignments_active'  : lambda member: member.content_assignments_active ,
    'assignments_previous': lambda member: member.content_assignments_previous,
    'assignments'         : lambda member: member.content_assignments ,
    'articles'            : lambda member: member.content_articles ,
    'drafts'              : lambda member: member.content_drafts ,
}

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
        if not content.viewable_by(c.logged_in_user): 
            raise action_error(_("_content not viewable"), code=403)
        if content.__type__ == "comment":
            user_log.debug("Attempted to view a comment as an article")
            raise action_error(_("_content not found"), code=404)
    if is_editable and not content.editable_by(c.logged_in_user):
        raise action_error(_("You do not have permission to edit this _content"), code=403)
    if is_parent_owner and not content.is_parent_owner(c.logged_in_user):
        raise action_error(_("not parent owner"), code=403)
    return content


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

    @auto_format_output()
    @web_params_to_kwargs
    @authorize(is_valid_user)
    def index(self, **kwargs):
        """
        GET /contents: All items in the collection

        @api contents 1.0 (WIP)

        @param list what type of contents to return, possible values:
          content
          assignments_active
          assignments_previous
          assignments
          articles
          drafts

        @return 200    list generated ok
                list   array of content objects
        """
        # url('contents')
        if 'list' not in kwargs:
            kwargs['list'] = 'content'
        if 'exclude_fields' not in kwargs:
            kwargs['exclude_fields'] = 'creator'
        
        list = kwargs['list']
        if list not in index_lists:
            raise action_error(_('list type %s not supported') % list, code=400)
            
        contents = index_lists[list](c.logged_in_user)
        contents = [content.to_dict(**kwargs) for content in contents]
        
        return action_ok(data={'list': contents})


    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def create(self, format=None):
        """
        POST /contents: Create a new item

        @api contents 1.0 (WIP)

        @param form_title
        @param form_contents
        @param form_type
        @param ...

        @return 201   content created
                id    new content id
        @return 400   missing data (ie, a type=comment with no parent_id)
        @return 403   can't reply to parent
        @return 404   parent not found

        @comment Shish paramaters need filling out
        @comment Shish do all the paramaters need to start with "form_"?
        @comment Allan   no need for all params to start with "form_" this was a leftover from the first prototype, they can be removed
        """
        # url('contents') + POST
        
        # if parent is specified, make sure it is valid
        if 'form_parent_id' in request.params:
            parent = get_content(request.params['form_parent_id'])
            if not parent:
                raise action_error(message='parent not found', code=404)
            if not parent.viewable_by(c.logged_in_user):
                raise action_error(code=403)
        
        # if type is comment, it must have a parent
        if request.params.get('form_type') == "comment" and 'form_parent_id' not in request.params:
            raise action_error(code=400)
        
        content = form_to_content(request.params, None)
        Session.add(content)
        Session.commit()
        return action_ok(message=_(' _content created ok'), data={'id':content.id}, code=201)


    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def new(self):
        """
        GET /contents/new: Form to create a new item

        As file-upload and such require an existing object to add to,
        we create a blank object and redirect to "edit-existing" mode
        """
        #url_for('new_content')
        content_id = call_action(ContentsController().create, format='python')['data']['id']
        return redirect(url('edit_content', id=content_id))


    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def update(self, id):
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
        
        # AllanC - Publish Permission placeholder for groups
        #          We need to not only know the current user persona, but also the role of that current persona e.g - might be logged in as EvilCorp but only as a 'contributor' or 'observer'
        #if 'submit_publish' in request.POST and :
        #    raise action_error(_("You do not have permission to publish this _content"), code=403)
        
        # Overlay form data over the current content object or return a new instance of an object
        content = form_to_content(request.params, content) #request.POST
        starting_content_type = content.__type__
        
        # If publishing perform profanity check and send notifications
        if 'submit_publish' in request.POST:
            profanity_filter(content) # Filter any naughty words and alert moderator
            
            m = None
            if starting_content_type and starting_content_type != content.__type__:
                # Send notifications about NEW published content
                if   content.__type__ == "article"   : m = messages.article_published_by_followed(reporter=content.creator, article   =content)
                elif content.__type__ == "assignment": m = messages.assignment_created           (reporter=content.creator, assignment=content)
                # TODO: Clear comments when upgraded from draft to published content?
                user_log.info("published new Content #%d" % (content.id, ))
                # Aggregate new content
                content.aggregate_via_creator() # Agrigate content over creators known providers
                twitter_global(content) # TODO? diseminate new or updated content?
            else:
                # Send notifications about previously published content has been UPDATED
                if   content.__type__ == "assignment": m = messages.assignment_updated           (reporter=content.creator, assignment=content)
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
        
        content_message  = None
        content_redirect = url('edit_content', id=content.id)
        
        if 'submit_preview' in request.POST:
            content_redirect = url('content', id=content.id)
        if 'submit_publish' in request.POST:
            content_redirect = url('content', id=content.id, prompt_aggregate=True)
        if 'submit_response' in request.POST:
            content_redirect = url('content', id=content.parent_id)
        
        if c.format == 'redirect':
            return redirect(content_redirect)
            
        return action_ok(_("_content updated"))


    @auto_format_output()
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


    @auto_format_output()
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
            template = 'design09/content/view',
            data     = {'content':content.to_dict(**kwargs)}
        )


    @auto_format_output()
    @authorize(is_valid_user)
    def edit(self, id, format='html'):
        """
        GET /contents/{id}/edit: Form to edit an existing item
        """
        # url('edit_content', id=ID)
        
        c.content = _get_content(id, is_editable=True)
        
        c.content                  = form_to_content(request.params, c.content)
        c.content_media_upload_key = get_content_media_upload_key(c.content)
        
        return render("/web/content_editor/content_editor.mako")

