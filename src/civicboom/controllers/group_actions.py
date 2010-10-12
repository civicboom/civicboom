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
        Join a group
        
        @return 200 - joined ok
        """
        group = _get_group(id)
        
        if group.join(c.logged_in_user):
            return action_ok(_('joined %s' % group.username))
        else:
            raise action_error(_('unable to join %s' % group.username), 403)

    #---------------------------------------------------------------------------
    # Invite Member : (Admin Action)
    #---------------------------------------------------------------------------
    @auto_format_output()
    @web_params_to_kwargs()
    @authorize(is_valid_user)
    @authenticate_form
    def invite(self, id, role=None):
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
        group = _get_group(id, check_admin=True)
        # (invite role needed otherwise default to group default role)
        #create an invitaiton and notify user
        pass
    
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
        group         = _get_group()
        remove_member = get_member(remove_member)

            
        
        group.remove_member(remove_member)
        
            
        #   ok
        # elif admin
        # if removing self and other admins NOT exisit: error
        #create an invitaiton and notify user
        pass
    
    #---------------------------------------------------------------------------
    # Set Member Role : (Admin Action)
    #---------------------------------------------------------------------------
    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def set_role(self, id):
        # if admin
        #   if changing self role and other admins not exisit: error
        # change user role
        pass
