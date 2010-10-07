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

class MemberController(BaseController):

    #@auto_format_output()
    #@authorize(is_valid_user)
    #def index(self, list=None):
    #    member_list_name = request.params.get('list', list)
    #    if member_list_name not in index_lists: return action_error(_('list type %s not supported') % member_list_name)
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
            return action_error(_("User does not exist"), code=404)
        
        return {'data': member.to_dict(**kwargs)}

    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def follow(self, id, format="html"):
        status = c.logged_in_user.follow(id)
        if status == True:
            return action_ok(_('You are now following %s') % id)
        return action_error(_('Unable to follow member: %s') % status)


    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def unfollow(self, id, format="html"):
        status = c.logged_in_user.unfollow(id)
        if status == True:
            return action_ok(_('You have stopped following %s') % id)
        return action_error(_('Unable to stop following member: %s') % status)
