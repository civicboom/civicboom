"""
Content Controller

For managing content:
-creating/editing
-attaching media
-deleting
-flagging
"""

# Base controller imports
from civicboom.lib.base                import BaseController, render, c, redirect, url, request, abort, _, app_globals, flash_message
from civicboom.lib.authentication      import authorize, is_valid_user
from pylons import session

# Datamodel and database session imports
from civicboom.model.meta              import Session
from civicboom.model                   import Media
from civicboom.lib.database.get_cached import get_content, update_content, get_licenses

# Other imports
from civicboom.lib.civicboom_lib import form_post_contains_content, form_to_content, get_content_media_upload_key
from civicboom.lib.communication import messages


# Logging setup
import logging
log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")





class ContentController(BaseController):


    #-----------------------------------------------------------------------------
    # View
    #-----------------------------------------------------------------------------
    def view(self, id=None):
        """
        View content
        Differnt content object types require a different view template
        Identify the object type and render with approriate renderer
        """
        c.content = get_content(id)
        
        # Check content is visable
        if not c.content.editable_by(c.logged_in_user): #Always allow content to be viewed by owners/editors
            if c.content.status != "show":
                return render('/web/message/content_unavailable.mako')
        
        # Increase content view count
        if hasattr(c.content,'views'):
            content_view_key = 'content_%s' % c.content.id
            if content_view_key not in session:
                session[content_view_key] = True
                #session.save()
                c.content.views += 1
                Session.commit()
                # AllanC - invalidating the content on EVERY view does not make scence
                #        - a cron should invalidate this OR the templates should expire after X time
                #update_content(c.content)
        
        return render('/web/design09/content/content_view.mako')


    #-----------------------------------------------------------------------------
    # Edit
    #-----------------------------------------------------------------------------
    @authorize(is_valid_user)
    def edit(self, id=None):
        """
        Create or Edit new content with an editable HTML form
        """    
        
        if 'submit_delete' in request.POST:
            return redirect(url.current(action='delete', id=c.content.id))
        
        # Get exisiting content from URL id
        c.content = get_content(id)
        
        if c.content:
            # If the content is not being edited by the creator then "Unauthorised"
            # AllanC - todo: in future this will have to be a more involved process as the ower of the content could be a group the user is part of
            if not c.content.editable_by(c.logged_in_user):
                flash_message(_("your user does not have the permissions to edit this _content"))
                abort(401) #Unauthorised
            starting_content_type = c.content.__type__
        
        # Overlay form data over the current content object or return a new instance of an object
        c.content = form_to_content(request.POST, c.content)
        
        # If this is the frist time viewing the content then redirect to new substatiated id
        if id==None and c.content.id==None:
            Session.add(c.content)
            Session.commit()
            return redirect(url.current(action='edit', id=c.content.id))
        
        if 'submit_publish' in request.POST:
            if starting_content_type and starting_content_type != c.content.__type__:
                # Send notifications about NEW published content
                if   c.content.__type__ == "article"   : m = messages.article_published_by_followed(reporter=c.content.creator, article   =c.content)
                elif c.content.__type__ == "assignment": m = messages.assignment_created           (reporter=c.content.creator, assignment=c.content)
                # TODO: Clear comments when upgraded from draft to published content?
                user_log.info("published new Content #%d" % (c.content.id, ))
            else:
                # Send notifications about previously published content has been UPDATED
                if   c.content.__type__ == "assignment": m = messages.assignment_updated           (reporter=c.content.creator, assignment=c.content)
                user_log.info("updated published Content #%d" % (c.content.id, ))
            if m:
                c.content.creator.send_message_to_followers(m, delay_commit=True)
        
        # If form contains post data
        if request.POST:
            # AllanC - This was an idea that if the content has not changed then dont commit it, but for now it is simpler to always commit it
            #content_hash_before = c.content.hash() # Generate hash of content
            #content_hash_after  = "always trigger db commit on post" #c.content.hash()                # Generate hash of content again
            #if content_hash_before != content_hash_after:         # If content has changed
            Session.add(c.content)                            #   Save content to database
            Session.commit()                                  #
            update_content(c.content)                         #   Invalidate any cache associated with this content
            user_log.info("edited Content #%d" % (c.content.id, )) # todo - move this so we dont get duplicate entrys with the publish events above 
            
            if 'submit_publish' in request.POST or 'submit_preview' in request.POST:
                return redirect(url.current(action='view', id=c.content.id))
            if 'submit_response' in request.POST:
                return redirect(url.current(action='view', id=c.content.parent_id))
        
        c.content_media_upload_key = get_content_media_upload_key(c.content)
        
        c.licenses = get_licenses() # WTF! without this line ... using app_globals.licences in the template does not work! why?
        # Render content editor
        return render("/web/content_editor/content_editor.mako")
        

    #-----------------------------------------------------------------------------
    # Add Media
    #-----------------------------------------------------------------------------
    #@authorize(is_valid_user)
    def upload_media(self, id=None):
        """
        With javascript/flash additional media can be uploaded individually
        There is no need to enforce session or cookie for identification because the media upload key should be provided in the URL to identify the user/content
        """
        if request.environ['REQUEST_METHOD']!='POST': return 
        id = app_globals.memcache.get(str(id))
        if not id: return
        
        form = request.POST
        if 'Filedata' in form and form['Filedata'] != "":
            form_file     = form["Filedata"]
            media = Media()
            media.load_from_file(tmp_file=form_file, original_name=form_file.filename)
            media.sync()
            #media.content_id = id # This does not work because the database complains about orphan records :(, it feels unnessisary to 
            get_content(id).attachments.append(media)
            Session.add(media)
            Session.commit()
            update_content(id)
            #user_log.info("media appended to content #%d" % (id, )) # Update user log # err no user identifyable here


    #-----------------------------------------------------------------------------
    # Delete
    #-----------------------------------------------------------------------------
    @authorize(is_valid_user)
    def delete(self, id):
        c.content = get_content(id)
        if not c.content.editable_by(c.logged_in_user):
            flash_message(_("your current user does not have the permissions to delete this _content"))
            #AllanC: todo - this message never gets seen as the session is not
            abort(401)
        flash_message(_("_content deletion is not implemented yet"))
        return redirect(request.environ.get('HTTP_REFERER'))


    #-----------------------------------------------------------------------------
    # Flag
    #-----------------------------------------------------------------------------
    @authorize(is_valid_user)
    def flag(self, id):
        """
        Flag this content as being inapproprate of copyright violoation
        """
        pass
