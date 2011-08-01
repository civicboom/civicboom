from civicboom.lib.base import *

#from civicboom.controllers.contents       import ContentsController, list_filters as content_list_filters
from civicboom.controllers.members        import MembersController
#from civicboom.controllers.member_actions import MemberActionsController
#from civicboom.controllers.messages       import MessagesController
#from civicboom.controllers.groups   import GroupsController
#from civicboom.controllers.contents import ContentsController

#contents_controller       = ContentsController()
members_controller        = MembersController()
#member_actions_controller = MemberActionsController()
#messages_controller       = MessagesController()
#content_list_names        = content_list_filters.keys()


class ProfileController(BaseController):
    """
    @title Profile
    @doc profile
    @desc a controller which pulls together many odd bits of user-relevant information
    """

    @web
    @authorize
    def index(self, **kwargs):
        """
        GET /profile: Get info about the logged in user

        @api profile 1.0 (WIP)

        @return 200      page ok
                member   member object
                content  a list of the member's contents
                messages a list of messages, split into 'notifications' and 'to'
                num_unread_messages
                num_unread_notifications
        """
        # NOTE: if this method is refactored or renamed please update cb_frag.js (as it is outside pylons and has a hard coded url to '/profile/index')
        
        member_return = members_controller.show(id=c.logged_in_persona.username, private=True)
        member_return['data'].update(
            self.messages()['data']
        )
        return member_return

    @web
    @authorize
    def messages(self, **kwargs):
        """
        GET /profile/messages: Get number of unread messages/notifications

        @api profile 1.0 (WIP)

        @return 200      page ok
                num_unread_messages
                num_unread_notifications
        """
        return action_ok(
            data = {
                'num_unread_messages'     :c.logged_in_persona.num_unread_messages,
                'num_unread_notifications':c.logged_in_persona.num_unread_notifications,
            }
        )
