"""
Member
"""

from civicboom.lib.base import *

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class MemberActionsController(BaseController):

    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def follow(self, id, format="html"):
        """
        POST /members/{name}/follow: follow the member

        @api members 1.0 (WIP)

        @return 200   following ok
        @return 500   error following
        """
        status = c.logged_in_user.follow(id)
        if status == True:
            return action_ok(_('You are now following %s') % id)
        raise action_error(_('Unable to follow member: %s') % status)


    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def unfollow(self, id, format="html"):
        """
        POST /members/{name}/unfollow: unfollow the member

        @api members 1.0 (WIP)

        @return 200   unfollowing ok
        @return 500   error unfollowing
        """
        status = c.logged_in_user.unfollow(id)
        if status == True:
            return action_ok(_('You have stopped following %s') % id)
        raise action_error(_('Unable to stop following member: %s') % status)


    @auto_format_output()
    def followers(self, id, format="html"):
        """
        GET /members/{name}/followers: get a list of followers

        @api members 1.0 (WIP)

        @return 200   list ok
                list  the list
        """
        m = get_user(id)
        return action_ok(data={"list": [f.to_dict() for f in m.followers]})


    @auto_format_output()
    def following(self, id, format="html"):
        """
        GET /members/{name}/following: get a list of members the user is following

        @api members 1.0 (WIP)

        @return 200   list ok
                list  the list
        """
        m = get_user(id)
        return action_ok(data={"list": [f.to_dict() for f in m.following]})
