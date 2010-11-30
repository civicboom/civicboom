from civicboom.lib.base import *

from civicboom.model              import Media, ArticleContent, SyndicatedContent
from civicboom.lib                import helpers as h
from civicboom.lib.communication  import messages
from civicboom.lib.text           import clean_html
from civicboom.lib.authentication import get_user_and_check_password, signin_user
from civicboom.lib.database.get_cached import get_content

from decorator import decorator
from datetime import datetime
from glob import glob
import os
import json
import hashlib

log = logging.getLogger(__name__)
user_log = logging.getLogger("user")


#-----------------------------------------------------------------------------
# Decorators
#-----------------------------------------------------------------------------

# Check logged in - No need for redirect to HTML signin form as the mobile app is not a human
@decorator
def _logged_in_mobile(func, *args, **kargs):
    if not c.logged_in_persona:
        raise action_error("not authenticated", code=403)
    return func(*args, **kargs)


class MobileController(BaseController):

    #-----------------------------------------------------------------------------
    # Latest Version
    #-----------------------------------------------------------------------------  
    @auto_format_output
    def latest_version(self, format="html"):
        if format == "html":
            # HTML format = really old; the only HTML output we want to support
            # is the "you need to upgrade" bit; everything else in the controller
            # can break compatability
            return "1.13"
        else:
            return action_ok(data={"version": "1.13"})


    @_logged_in_mobile
    @auto_format_output
    def media_init(self):
        log.debug("Preparing for media from mobile")
        content = get_content(int(request.POST['content_id']))
        if not content:
            raise action_error(_("The content does not exist"), code=404)

        if os.path.exists("/tmp/upload-"+str(content.id)):
            os.remove("/tmp/upload-"+str(content.id))

        return action_ok(_("File prepared"), code=201)


    @_logged_in_mobile
    @auto_format_output
    def media_part(self):
        log.debug("Uploading media from mobile")
        content = get_content(int(request.POST['content_id']))
        if not content:
            raise action_error(_("The content does not exist"), code=404)
        #if content.editable_by(c.logged_in_persona):
        #    raise action_error(_("You are not the owner of that content"), code=403)

        tmp = file("/tmp/upload-"+str(content.id), "a")
        tmp.write(request.POST["file_data"].value)
        tmp.close()

        return action_ok(_("Part appended"), code=201)


    @_logged_in_mobile
    @auto_format_output
    def media_finish(self):
        log.debug("Finishing media")
        content = get_content(int(request.POST['content_id']))
        if not content:
            raise action_error(_("The content does not exist"), code=404)
        #if content.editable_by(c.logged_in_user):
        #    raise action_error(_("You are not the owner of that content"), code=403)

        m = Media()
        m.load_from_file(
            tmp_file="/tmp/upload-"+str(content.id),
            original_name=request.POST["file_name"],
            caption=None,
            credit=c.logged_in_persona.name
        )
        content.attachments.append(m)
        Session.commit()

        #os.unlink("/tmp/upload-"+str(content.id))

        return action_ok(_("Media attached"), code=201)

    #-----------------------------------------------------------------------------
    # Log mobile error
    #-----------------------------------------------------------------------------
    # If the mobile app has an error that it is not expecting then it can notify the live server
    # This can then be logged and email sent etc
    @auto_format_output
    def error(self):
        #from civicboom.lib.communication.email import send_email
        if not request.POST:
            if config['debug']:
                return action_ok("mobile error test") # FIXME: render(prefix+'mobile_error_test.mako')
            raise action_error("form data required", code=401)
        if 'error_message' in request.POST:
            #send_email(config['email_to'], subject='Mobile Error', content_text=request.POST['error_message'])
            #AllanC - Temp addition to get errors to the mobile developer
            #send_email("nert@poik.net"   , subject='Mobile Error', content_text=request.POST['error_message'])
            return action_ok("logged ok", code=201)

