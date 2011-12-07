from civicboom.lib.base import *

#from civicboom.controllers.contents       import ContentsController, list_filters as content_list_filters
from civicboom.controllers.members        import MembersController
from civicboom.controllers.member_actions import MemberActionsController
#from civicboom.controllers.messages       import MessagesController
#from civicboom.controllers.groups   import GroupsController
#from civicboom.controllers.contents import ContentsController

#contents_controller       = ContentsController()
members_controller        = MembersController()
member_actions_controller = MemberActionsController()
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
                num_unread_messages integer
                num_unread_notifications integer
                * all the default lists retured by member/show with the additional kwarg 'private=True'
        """
        # NOTE: if this method is refactored or renamed please update cb_frag.js (as it is outside pylons and has a hard coded url to '/profile/index')
        

        if c.format == "html" and c.subformat == 'web': # Proto: optimisation for web subformat, broke mobile without c.subformat check
            return action_ok() # html format is just "include /profile.frag"

        member_return = members_controller.show(id=c.logged_in_persona, private=True, **kwargs)

        member_return['data'].update(self.messages()['data'])
        #member_return['data'].update(self.personas()['data']) # AllanC - there is no need to include this here as it is the same as ['data']['groups']
        
        return member_return

    @web
    @authorize
    def messages(self, **kwargs):
        """
        GET /profile/messages: Get number of unread messages/notifications

        @api profile 1.0 (WIP)

        @return 200 page ok
                num_unread_messages integer
                num_unread_notifications integer
                last_message_timestamp dateime
                last_notification_timestamp datetime
        """
        return action_ok(
            data = {
                'num_unread_messages'           :c.logged_in_persona.num_unread_messages,
                'num_unread_notifications'      :c.logged_in_persona.num_unread_notifications,
                'last_message_timestamp'        :c.logged_in_persona.last_message_timestamp.strftime('%s.%f') if c.logged_in_persona.last_message_timestamp else None,
                'last_notification_timestamp'   :c.logged_in_persona.last_notification_timestamp.strftime('%s.%f') if c.logged_in_persona.last_notification_timestamp else None,
            }
        )

    @web
    @authorize
    def personas(self, **kwargs):
        """
        GET /profile/personas: Get a list of peronas that the current user can swich to.

        @api profile 1.0 (WIP)

        @return 200      page ok
                groups a list of personas this user can swich into
        
        @comment AllanC Shortcut to index/groups_for=me?private=True this is provided by default in the full profile

        """
        return action_ok(
            data = {
                'groups': member_actions_controller.groups(id=c.logged_in_persona, private=True)
            }
        )