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
    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def join(self, id):
        """
        Current user join a group
        
        @return 200 - joined ok
        """
        group = _get_group(id)
        if group.join(c.logged_in_user):
            return action_ok(_('joined %s' % group.username))
        raise action_error(_('unable to join %s' % group.username), 500)


    #---------------------------------------------------------------------------
    # Remove Member : (Admin Action) or self
    #---------------------------------------------------------------------------
    @auto_format_output()
    @web_params_to_kwargs()
    @authorize(is_valid_user)
    @authenticate_form
    def remove_member(self, id, remove_member=None, **kwargs):
        """
        """
        group = _get_group()
        if group.remove_member(remove_member):
            return action_ok(message='member removed sucessfully')
        raise action_error('unable to remove member', 500)


    #---------------------------------------------------------------------------
    # Invite Member : (Admin Action)
    #---------------------------------------------------------------------------
    @auto_format_output()
    @web_params_to_kwargs()
    @authorize(is_valid_user)
    @authenticate_form
    def invite(self, id, member=None, role=None, **kwargs):
        """
        Invite a member to join this groups
        (only if current user has admin role in group)
        
        @param role - the role the new user is to be invited as (if None group default is used)
            admin
            editor
            contributor
            observer
        
        @return 200 - invite sent ok
        """
        group = _get_group(id)
        if group.invite(member, role):
            return action_ok(_('member invited ok'))
        raise action_error('unable to invite member', 500)
    
    
    #---------------------------------------------------------------------------
    # Set Member Role : (Admin Action)
    #---------------------------------------------------------------------------
    @auto_format_output()
    @web_params_to_kwargs()
    @authorize(is_valid_user)
    @authenticate_form
    def set_role(self, id, member=None, role=None, **kwargs):
        """
        (only if current user has admin role in group)
        
        return 200 - role set ok
        """
        group = _get_group(id)
        if group.set_role(member, role):
            return action_ok(_('role set successfully'))
        raise action_error('unable to set role', 500)
