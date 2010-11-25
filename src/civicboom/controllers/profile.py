from civicboom.lib.base import *

from civicboom.controllers.members  import MembersController
#from civicboom.controllers.contents import ContentsController
from civicboom.controllers.member_actions import MemberActionsController
from civicboom.controllers.messages import MessagesController
from civicboom.controllers.search   import SearchController
from civicboom.controllers.groups   import GroupsController

class ProfileController(BaseController):
    """
    @title Profile
    @doc profile
    @desc a controller which pulls together many odd bits of user-relevant information
    """

    @auto_format_output
    @authorize(is_valid_user)
    def index(self):
        """
        GET /profile: Get info about the logged in user

        @api profile 1.0 (WIP)

        @return 200      page ok
                member   member object
                content  a list of the member's contents
                messages a list of messages, split into 'notifications' and 'to'
        """
        # AllanC - contruct an uber dictionary for the template to render built from data from other controller actions
        results = action_ok(data={
            'member'  :       MembersController().show   (id=c.logged_in_persona.id, exclude_fields='content_public, groups_public')['data']['member'],
            'content' : MemberActionsController().content(id=c.logged_in_persona.id,                                               )['data']['list']  ,
            'messages': {
                'notifications': MessagesController().index(list='notification')['data']['list'] ,
                'to'           : MessagesController().index(list='to'          )['data']['list'] ,
            } ,
            'groups'  : MemberActionsController().groups(id=c.logged_in_persona.id)['data']['list'] ,
        })
        return results
