"""
Group Actions
"""

from civicboom.lib.base import *
from civicboom.controllers.groups import _get_group

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class GroupActionsController(BaseController):


    #---------------------------------------------------------------------------
    # Join : 
    #---------------------------------------------------------------------------
    @web
    @auth
    def join(self, id, **kwargs):
        """
        POST /groups/{id}/join: join the group, or request to join if admin approval is required

        @api groups 1.0 (WIP)
        
        @return 200 joined ok
        @return 403 permission denied
        """
        group = _get_group(id)

        # Check permissions
        if not group.can_join(c.logged_in_persona):
            raise action_error(_('current user cannot join this group'), code=403)
        
        # Join action
        join_status = group.join(c.logged_in_persona)
        if join_status == True:
            user_log.info("joined %s" % group.username)
            return action_ok(_('joined %s' % group.username))
        elif join_status == "request":
            return action_ok(_('join request sent'))
        
        raise action_error(_('unable to join %s' % group.username), code=500)


    #---------------------------------------------------------------------------
    # Remove Member : (Admin Action) or self
    #---------------------------------------------------------------------------
    @web
    @auth
    def remove_member(self, id, **kwargs):
        """
        POST /groups/{id}/remove_member: remove a member from the group
        
        @api groups 1.0 (WIP)
        """
        member = kwargs.get('member', None)
        
        group  = _get_group(id)
        member = get_member(member)
        # permissions check
        if member!=c.logged_in_persona and not group.is_admin(c.logged_in_persona):
            raise action_error('current user has no permissions for this group', code=403)
        # remove action
        if group.remove_member(member):
            user_log.info("Remebed member %s from group %s" % (member.username, group.username))
            return action_ok(message='member removed sucessfully')
        raise action_error('unable to remove member', code=500)


    #---------------------------------------------------------------------------
    # Invite Member : (Admin Action)
    #---------------------------------------------------------------------------
    @web
    @auth
    def invite(self, id, **kwargs):
        """
        POST /groups/{id}/invite:
        Invite a member to join this groups
        (only if current user has admin role in group)
        
        @api groups 1.0 (WIP)
        
        @param role - the role the new user is to be invited as (if None group default is used)
            admin
            editor
            contributor
            observer
        
        @return 200 - invite sent ok
        """
        member = kwargs.get('member', None)
        role   = kwargs.get('role'  , None)        
        
        group = _get_group(id, is_admin=True)
        if group.invite(member, role):
            return action_ok(_('%(member)s has been invited to join %(group)s' % {'member':member, 'group':group.name}))
        raise action_error('unable to invite member', code=500)
    
    
    #---------------------------------------------------------------------------
    # Set Member Role : (Admin Action)
    #---------------------------------------------------------------------------
    @web
    @auth
    def set_role(self, id, member=None, role=None, **kwargs):
        """
        POST /groups/{id}/set_role:
        
        @api groups 1.0 (WIP)
        
        (only if current user has admin role in group)
        
        used to approve join requests (role=None=default group join role)

        @param member
        @param role
        
        @return 200  role set ok
        @return 400  cannot remove last admin
        """
        group = _get_group(id, is_admin=True)
        if group.set_role(member, role): # FIXME: check that member exists? If we _get_member, then member.username would work below
            user_log.info("Set role of member %s to %s in group %s" % (member, role, group.username))
            return action_ok(_('role set successfully'))
        raise action_error('unable to set role', code=500)
