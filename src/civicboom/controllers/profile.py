from civicboom.lib.base import *

from civicboom.controllers.members  import MembersController
#from civicboom.controllers.contents import ContentsController
from civicboom.controllers.member_lists import MemberListsController
from civicboom.controllers.messages import MessagesController
#from civicboom.controllers.search   import SearchController
#from civicboom.controllers.groups   import GroupsController

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
        data = MembersController().show(id=c.logged_in_persona.id, lists='followers, following, assignments_accepted')['data']
        data.update({
            'content' : MemberListsController().content(id=c.logged_in_persona.id          )['data']['list']  ,
            'messages': {
                'notifications': MessagesController().index(list='notification')['data']['list'] ,
                'to'           : MessagesController().index(list='to'          )['data']['list'] ,
            } ,
            'groups'  : MemberListsController()._groups_list_dict(c.logged_in_persona.groups_roles) ,
        })
        return action_ok(data=data)
