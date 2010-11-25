from civicboom.lib.base import *
from civicboom.controllers.members import _get_member

from civicboom.lib.misc import update_dict

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class MemberActionsController(BaseController):

    @auto_format_output
    @authorize(is_valid_user)
    @authenticate_form
    def follow(self, id, format="html"):
        """
        POST /members/{name}/follow: follow the member

        @api members 1.0 (WIP)

        @return 200   following ok
        @return 500   error following
        """
        status = c.logged_in_persona.follow(id)
        if status == True:
            return action_ok(_('You are now following %s') % id)
        raise action_error(_('Unable to follow member: %s') % status)


    @auto_format_output
    @authorize(is_valid_user)
    @authenticate_form
    def unfollow(self, id, format="html"):
        """
        POST /members/{name}/unfollow: unfollow the member

        @api members 1.0 (WIP)

        @return 200   unfollowing ok
        @return 500   error unfollowing
        """
        status = c.logged_in_persona.unfollow(id)
        if status == True:
            return action_ok(_('You have stopped following %s') % id)
        raise action_error(_('Unable to stop following member: %s') % status)

