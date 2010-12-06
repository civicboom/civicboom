from civicboom.lib.base import *
from civicboom.model import Media

from civicboom.lib.civicboom_lib import get_content_media_upload_key


class MediaController(BaseController):

    #-----------------------------------------------------------------------------
    # Upload Media
    #-----------------------------------------------------------------------------
    #@authorize
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
            form_file = form["Filedata"]
            media = Media()
            media.load_from_file(tmp_file=form_file, original_name=form_file.filename)
            #media.content_id = id # This does not work because the database complains about orphan records :(, it feels unnessisary to 
            get_content(id).attachments.append(media)
            #Session.add(media) # unneeded with attachments.append(media)
            Session.commit()
            update_content(id)
            #user_log.info("media appended to content #%d" % (id, )) # Update user log # err no user identifyable here

    #-----------------------------------------------------------------------------
    # Get Processing Status
    #-----------------------------------------------------------------------------
    def get_media_processing_staus(self, id):
        """
        Javascript can poll this method to get progress updates on the media processing
        Currently only return a flag to state if processing it taking place,
        but could be improved to return aditional progress info.
        """
        return action_ok(data=app_globals.memcache.get(str("media_processing_"+id)))
