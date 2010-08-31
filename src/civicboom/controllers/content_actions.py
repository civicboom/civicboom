"""
Assignemnt Actions
"""

from civicboom.lib.base import *
from civicboom.lib.database.get_cached import get_content
from civicboom.lib.communication       import messages

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class ContentActionsController(BaseController):

    #---------------------------------------------------------------------------
    # Rate: User Visable Content
    #---------------------------------------------------------------------------
    @action_redirector()
    @authorize(is_valid_user)
    @authenticate_form
    def rate(self, id):
        # Implement me
        pass


    #---------------------------------------------------------------------------
    # Boom: User Visable Content (to all followers)
    #---------------------------------------------------------------------------
    @action_redirector()
    @authorize(is_valid_user)
    @authenticate_form
    def boom(self, id):
        # Implement me
        pass


    #---------------------------------------------------------------------------
    # Approve: User Visable Content (organistaion only)
    #---------------------------------------------------------------------------
    @action_redirector()
    @authorize(is_valid_user)
    @authenticate_form
    def approve(self, id):
        # Implement me
        pass

    #---------------------------------------------------------------------------
    # Disassociate: User Visable Content (organistaion only)
    #---------------------------------------------------------------------------
    @action_redirector()
    @authorize(is_valid_user)
    @authenticate_form
    def disasociate(self):
        # Implement me
        pass


    #---------------------------------------------------------------------------
    # Accept: Assignment
    #---------------------------------------------------------------------------
    @action_redirector()
    @authorize(is_valid_user)
    @authenticate_form
    def accept(self, id=None):
        assignment = get_content(id)
        status     = assignment.accept(c.logged_in_user)
        if status == True:
            assignment.creator.send_message(messages.assignment_accepted(member=c.logged_in_user, assignment=assignment))
            return action_ok(_("_assignment accepted"))
        #elif isinstance(status,str):
        return action_error(_('Error accepting _assignment'))


    #---------------------------------------------------------------------------
    # Withdraw: from Assignment
    #---------------------------------------------------------------------------
    @action_redirector()
    @authorize(is_valid_user)
    @authenticate_form
    def withdraw(self, id=None):
        assignment = get_content(id)
        status     = assignment.withdraw(c.logged_in_user)
        if status == True:
            assignment.creator.send_message(messages.assignment_interest_withdrawn(member=c.logged_in_user, assignment=assignment))
            return action_ok(_("_assignment interest withdrawn"))
        #elif isinstance(status,str):
        #return status
        return action_error(_('Error withdrawing _assignment interest'))
