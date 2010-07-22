"""
Content Controller

For managing content:
-creating/editing
-attaching media
-deleting
-flagging
"""

from civicboom.lib.base                import BaseController, render, c, redirect, url, request, abort
from civicboom.lib.misc                import flash_message
from civicboom.lib.database.get_cached import get_content
from civicboom.lib.authentication      import authorize, is_valid_user

from civicboom.model.content           import DraftContent

from civicboom.model.meta import Session

import logging
log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")

this_controller_name = __name__.split(".")[2] #Could get this from current request? so no need to store in a var or get it in a hacky way like this?

prefix = "/web/content_editor/"


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
        return "implement content render template"

    #-----------------------------------------------------------------------------
    # Edit
    #-----------------------------------------------------------------------------
    @authorize(is_valid_user)
    def edit(self, id=None):
        """
        Create or Edit new content with an editable HTML form
        """
        
        #------------------------------
        # Form POST to Content Object
        #------------------------------
        def form_to_content(form, content):
            """
            Takes form post data and either overlays the form with an existing object or create the relevent content object type and overlay form data
            Will never return None - will always return at leist an empty content object
            """
            if not form   : return content #If there is no form data there is nothing to overlay or do
            if not content:
                content = DraftContent()
            
            #for key in form: print "%s:%s" % (key,form[key])
            
            for field in ("title","content"):
                setattr(content,field,form["form_"+field])
            
            return content
        
            #commit content update with data from form
            # save media
            # if record type changed
            #  remove previous record
            #  redirect to new id
            
        # Get exisiting content from URL id
        c.content = get_content(id)
        
        # If the content is None then create a blank content object
        #  This saves unnessisary null checking in template
        if c.content==None:
            c.content         = DraftContent()
            c.content.creator = c.logged_in_user
        
        # If the content is not being edited by the creator then "Unauthorised"
        # AllanC - todo: in future this will have to be a more involved process as the ower of the content could be a group the user is part of
        if c.content.creator != c.logged_in_user:
            abort(401)

        # If form contains post data
        if request.POST:
            content_hash_before = c.content.hash()                # Generate hash of content
            c.content = form_to_content(request.POST, c.content)  # Overlay form data over the current content object
            content_hash_after  = c.content.hash()                # Generate hash of content again
            if content_hash_before != content_hash_after:         # If content has changed
                Session.add(c.content)                            #   Save content to database
                Session.commit()
                user_log.info("edited Content #%d" % (c.content.id, )) # Update user log

            #submit_action = request.POST['submit']
            if 'submit_publish' in request.POST or 'submit_preview' in request.POST:
                return redirect(url(controller=this_controller_name, action='view', id=c.content.id))
                
        # If this is the frist time saving the content then redirect to new substatiated id
        if id==None and c.content.id:
            return redirect(url(controller=this_controller_name, action='edit', id=c.content.id))

        # Render content editor
        return render(prefix + "content_editor.mako")

    #-----------------------------------------------------------------------------
    # Add Media
    #-----------------------------------------------------------------------------
    def upload_media(self, id):
        """
        With javascript additional media can be uploaded individually
        """
        pass

    #-----------------------------------------------------------------------------
    # Delete
    #-----------------------------------------------------------------------------
    def delete(self, id):
        pass

    #-----------------------------------------------------------------------------
    # Flag
    #-----------------------------------------------------------------------------
    def flag(self, id):
        """
        Flag this content as being inapproprate of copyright violoation
        """
        pass



