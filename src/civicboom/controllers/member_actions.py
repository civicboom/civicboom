from civicboom.lib.base import *
from civicboom.controllers.members  import MembersController 
from civicboom.controllers.contents import ContentsController, sqlalchemy_content_query
from civicboom.lib.misc import update_dict

content_search = ContentsController().index
member_search  = MembersController().index

log      = logging.getLogger(__name__)


class MemberActionsController(BaseController):
    """
    Actions and lists that can be performed on a member
    
    @comment AllanC the id value given to these lists could be str, int or loaded object
    """

    #---------------------------------------------------------------------------
    # Action - Follow Member
    #---------------------------------------------------------------------------
    @web
    @auth
    @role_required('editor')
    def follow(self, id, **kwargs):
        """
        POST /members/{name}/follow: follow the member

        @type action
        @api members 1.0 (WIP)

        @return 200   following ok
        @return 500   error following
        """
        member = get_member(id, set_html_action_fallback=True)

        status = c.logged_in_persona.follow(member)
        if status == True:
            return action_ok( _('You are now following %s') % member.name or member.username )
        raise action_error(_('Unable to follow member: %s') % status)

    #---------------------------------------------------------------------------
    # Action - Unfollow Member
    #---------------------------------------------------------------------------
    @web
    @auth
    @role_required('editor')
    def unfollow(self, id, **kwargs):
        """
        POST /members/{name}/unfollow: unfollow the member

        @type action
        @api members 1.0 (WIP)

        @return 200   unfollowing ok
        @return 500   error unfollowing
        """
        member = get_member(id, set_html_action_fallback=True)
        status = c.logged_in_persona.unfollow(member)
        if status == True:
            return action_ok(_('You have stopped following %s') % member.name or member.username)
        raise action_error(_('Unable to stop following member: %s') % status)


    #---------------------------------------------------------------------------
    # List - User Actions
    #---------------------------------------------------------------------------
    @web
    def actions(self, id, **kwargs):
        """
        GET /members/{name}/actions: actions the current user can perform on this member

        @type special
        @api members 1.0 (WIP)
        
        @return 200   list ok
                list of strings
        
        @comment AllanC This is just a list of strings and is not a list object
        """
        member = get_member(id)
        return action_ok(data={"list": member.action_list_for(c.logged_in_persona)})


    #---------------------------------------------------------------------------
    # List - Followers
    #---------------------------------------------------------------------------
    @web
    def followers(self, id, **kwargs):
        """
        GET /members/{name}/followers: get a list of followers

        shortcut to members?follower_of={name}

        @type list
        @api members 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200   list ok
                list  the list
        @return 404   not found
        """
        #member = _get_member(id)
        #return action_ok(data={"list": [f.to_dict(**kwargs) for f in member.followers]})
        return member_search(follower_of=id, **kwargs)


    #---------------------------------------------------------------------------
    # List - Following
    #---------------------------------------------------------------------------
    @web
    def following(self, id, **kwargs):
        """
        GET /members/{name}/following: get a list of members the user is following

        shortcut to members?followed_by={name}

        @type list
        @api members 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @return 200   list ok
                list  the list
        @return 404   not found
        """
        #member = _get_member(id)
        #return action_ok(data={"list": [f.to_dict(**kwargs) for f in member.following]})
        return member_search(followed_by=id, **kwargs)


    #---------------------------------------------------------------------------
    # List - Content
    #---------------------------------------------------------------------------
    @web
    def content(self, id, **kwargs):
        """
        GET /members/{name}/content: get a list content (including private if current user)

        @type list
        shortcut to /contents?creator={name}
        
        @api members 1.0 (WIP)
        
        @param * (see GET /content)

        @return 200    list generated ok
                list   array of content objects
        """
        return content_search(creator=id, **kwargs)


    #---------------------------------------------------------------------------
    # List - Boomed Content
    #---------------------------------------------------------------------------
    @web
    def boomed(self, id, **kwargs):
        """
        GET /members/{name}/boomed: get a list content this user has boomed
        
        shortcut to content?boomed_by={name}

        @type list
        @api members 1.0 (WIP)
        
        @return 200    list generated ok
                list   array of content objects
        @return 404   member not found
        """
        return content_search(boomed_by=id, **kwargs)


    #---------------------------------------------------------------------------
    # List - Member Content and Boomed Content Union
    #---------------------------------------------------------------------------
    @web
    def content_and_boomed(self, id, **kwargs):
        """
        GET /members/{name}/content_and_boomed: get a list content this user has created and boomed

        @type list
        @api members 1.0 (WIP)
        
        @return 200    list generated ok
                list   array of content objects
        
        @comment AllanC special list union of content?boomed_by={name} and content?creator={name}
        """
        return content_search(boomed_by=id, union_query=sqlalchemy_content_query(creator=id) , **kwargs)


    #---------------------------------------------------------------------------
    # List - Group Membership
    #---------------------------------------------------------------------------
    
    def _groups_list_dict(self, group_roles, **kwargs):
        return [update_dict(group_role.group.to_dict(**kwargs), {'role':group_role.role, 'status':group_role.status}) for group_role in group_roles]

    @web
    def groups(self, id, **kwargs):
        """
        GET /members/{name}/groups: get a list groups this member belongs to

        @type list
        @api members 1.0 (WIP)
        
        @return 200    list generated ok
                list   array of content objects
        @return 404   member not found
        
        @comment AllanC not driven by members/index and lacks limit/offset controls etc
        """

        member = get_member(id)
        
        if member == c.logged_in_persona and kwargs.get('private'):
            group_roles = member.groups_roles #self._groups_list_dict(
        else:
            group_roles = [gr for gr in member.groups_roles if gr.status=="active" and gr.group.member_visibility=="public"] # AllanC - Duplicated from members.__to_dict__ .. can this be unifyed
        
        groups      = self._groups_list_dict(group_roles, **kwargs)
        return action_ok_list(groups)

    #---------------------------------------------------------------------------
    # List shortcuts
    #---------------------------------------------------------------------------
    @web
    def assignments_accepted(self, id, **kwargs):
        """
        GET /members/{name}/assignments_accepted: get a list of assignments this use has accepted

        @type list
        @api members 1.0 (WIP)
        
        @return 200    list generated ok
                list   array of content objects
        @return 404   member not found
        
        @comment AllanC not driven by members/index and lacks limit/offset controls etc
        """
        member = get_member(id)
        #if member != c.logged_in_user:
        #    raise action_error(_("Users may only view their own assignments (for now)"), code=403)
        contents = [content.to_dict("full") for content in member.assignments_accepted]
        return action_ok_list(contents, obj_type='content')


    @web
    def assignments_unaccepted(self, id, **kwargs):
        """
        GET /members/{name}/assignments_unaccepted: get a list of assignments this user has been invited to join

        @type list
        @api members 1.0 (WIP)
        
        @return 200    list generated ok
                list   array of content objects
        @return 404   member not found
        
        @comment AllanC unaccepted is not the correct term, we use the term 'invite'
        @comment AllanC not driven by members/index and lacks limit/offset controls etc
        """

        member = get_member(id)
        #if member != c.logged_in_user:
        #    raise action_error(_("Users may only view their own assignments (for now)"), code=403)
        contents = [content.to_dict("full") for content in member.assignments_unaccepted]
        return action_ok_list(contents, obj_type='content')

    @web
    def assignments_active(self, id, **kwargs):
        """
        GET /members/{name}/assignments_active: list of members active assignments

        @type list
        
        shotcut to /members?creator={name}&list=assignments_active
        
        @api members 1.0 (WIP)
        
        @return 200    list generated ok
                list   array of content objects
        """
        return content_search(creator=id, list='assignments_active'  ,**kwargs)

    @web
    def assignments_previous(self, id, **kwargs):
        """
        GET /members/{name}/assignments_previous: list of members previous assignments

        @type list
        
        shotcut to /members?creator={name}&list=assignments_previous
        
        @api members 1.0 (WIP)
        
        @return 200    list generated ok
                list   array of content objects
        """
        return content_search(creator=id, list='assignments_previous',**kwargs)


    #---------------------------------------------------------------------------
    # List - Members (group only)
    #---------------------------------------------------------------------------
    @web
    def members(self, id, **kwargs):
        """
        GET /members/{name}/members: list of members of this group
        
        groups only

        @type list
        @api members 1.0 (WIP)
        
        @comment AllanC
        not exactly the best place for this ... but it fits.
        making a groups_list controler was overkill and compicated members/show ... so I left it here
        """
        group = get_member(id)
        
        # FIXME!!!!!
        # AllanC - HACK ALERT - I needed actions for a member list, so I left c.group so the frag template could look at it - horrible!!!
        c.group = group
        
        if hasattr(group, 'member_visibility'):
            if group.member_visibility=="public" or group.get_membership(c.logged_in_persona) or group == c.logged_in_persona:
                members = [update_dict(mr.member.to_dict(),{'role':mr.role, 'status':mr.status}) for mr in group.members_roles]
                return action_ok_list(members)
        return action_ok_list([])
