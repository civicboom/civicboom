from civicboom.lib.base import *
from civicboom.controllers.members import _get_member
from civicboom.controllers.contents import ContentsController
content_search = ContentsController().index

from civicboom.lib.misc import update_dict

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")




#-------------------------------------------------------------------------------
# Controller
#-------------------------------------------------------------------------------
class MemberListsController(BaseController):
    """
    @comment AllanC the id value given to these lists could be str, int or loaded object
    """

    @web
    def actions(self, id, **kwargs):
        """
        GET /members/{name}/actions: actions the current user can perform on this member
        
        @api members 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200   list ok
                list  the list
        @return 404   not found
        """
        member = _get_member(id)
        return action_ok(data={"list": member.action_list_for(c.logged_in_persona)})



    @web
    def followers(self, id, **kwargs):
        """
        GET /members/{name}/followers: get a list of followers
        
        @api members 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200   list ok
                list  the list
        @return 404   not found
        """
        member = _get_member(id)
        return action_ok(data={"list": [f.to_dict(**kwargs) for f in member.followers]})


    @web
    def following(self, id, **kwargs):
        """
        GET /members/{name}/following: get a list of members the user is following
        
        @api members 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200   list ok
                list  the list
        @return 404   not found
        """
        member = _get_member(id)
        return action_ok(data={"list": [f.to_dict(**kwargs) for f in member.following]})


    @web
    def content(self, id, **kwargs):
        """
        GET /members/{name}/content: get a list content (including private if current user)
        
        @api members 1.0 (WIP)
        
        @param * (see common list return controls)
        @param list what type of contents to return, possible values:
          content
          assignments_active
          assignments_previous
          assignments
          articles
          drafts

        @return 200    list generated ok
                list   array of content objects
        @return 404   member not found
        """
        return content_search(creator=id, **kwargs)


    def _groups_list_dict(self, group_roles, **kwargs):
        return [update_dict(group_role.group.to_dict(**kwargs), {'role':group_role.role, 'status':group_role.status}) for group_role in group_roles]

    @web
    def groups(self, id, **kwargs):
        member = _get_member(id)
        
        #if member == c.logged_in_persona:
        #    group_roles = member.groups_roles
        #else: # Else only show public groups
        group_roles = [gr for gr in member.groups_roles if gr.status=="active" and gr.group.member_visability=="public"] # AllanC - Duplicated from members.__to_dict__ .. can this be unifyed
        groups      = self._groups_list_dict(group_roles, **kwargs)
        
        return action_ok(data={'list': groups})



    @web
    def assignments_accepted(self, id, **kwargs):
        member = _get_member(id)
        #if member != c.logged_in_user:
        #    raise action_error(_("Users may only view their own assignments (for now)"), code=403)
        contents = [content.to_dict("full") for content in member.assignments_accepted]
        return action_ok(data={'list': contents})


    @web
    def members(self, id, **kwargs):
        """
        groups only
        
        AllanC
        not exactly the best place for this ... but it fits.
        making a groups_list controler was overkill and compicated members/show ... so I left it here
        """
        group = _get_member(id)
        
        if hasattr(group, 'member_visability'):
            if group.member_visability=="public" or group.get_membership(c.logged_in_persona):
                return action_ok(data={'list':
                    [update_dict(mr.member.to_dict(),{'role':mr.role, 'status':mr.status}) for mr in group.members_roles]
                })
        
        return action_ok(data={'list': []})
