from civicboom.lib.base import *

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")

# AllanC - for members autocomplete index
from civicboom.model    import Member
from sqlalchemy         import or_, and_
#from sqlalchemy.orm     import join

#-------------------------------------------------------------------------------
# Global Functions
#-------------------------------------------------------------------------------

def _get_member(member):
    """
    Shortcut to return a member and raise not found automatically (as these are common opertations every time a member is fetched)
    """
    member = get_member(member)
    if not member:
        raise action_error(_("member not found"), code=404)
    return member


#-------------------------------------------------------------------------------
# Members Controler
#-------------------------------------------------------------------------------

class MembersController(BaseController):
    """
    @title Members
    @doc members
    @desc REST Controller styled on the Atom Publishing Protocol
    """


    @web
    def index(self, list='all', term=None, **kwargs):
        """
        GET /members: Show a list of members
        
        @api members 1.0 (WIP)
    
        @param list    type of list to get
               all     all members (useful with "term")
        @param term    filter results
        @param * (see common list return controls)
    
        @return 200      list ok
                members  array of member objects
        """
        result = []
    
        if list == "all":
            result = Session.query(Member)
    
        if term:
            result = result.filter(or_(Member.name.ilike("%"+term+"%"), Member.username.ilike("%"+term+"%")))
    
        return action_ok(data={"list": [m.to_dict(**kwargs) for m in result]})


    @web
    def show(self, id, **kwargs):
        """
        GET /members/{id}: Show a specific item
        
        @api members 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200      page ok
                member   member object
        @return 404      member not found
        """
        member = _get_member(id)
        
        if 'lists' not in kwargs:
            kwargs['lists'] = 'followers, following, assignments_accepted, content, groups, members, actions, boomed_content'
        
        data = {'member': member.to_dict(list_type='full', **kwargs)}

        # AllanC - cannot be imported at begining of module because of mutual coupling error
        from civicboom.controllers.member_actions import MemberActionsController
        member_actions_controller = MemberActionsController()
        
        for list in [list.strip() for list in kwargs['lists'].split(',')]:
            if hasattr(member_actions_controller, list):
                data[list] = getattr(member_actions_controller, list)(member, **kwargs)['data']['list']
        
        return action_ok(data=data)





# AllanC - Depricated old stuff?

#index_lists = {
#    'following'             : lambda member: member.following ,
#    'followers'             : lambda member: member.followers ,
#     'assignments_accepted': lambda member: member.assignments_accepted , 
#}


    #@auto_format_output
    #@authorize
    #def index(self, list=None):
    #    member_list_name = request.params.get('list', list)
    #    if member_list_name not in index_lists: raise action_error(_('list type %s not supported') % member_list_name)
    #    members = index_lists[member_list_name](c.logged_in_persona)
    #    members = [member.to_dict('default_list') for member in members]
    #    
    #    return {'data': {'list': members}}
