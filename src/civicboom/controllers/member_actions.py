"""
Member Actions
"""

from civicboom.lib.base import *
from civicboom.controllers.members import _get_member

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
        status = c.logged_in_user.follow(id)
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
        status = c.logged_in_user.unfollow(id)
        if status == True:
            return action_ok(_('You have stopped following %s') % id)
        raise action_error(_('Unable to stop following member: %s') % status)


    @auto_format_output
    @web_params_to_kwargs
    def followers(self, id, **kwargs):
        """
        GET /members/{name}/followers: get a list of followers
        
        @api members 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200   list ok
                list  the list
        @return 404   not found
        """
        member = _get_member(id)
        return action_ok(data={"list": [f.to_dict(**kwargs) for f in member.followers]})


    @auto_format_output
    @web_params_to_kwargs
    def following(self, id, **kwargs):
        """
        GET /members/{name}/following: get a list of members the user is following
        
        @api members 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200   list ok
                list  the list
        @return 404   not found
        """
        member = _get_member(id)
        return action_ok(data={"list": [f.to_dict(**kwargs) for f in member.following]})
