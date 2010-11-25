from civicboom.lib.base import *
from civicboom.controllers.members import _get_member

from civicboom.lib.misc import update_dict

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------

# AllanC - TODO: these SQLAlchemy links should be deprecated in preference to actual content searches
content_lists = {
    'content'             : lambda member: member.content ,
    'content_public'      : lambda member: member.content_public ,
    'assignments_active'  : lambda member: member.content_assignments_active ,
    'assignments_previous': lambda member: member.content_assignments_previous,
    'assignments'         : lambda member: member.content_assignments ,
    'articles'            : lambda member: member.content_articles ,
    'drafts'              : lambda member: member.content_drafts ,
    #'accepted_assignments': lambda member: member.accepted_assignments ,
}



#-------------------------------------------------------------------------------
# Controller
#-------------------------------------------------------------------------------
class MemberListsController(BaseController):

    @auto_format_output
    @web_params_to_kwargs
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



    @auto_format_output
    @web_params_to_kwargs
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


    @auto_format_output
    @web_params_to_kwargs
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


    @auto_format_output
    @web_params_to_kwargs
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
        if 'list' not in kwargs:
            kwargs['list'] = 'content'
        if 'exclude_fields' not in kwargs:
            kwargs['exclude_fields'] = 'creator'
        
        member = _get_member(id)
        
        # AllanC - I dont like this ...
        #          we want people to be able to filter the lists from the API ... but as we just call the SQLAlchemy links we cant tell what data is public or private
        #          we need a more sophisticated method of doing this, maybe leveraging a new search with public=true
        #          content_lists (above) should be refactored?
        if member != c.logged_in_persona:
            kwargs['list'] = 'content_public'
        
        list = kwargs['list']
        if list not in content_lists:
            raise action_error(_('list type %s not supported') % list, code=400)
            
        contents = content_lists[list](member)
        contents = [content.to_dict(**kwargs) for content in contents]
        
        return action_ok(data={'list': contents})


    def _groups_list_dict(self, group_roles):
        return [update_dict(group_role.group.to_dict(**kwargs), {'role':group_role.role, 'status':group_role.status}) for group_role in group_roles]

    @auto_format_output
    @web_params_to_kwargs
    def groups(self, id, **kwargs):
        member = _get_member(id)
        
        #if member == c.logged_in_persona:
        #    group_roles = member.groups_roles
        #else: # Else only show public groups
        group_roles = [gr for gr in member.groups_roles if gr.status=="active" and gr.group.member_visability=="public"] # AllanC - Duplicated from members.__to_dict__ .. can this be unifyed
        groups      = self._groups_list_dict(group_roles)
        
        return action_ok(data={'list': groups})



    @auto_format_output
    @web_params_to_kwargs
    def assignments_accepted(self, id, **kwargs):
        member = _get_member(id)
        #if member != c.logged_in_user:
        #    raise action_error(_("Users may only view their own assignments (for now)"), code=403)
        contents = [content.to_dict("full") for content in member.assignments_accepted]
        return action_ok(data={'list': contents})

    @auto_format_output
    @web_params_to_kwargs
    def members(self, id, **kwargs):
        """
        groups only
        """
        #if group.member_visability=="public" or group.get_membership(c.logged_in_persona):
        #return [update_dict(m.member.to_dict(),{'role':m.role, 'status':m.status}) for m in group.members_roles]
        pass
