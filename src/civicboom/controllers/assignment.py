"""
Assignemnt Actions
"""

from civicboom.lib.base import *
from civicboom.lib.database.get_cached import get_content
from civicboom.lib.communication       import messages

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class AssignmentController(BaseController):

    #-----------------------------------------------------------------------------
    # Accept
    #-----------------------------------------------------------------------------
    @action_redirector()
    @authorize(is_valid_user)
    @authenticate_form
    def accept(self, id=None):
        assignment = get_content(id)
        status     = assignment.accept(c.logged_in_user)
        if status == True:
            assignment.creator.send_message(messages.assignment_accepted(member=c.logged_in_user, assignment=assignment))
            return _("_assignment accepted")
        #elif isinstance(status,str):
        return status
        #return 'Error accepting _assignment'


    #-----------------------------------------------------------------------------
    # Withdraw
    #-----------------------------------------------------------------------------
    @action_redirector()
    @authorize(is_valid_user)
    @authenticate_form
    def withdraw(self, id=None):
        assignment = get_content(id)
        status     = assignment.withdraw(c.logged_in_user)
        if status == True:
            assignment.creator.send_message(messages.assignment_interest_withdrawn(member=c.logged_in_user, assignment=assignment))
            return _("_assignment interest withdrawn")
        #elif isinstance(status,str):
        #return status
        return _('Error withdrawing _assignment interest')
