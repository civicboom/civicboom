from civicboom.lib.base import *

from civicboom.lib.helpers          import call_action
from civicboom.controllers.members  import MembersController
from civicboom.controllers.contents import ContentsController
from civicboom.controllers.messages import MessagesController
from civicboom.controllers.search   import SearchController

class ProfileController(BaseController):

    @auto_format_output()
    @authorize(is_valid_user)
    def index(self):
        # AllanC - contruct an uber dictionary for the template to render built from data from other controller actions
        results = action_ok(data={
            'member'  : call_action(MembersController().show  , format='python', id=c.logged_in_user.id, exclude_fields='content_public')['data'],
            'content' : call_action(ContentsController().index, format='python'                                                         )['data']['list'],
            'messages': {
                'notifications': call_action(MessagesController().index, format='python', list='notification')['data']['list'] ,
                'to'           : call_action(MessagesController().index, format='python', list='to'          )['data']['list'] ,
            }
        })
        return results
