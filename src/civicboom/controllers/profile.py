from civicboom.lib.base import *

from civicboom.lib.helpers          import call_action
from civicboom.controllers.member   import MemberController
from civicboom.controllers.contents import ContentsController
from civicboom.controllers.messages import MessagesController
from civicboom.controllers.search   import SearchController

class ProfileController(BaseController):

    @auto_format_output()
    @authorize(is_valid_user)
    def index(self):
        # AllanC - contruct an uber dictionary for the template to render built from data from other controller actions
        results = {'data': {}}
        results['data'].update({'member'  : call_action(MemberController().show   , format='python', id=c.logged_in_user.id)['data']})
        results['data'].update({'content' : call_action(ContentsController().index, format='python'                        )['data']['list']})
        results['data'].update({'messages': {
            'notifications':                call_action(MessagesController().index, format='python', list='notification')['data']['list'] ,
            'to'           :                call_action(MessagesController().index, format='python', list='to'          )['data']['list'] ,
        }})
        return results

    @auto_format_output()
    def view(self, id=None):
        if id:
            c.viewing_user = get_user(id)
        else:
            c.viewing_user = c.logged_in_user
            
        if not c.viewing_user:
            return action_error(_("User does not exist"), code=404)
            
        results = {'data': {}}
        results['data'].update({'member'  : call_action(MemberController().show   , format='python', id     =c.viewing_user.id  )['data']})
        results['data'].update({'content' : call_action(SearchController().content, format='python', creator=c.viewing_user.id  )['data']['list']})
        #results['data'].update({'messages': {
        #    'public':                       call_action(MessagesController().index, format='python', list='public')['data']['list'] ,
        #}})
        
        return results
            
        #return render("web/profile/view.mako")
