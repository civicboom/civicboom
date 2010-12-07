from civicboom.lib.base import *

from civicboom.controllers.members        import MembersController
from civicboom.controllers.member_actions import MemberActionsController
from civicboom.controllers.messages       import MessagesController
#from civicboom.controllers.search   import SearchController
#from civicboom.controllers.groups   import GroupsController
#from civicboom.controllers.contents import ContentsController

members_controller        = MembersController()
member_actions_controller = MemberActionsController()
messages_controller       = MessagesController()

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
        """
        # AllanC - contruct an uber dictionary for the template to render built from data from other controller actions
        data = members_controller.show(id=c.logged_in_persona.id, lists='followers, following, assignments_accepted')['data']
        data.update({
            'content' : member_actions_controller.content(id=c.logged_in_persona.id          )['data']['list']  ,
            'messages': {
                'notifications': messages_controller.index(list='notification')['data']['list'] ,
                'to'           : messages_controller.index(list='to'          )['data']['list'] ,
            } ,
            'groups'  : member_actions_controller._groups_list_dict(c.logged_in_persona.groups_roles) ,
        })
        return action_ok(data=data)
