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

# Logging setup
log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class ContentsController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('content', 'contents')


    def index(self, format='html'):
        """GET /contents: All items in the collection"""
        # url('contents')
        return redirect(url(controller='search', action='content'))


    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def create(self, format=None):
        """POST /contents: Create a new item"""
        # url('contents') + POST

        # if parent is specified, make sure it is valid
        if 'form_parent_id' in request.params:
            parent = get_content(request.params['form_parent_id'])
            if not parent:
                return action_error(code=404)
            if not parent.viewable_by(c.logged_in_user):
                return action_error(code=403)

        # if type is comment, it must have a parent
        if request.params.get('form_type') == "comment" and 'form_parent_id' not in request.params:
            return action_error(code=400)

        content = form_to_content(request.params, None)
        Session.add(content)
        Session.commit()
        return action_ok(message=_(' _content created ok'), data={'id':content.id}, code=201)


    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def new(self, format='html'):
        """GET /contents/new: Form to create a new item
        As file-upload and such require an existing object to add to, we create a blank object and redirect to "edit-existing" mode
        """
        #url_for('new_content')
        content_id = self.create(format='python')['data']['id']
        return redirect(url('edit_content', id=content_id))


    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def update(self, id):
        """PUT /contents/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('content', id=ID),
        #           method='put')
        # url('content', id=ID)
        
        content = get_content(id)
        
        if not content:
            return action_error(_("_content not found"), code=404)

        if not c.content.editable_by(c.logged_in_user):
            return action_error(_("You do not have permission to edit this _content"), code=403)

        # Overlay form data over the current content object or return a new instance of an object
        content = form_to_content(request.params, c.content) #request.POST
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
        #content_hash_before = c.content.hash() # Generate hash of content
        #content_hash_after  = "always trigger db commit on post" #c.content.hash()                # Generate hash of content again
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
    def delete(self, id, format="html"):
        """DELETE /contents/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('content', id=ID),
        #           method='delete')
        # url('content', id=ID)
        content = get_content(id)
        if not content:
            return action_error(_("_content not found"), code=404)
        if not content.editable_by(c.logged_in_user):
            return action_error(_("your current user does not have the permissions to delete this _content"), code=403)
        content.delete()
        return action_ok(_("_content deleted"), code=200)


    @auto_format_output()
    def show(self, id, format='html'):
        """GET /contents/id: Show a specific item"""
        # url('content', id=ID)
        """
        View content
        Differnt content object types require a different view template
        Identify the object type and render with approriate renderer
        """
        c.content = get_content(id)

        if not c.content:
            return action_error(_("_content not found"), code=404)

        # Check content is visable
        if c.content.__type__ == "comment":
            user_log.debug("Attempted to view a comment as an article")
            return action_error(_("_content not found"), code=404)
        if not c.content.editable_by(c.logged_in_user): #Always allow content to be viewed by owners/editors
            if c.content.status == "pending":
                user_log.debug("Attempted to view someone else's pending content")
                return action_error(_("_content not found"), code=404)
                #c.error_message = _("your user does not have the permissions to view this _content")
                #return render('/web/design09/content/unavailable.mako')

        # Increase content view count
        if hasattr(c.content,'views'):
            content_view_key = 'content_%s' % c.content.id
            if session_get(content_view_key):
                session_set(content_view_key, True)
                #session.save()
                c.content.views += 1
                Session.commit()
                # AllanC - invalidating the content on EVERY view does not make scence
                #        - a cron should invalidate this OR the templates should expire after X time
                #update_content(c.content)

        return action_ok(
            template='design09/content/view',
            data={
                "content": c.content,
                "author": c.content.creator
            }
        )


    @authorize(is_valid_user)
    def edit(self, id, format='html'):
        """GET /contents/id/edit: Form to edit an existing item"""
        # url('edit_content', id=ID)

        # Get exisiting content from URL id
        c.content = get_content(id)
        if not c.content:
            return action_error(_("_content not found"), code=404)

        c.content = form_to_content(request.params, c.content)

        #if c.content:
        # If the content is not being edited by the creator then "Unauthorised"
        # AllanC - todo: in future this will have to be a more involved process as the ower of the content could be a group the user is part of
        if not c.content.editable_by(c.logged_in_user):
            return action_error(_("your user does not have the permissions to edit this _content"), code=403)
        
        c.content_media_upload_key = get_content_media_upload_key(c.content)

        #c.licenses = get_licenses() # WTF! without this line ... using app_globals.licences in the template does not work! why?
        # Render content editor
        #if id and c.content.id and id != c.content.id: redirect(url.current(id=c.content.id))
        
        return render("/web/content_editor/content_editor.mako")


    def get_media_processing_staus(self, id):
        """
        Javascript can poll this method to get progress updates on the media processing
        Currently only return a flag to state if processing it taking place,
        but could be improved to return aditional progress info.
        """
        stat = app_globals.memcache.get(str("media_processing_"+id))
        return action_ok(data=stat)
