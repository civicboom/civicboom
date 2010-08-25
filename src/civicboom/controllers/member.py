"""
Member
"""

from civicboom.lib.base import *
from pylons.i18n.translation import _ # see bug #51

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class MemberController(BaseController):

    @authorize(is_valid_user)
    @action_redirector()
    @authenticate_form
    def follow(self, id):
        status = c.logged_in_user.follow(id)
        if status == True:
            return _('You are now following %s') % id
        return _('Unable to follow member: %s') % status


    @authorize(is_valid_user)
    @action_redirector()
    @authenticate_form
    def unfollow(self, id):
        status = c.logged_in_user.unfollow(id)
        if status == True:
            return _('You have stopped following %s') % id
        return _('Unable to stop following member: %s') % status
