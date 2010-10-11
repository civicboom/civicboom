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
        # check if inviation exisit
        # join an open group or create a request if
        # send notify group
        pass

    #---------------------------------------------------------------------------
    # Invite Member : (Admin Action)
    #---------------------------------------------------------------------------
    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def invite(self, id):
        # if admin
        #create an invitaiton and notify user
        pass
    
    #---------------------------------------------------------------------------
    # Remove Member : (Admin Action)
    #---------------------------------------------------------------------------
    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def remove(self, id):
        # if admin
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
