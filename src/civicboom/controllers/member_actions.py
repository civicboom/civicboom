from civicboom.lib.base import *
from civicboom.model.filters import *
from civicboom.controllers.members  import MembersController
from civicboom.controllers.contents import ContentsController
from cbutils.misc import update_dict

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
        #raise action_error(_('Unable to follow member: %s') % status)

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
        #raise action_error(_('Unable to stop following member: %s') % status)


    #---------------------------------------------------------------------------
    # Action - Trust Follower
    #---------------------------------------------------------------------------
    @web
    @auth
    @role_required('editor')
    @account_type('plus')
    def follower_trust(self, id, **kwargs):
        """
        POST /members/{name}/trust_follower: trust a follower

        @type action
        @api members 1.0 (WIP)

        @return 200   follower trusted
        @return 500   error trusting
        """
        member = get_member(id, set_html_action_fallback=True)

        status = c.logged_in_persona.follower_trust(member)
        if status == True:
            return action_ok( _('You are now trusting your follower %s') % member.name or member.username )
        #raise action_error(_('Unable to trust member: %s') % status)


    #---------------------------------------------------------------------------
    # Action - DisTrust Follower
    #---------------------------------------------------------------------------
    @web
    @auth
    @role_required('editor')
    @account_type('plus')
    def follower_distrust(self, id, **kwargs):
        """
        POST /members/{name}/distrust_follower: remove trust from a follower

        @type action
        @api members 1.0 (WIP)

        @return 200   follower trust removed
        @return 500   error removing trust
        """
        member = get_member(id, set_html_action_fallback=True)

        status = c.logged_in_persona.follower_distrust(member)
        if status == True:
            return action_ok( _('You have removed trust from your follower %s') % member.name or member.username )
        #raise action_error(_('Unable to distrust: %s') % status)


    #---------------------------------------------------------------------------
    # Action - Invite Trusted Follower
    #---------------------------------------------------------------------------
    @web
    @auth
    @role_required('editor')
    @account_type('plus')
    def follower_invite_trusted(self, id, **kwargs):
        """
        POST /members/{name}/follower_invite: invite someone to follow you and become trusted

        @type action
        @api members 1.0 (WIP)

        @return 200   trusted follower invite sent
        @return 400   error sending invite
        """
        member = get_member(id, set_html_action_fallback=True)

        status = c.logged_in_persona.follower_invite_trusted(member)
        if status == True:
            return action_ok( _('You have invited the member %s to follow you as a trusted follower') % member.name or member.username )
        #raise action_error(_('Unable to invite: %s') % status)



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
        return action_ok(data={"list": member.action_list_for(member=c.logged_in_persona, role=c.logged_in_persona_role)})


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
        q = CreatorFilter.from_string(id)
        return content_search(_filter=q, **kwargs)


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
        q = BoomedByFilter.from_string(id)
        return content_search(_filter=q, **kwargs)


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
        q = OrFilter([
            BoomedByFilter.from_string(id),
            CreatorFilter.from_string(id),
        ])
        return content_search(_filter=q, **kwargs)


    #---------------------------------------------------------------------------
    # List - Group Membership
    #---------------------------------------------------------------------------
    
    #def _groups_list_dict(self, group_roles, **kwargs):
    #    return [update_dict(group_role.group.to_dict(**kwargs), {'role':group_role.role, 'status':group_role.status}) for group_role in group_roles]

    @web
    def groups(self, id, **kwargs):
        """
        GET /members/{name}/groups: get a list groups this member belongs to
        
        if logged in user = id and private=true will show groups membership of groups with hidden membership
        
        @type list
        @api members 1.0 (WIP)
        
        @return 200    list generated ok
                list   array of content objects
        @return 404   member not found
        """
        return member_search(groups_for=id, **kwargs)
        
        #member = get_member(id)        
        #if member == c.logged_in_persona and kwargs.get('private'):
        #    group_roles = member.groups_roles #self._groups_list_dict(
        #else:
        #    group_roles = [gr for gr in member.groups_roles if gr.status=="active" and gr.group.member_visibility=="public"] # AllanC - Duplicated from members.__to_dict__ .. can this be unifyed
        #
        #groups      = self._groups_list_dict(group_roles, **kwargs)
        #return to_apilist(groups, obj_type='member') #TODO transform


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
        
        if group.__type__ == 'group':
            return member_search(members_of=group)
        return to_apilist()
        
        #if hasattr(group, 'member_visibility'):
        #if group.member_visibility=="public" or group == c.logged_in_persona or group.get_membership(c.logged_in_persona):
        #        members = [update_dict(mr.member.to_dict(),{'role':mr.role, 'status':mr.status}) for mr in group.members_roles]
        #        return to_apilist(members, **kwargs) #TODO tranform
        #return to_apilist()
        

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
        return to_apilist(contents, obj_type='content') #TODO transform .. WTF!!? full? is this needed by mobile?


    @web
    def assignments_invited(self, id, **kwargs):
        """
        GET /members/{name}/assignments_invited: get a list of assignments this user has been invited to join

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
        contents = [content.to_dict("full") for content in member.assignments_invited]
        return to_apilist(contents, obj_type='content') #TODO transform .. full? again?
    
    # the mobile app uses "unaccepted" for "things that have been inited to and not accepted yet",
    # remove this once the mobile is updated to not use it (and customers get the update)
    assignments_unaccepted = assignments_invited


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

    # AllanC - for disscusuton
    #  should get_widget go here?
    # e.g. members/unittest/get_widget
    # e.g. members/unittest/widget
    # rather than
    # misc/get_widget/unittest
    # thoughts?
