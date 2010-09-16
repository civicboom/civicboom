"""
Member
"""

from civicboom.lib.base import *

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class MemberController(BaseController):

    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def follow(self, id, format="html"):
        status = c.logged_in_user.follow(id)
        if status == True:
            return action_ok(_('You are now following %s') % id)
        return action_error(_('Unable to follow member: %s') % status)


    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def unfollow(self, id, format="html"):
        status = c.logged_in_user.unfollow(id)
        if status == True:
            return action_ok(_('You have stopped following %s') % id)
        return action_error(_('Unable to stop following member: %s') % status)
