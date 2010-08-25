"""
Member
"""

from civicboom.lib.base import *

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class MemberController(BaseController):

    @authorize(is_valid_user)
    @action_redirector()
    @authenticate_form
    def follow(self, id):
        status = c.logged_in_user.follow(id)
        if status == True:
            return action_ok(_('You are now following %s') % id)
        return action_error(_('Unable to follow member: %s') % status)


    @authorize(is_valid_user)
    @action_redirector()
    @authenticate_form
    def unfollow(self, id):
        status = c.logged_in_user.unfollow(id)
        if status == True:
            return action_ok(_('You have stopped following %s') % id)
        return action_error(_('Unable to stop following member: %s') % status)
