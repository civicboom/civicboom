from civicboom.lib.base import *
from civicboom.controllers.contents import _get_content, ContentsController

content_search = ContentsController().index

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class ContentListsController(BaseController):
    
    @web
    def actions(self, id, **kwargs):
        """
        GET /contents/{id}/actions: actions the current user can perform on this content
        
        @api contents 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200   list ok
                list  the list
        @return 404   not found
        """
        content = _get_content(id, is_viewable=True)
        return action_ok(data={"list": content.action_list_for(c.logged_in_persona)})


    #-----------------------------------------------------------------------------
    # Comments
    #-----------------------------------------------------------------------------

    @web
    def comments(self, id, **kwargs):
        """
        POST /contents/{id}/comments: Get a list of comments on the article
        
        @api contents 1.0 (WIP)
        
        @return list  the list of comments
        """
        content = _get_content(id, is_viewable=True)
        return action_ok(data={'list': [c.to_dict() for c in content.comments]})

    #-----------------------------------------------------------------------------
    # Accepted status
    #-----------------------------------------------------------------------------

    @web
    def accepted_status(self, id, **kwargs):
        content = _get_content(id, is_viewable=True)
        accepted_status = {
            'accepted' : [a.member.to_dict() for a in content.assigned_to if a.status=="accepted" ],
            'pending'  : [a.member.to_dict() for a in content.assigned_to if a.status=="pending"  ],
            'withdrawn': [a.member.to_dict() for a in content.assigned_to if a.status=="withdrawn"],
        }
        return action_ok(data={'accepted_status': accepted_status})


    #-----------------------------------------------------------------------------
    # Responses
    #-----------------------------------------------------------------------------

    @web
    def responses(self, id, **kwargs):
        #content = _get_content(id, is_viewable=True)
        #if 'include_fields' not in kwargs:
        #    kwargs['include_fields']='creator'
        #return action_ok(data={'list': [c.to_dict(**kwargs) for c in content.responses]})
        return content_search(response_to=id, **kwargs)
    
    
    #-----------------------------------------------------------------------------
    # Contributors
    #-----------------------------------------------------------------------------

    @web
    def contributors(self, id, **kwargs):
        content = _get_content(id, is_viewable=True)
        return action_ok(data={'list': []})
