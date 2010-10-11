"""
Group Actions
"""

from civicboom.lib.base import *

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class GroupActionsController(BaseController):

    #---------------------------------------------------------------------------
    # Join : 
    #---------------------------------------------------------------------------
    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def join(self, id, format="html"):
        group = get_group(id)
        if not group:
            raise action_error(_('group does not exist'), 404)
        if group.join(c.logged_in_user):
            return action_ok(_('joined %s' % group.username))
        else:
            raise action_error(_('unable to join %s' % group.username), 403)

    #---------------------------------------------------------------------------
    # Invite Member : (Admin Action)
    #---------------------------------------------------------------------------
    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def invite(self, id):
        # if admin
        # (invite role needed otherwise default to group default role)
        #create an invitaiton and notify user
        pass
    
    #---------------------------------------------------------------------------
    # Remove Member : (Admin Action)
    #---------------------------------------------------------------------------
    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def remove(self, id):
        # if removing self:
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
