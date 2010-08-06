"""
Set of helpers specificly to the Civicboom project
  (these are not part of misc because misc is more genereal functions that could be used in a range of projects)
"""

from pylons import url, app_globals
from pylons.i18n.translation import _


from civicboom.model.meta import Session
from civicboom.lib.database.get_cached import get_user

from civicboom.lib.communication.email import send_email



#-------------------------------------------------------------------------------
# Users in pending status are forced to complete the registration process.
#   some urls have to be made avalable to pending users (such as signout, etc)
def deny_pending_user(url_to_check):
    pending_user_allowed_list = ['register/new_user','account/signout']
    for url_safe in pending_user_allowed_list:
        if url_to_check.find(url_safe)>=0:
            return False
    return True


#-------------------------------------------------------------------------------

def send_verifiy_email(user, controller='account', action='verify_email', message=_('verify this email address')):
    Session.refresh(user)
    validation_link = url(controller=controller, action=action, id=user.id, host=app_globals.site_host, hash=user.hash())
    message         = _('Please %s by clicking on, or copying the following link into your browser: %s') % (message, validation_link)
    send_email(user.email_unverifyed, subject=_('verify e-mail address'), content_text=message)

def verify_email(user, hash, commit=False):
    user = get_user(user)
    if user and user.hash() == hash:
        user.email            = user.email_unverifyed
        user.email_unverifyed = None
        if commit: Session.commit()
        return True
    return False
