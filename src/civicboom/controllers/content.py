"""
Content Controller

For managing content:
-creating/editing
-attaching media
-deleting
-flagging
"""

from civicboom.lib.base                import BaseController, render, c, redirect, url, request
from civicboom.lib.misc                import flash_message
from civicboom.lib.database.get_cached import get_content

import logging
log = logging.getLogger(__name__)

prefix = "/web/content_editor/"


class ContentController(BaseController):
  
  #-----------------------------------------------------------------------------
  # View
  #-----------------------------------------------------------------------------
  def view(self,id=None):
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
  def edit(self,id=None):
    """
    Create or Edit new content with an editable HTML form
    """
    c.content = get_content(id)
    
    if request.POST: #Form contains post data
      c.content = _form_to_content(request.POST, c.content)
      Session.save(c.content)
      Session.commit()
    
      submit_action = request.POST['submit']
      if submit_action=='publish' or submit_action=='preview':
        return redirect(url(controller=__name__, action='view', id=c.content.id))

    # If this is the frist time saving the content then redirect to new substatiated id
    if id==None and request.POST:
      return redirect(url(controller=__name__, action='edit', id=c.content.id))
      
    #if c.content==None: pass #something has gone wrong, throw exception
    
    # Render content editor
    return render(prefix + "content_editor.mako")
  
  #-----------------------------------------------------------------------------
  # Add Media
  #-----------------------------------------------------------------------------
  def upload_media(self,id):
    """
    With javascript additional media can be uploaded individually
    """
    pass

  #-----------------------------------------------------------------------------
  # Delete
  #-----------------------------------------------------------------------------
  def delete(self,id):
    pass
  
  #-----------------------------------------------------------------------------
  # Flag
  #-----------------------------------------------------------------------------
  def flag(self,id):
    """
    Flag this content as being inapproprate of copyright violoation
    """
    pass
  
  #-----------------------------------------------------------------------------
  # Helpers
  #-----------------------------------------------------------------------------  
  def _form_to_content(form, content):
    """
    Takes form post data and either overlays the form with an existing object or create the relevent content object type and overlay form data
    """
    if not form   : return content #If there is no form data there is nothing to overlay or do
    if not content:
      content = DraftContent()
    return content
      #commit content update with data from form
      # save media
      # if record type changed
      #  remove previous record
      #  redirect to new id
