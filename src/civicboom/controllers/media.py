from civicboom.lib.base import *
from civicboom.model import Media

from civicboom.lib.civicboom_lib import get_content_media_upload_key
from civicboom.lib.database.get_cached import get_content, get_member

import pprint

# Logging setup
log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class MediaController(BaseController):

    #-----------------------------------------------------------------------------
    # Upload Media
    #-----------------------------------------------------------------------------
    #@authorize
    def upload_media(self):
        """
        With javascript/flash additional media can be uploaded individually
        """
        user_log.debug("User is attempting to upload media:" + pprint.pformat(request.POST))
        form = request.POST
        if 'file_data' in form and 'content_id' in form and 'member_id' in form and 'key' in form:
            form_file = form["file_data"]
            content = get_content(int(form['content_id']))
            member  = get_member(int(form['member_id']))
            if not member.check_action_key("attach to %d" % content.id, form['key']):
                return "invalid action key"
            if not content.editable_by(member):
                return "can't edit this article"
            media = Media()
            media.load_from_file(tmp_file=form_file, original_name=form_file.filename)
            content.attachments.append(media)
            Session.commit()
            user_log.info("Media #%d appended to Content #%d" % (media.id, content.id))
            return "ok"
        else:
            return "missing file_data or content_id"

    #-----------------------------------------------------------------------------
    # Get Processing Status
    #-----------------------------------------------------------------------------
    @web
    def get_media_processing_staus(self, id):
        """
        Javascript can poll this method to get progress updates on the media processing
        Currently only return a flag to state if processing it taking place,
        but could be improved to return aditional progress info.
        """
        return action_ok(data={"status":app_globals.memcache.get(str("media_processing_"+id))})
