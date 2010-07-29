"""
Content Controller

For managing content:
-creating/editing
-attaching media
-deleting
-flagging
"""

# Base controller imports
from civicboom.lib.base                import BaseController, render, c, redirect, url, request, abort, _, app_globals
from civicboom.lib.misc                import flash_message
from civicboom.lib.authentication      import authorize, is_valid_user

# Datamodel and database session imports
from civicboom.model                   import DraftContent, Media, Tag
from civicboom.model.meta              import Session
from civicboom.lib.database.get_cached import get_content, get_tag, get_licenses
from civicboom.lib.database.get_cached import update_content

# Other imports
from civicboom.lib.text import clean_html_markup
from civicboom.lib.misc import remove_where


from sets import Set # may not be needed in Python 2.7+
import hashlib
import random


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
                session.save()
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
        
        c.licenses = get_licenses() # Temp botch for licenses being passed to template, was in app_globals but moved it
        
        
        #------------------------------
        # Form POST contains Content
        #------------------------------
        # AllanC - is there a way this can be placed at the end of the file away from the rest of the edit action for clarity?
        def form_post_contains_content(form):
            """
            Check if a range of required fields are not null
            """
            return_bool = False
            if form:
                for field in ("title","content","media_file"):
                    if form["form_"+field]:
                        return_bool = True
            return return_bool
          

        
        #------------------------------
        # Form POST to Content Object
        #------------------------------
        # AllanC - is there a way this can be placed at the end of the file away from the rest of the edit action for clarity?
        def form_to_content(form, content):
            """
            Takes form post data and either overlays the form with an existing object or create the relevent content object type and overlay form data
            Will never return None - will always return at leist an empty content object
            """
            if not form   : return content #If there is no form data there is nothing to overlay or do
            if not content:
                content = DraftContent()
            
            # for key in form: print "%s:%s" % (key,form[key])
            
            # from most form values we need to escape '"' and "'" characters as these are used in HTML alt tags and value tags
            
            # Content
            if "form_content" in form:
                content.content = clean_html_markup(form["form_content"])

            # Owner
            if "form_owner" in form:
                c.content.creator_id = form["form_owner"]
                # Although the form limits the user to a selectable list, any id can be passed here, it is possible that with an API call a user can give content to anyone.

            # Tags
            if "form_tags" in form:
                form_tags    = [tag for tag in form["form_tags"].split(" ") if tag!=""] # Get tags from form removing any empty strings
                content_tags = [tag.name for tag in c.content.tags]                     # Get tags form current content object
                
                # Add any new tag objects
                for tag in Set(form_tags).difference(content_tags):
                    c.content.tags.append(get_tag(tag))

                # Remove any missing tag objects
                def remove_check(tag):
                    return tag.name in Set(content_tags).difference(form_tags)
                remove_where(c.content.tags, remove_check)

            # Existing Media Form Fields
            for media in content.attachments:
                # Update media item fields
                caption_key = "form_media_caption_%d" % (media.id)
                if caption_key in form:
                    media.caption = form[caption_key]
                credit_key = "form_media_credit_%d"   % (media.id)
                if credit_key in form:
                    media.credit = form[credit_key]
                # Remove media if required
                if "form_file_remove_%d" % media.id in form:
                    content.attachments.remove(media)

            # Add Media - if file present in form post
            if 'form_media_file' in form and form['form_media_file'] != "":
                form_file     = form["form_media_file"]
                media = Media()
                media.load_from_file(tmp_file=form_file, original_name=form_file.filename, caption=form["form_media_caption"], credit=form["form_media_credit"])
                media.sync()
                content.attachments.append(media)
                #Session.add(media)
            
            if 'form_licence' in form:
                content.license_id = form['form_licence']
                
            for field in ["title"]:
                setattr(content,field,form["form_"+field])

            return content

        #------------------------------------------------
        # Edit Content Main
        #------------------------------------------------
        
        # Get exisiting content from URL id
        c.content = get_content(id)
        
        # If the content is None then create a blank content object
        #  This saves unnessisary null checking in template
        if c.content==None:
            c.content         = DraftContent()
            c.content.creator = c.logged_in_user

        if 'submit_delete' in request.POST:
            return redirect(url.current(action='delete', id=c.content.id))

        # If the content is not being edited by the creator then "Unauthorised"
        # AllanC - todo: in future this will have to be a more involved process as the ower of the content could be a group the user is part of
        if not c.content.editable_by(c.logged_in_user):
            flash_message(_("your user does not have the permissions to edit this _content"))
            abort(401) #Unauthorised

        # If form contains post data
        if form_post_contains_content(request.POST):
            content_hash_before = c.content.hash()                # Generate hash of content
            c.content = form_to_content(request.POST, c.content)  # Overlay form data over the current content object
            content_hash_after  = "always trigger db commit on post" #c.content.hash()                # Generate hash of content again
            if content_hash_before != content_hash_after:         # If content has changed
                Session.add(c.content)                            #   Save content to database
                Session.commit()                                  #
                update_content(c.content)                         #   Invalidate any cache associated with this content
                user_log.info("edited Content #%d" % (c.content.id, )) # Update user log

            # if record type changed
            #  remove previous record?
            #  redirect to new id

            if 'submit_publish' in request.POST or 'submit_preview' in request.POST:
                return redirect(url.current(action='view', id=c.content.id))
                
        # If this is the frist time saving the content then redirect to new substatiated id
        if id==None and c.content.id:
            return redirect(url.current(action='edit', id=c.content.id))

        # Generate tempory content unique key in memcache for additional media appends from flash or javascript
        def get_content_key(content):
            """
            Generate/Get a tempory key associated with this content
            The tempory key stays active for "x" minuets in memcache (so page reloads can refer to the same key)
            The key is used for file uploads from sources that cannot send the authentication cookie each time
            """
            content_id_key  = "content_upload_%d" % content.id
            memcache_expire = 60*60 # memcache expire time in seconds 60*60 = 1 Hour
            mc              = app_globals.memcache
            key             = mc.get(content_id_key)
            if not key:
                key = hashlib.md5(str(random.random())).hexdigest()
                mc.set(content_id_key,             key, time=memcache_expire)
                mc.set(key           , str(content.id), time=memcache_expire)
            return key

        c.content_media_upload_key = get_content_key(c.content)

        # Render content editor
        return render("/web/content_editor/content_editor.mako")
        

    #-----------------------------------------------------------------------------
    # Add Media
    #-----------------------------------------------------------------------------
    #@authorize(is_valid_user)
    def upload_media(self, id=None):
        """
        With javascript/flash additional media can be uploaded individually
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