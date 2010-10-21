"""
Member
"""

from civicboom.lib.base import *
from civicboom.model    import Member

from sqlalchemy         import or_, and_
from sqlalchemy.orm     import join

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


#index_lists = {
#    'following'             : lambda member: member.following ,
#    'followers'             : lambda member: member.followers ,
#     'assignments_accepted': lambda member: member.assignments_accepted , 
#}

class MembersController(BaseController):
    """
    @title Members
    @doc members
    @desc REST Controller styled on the Atom Publishing Protocol
    """

    #@auto_format_output()
    #@authorize(is_valid_user)
    #def index(self, list=None):
    #    member_list_name = request.params.get('list', list)
    #    if member_list_name not in index_lists: raise action_error(_('list type %s not supported') % member_list_name)
    #    members = index_lists[member_list_name](c.logged_in_user)
    #    members = [member.to_dict('default_list') for member in members]
    #    
    #    return {'data': {'list': members}}

    @auto_format_output()
    @web_params_to_kwargs()
    def index(self, **kwargs):
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

        if kwargs.get('list', "all") == "all":
            result = Session.query(Member)

        if "term" in kwargs:
            s = kwargs["term"]
            result = result.filter(or_(Member.name.ilike("%"+s+"%"), Member.username.ilike("%"+s+"%")))

        return action_ok(data={"members": [m.to_dict(**kwargs) for m in result]})

    @auto_format_output()
    @web_params_to_kwargs()
    def show(self, id, **kwargs):
        """
        GET /members/{id}: Show a specific item
        
        @api members 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200      page ok
                member   member object
        @return 404      member not found
        """
        if 'list_type' not in kwargs:
            kwargs['list_type'] = 'full+actions'
        
        member = get_member(id)
        
        if not member:
            raise action_error(_("User does not exist"), code=404)
        
        return action_ok(data={'member': member.to_dict(**kwargs)})
