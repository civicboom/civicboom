"""
Member
"""

from civicboom.lib.base import *

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


#index_lists = {
#    'following'             : lambda member: member.following ,
#    'followers'             : lambda member: member.followers ,
#     'assignments_accepted': lambda member: member.assignments_accepted , 
#}

class MembersController(BaseController):

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
    def show(self, id=None, **kwargs):
        """
        Get single user
        """
        if 'list_type' not in kwargs:
            kwargs['list_type'] = 'single'
            
        if id:
            member = get_user(id)
        else:
            member = c.logged_in_user
        if not member:
            raise action_error(_("User does not exist"), code=404)

        return action_ok(data={'member': member.to_dict(**kwargs)})
