"""
Assignemnt Actions
"""

from civicboom.lib.base import *
from civicboom.lib.database.get_cached import get_content
from civicboom.lib.communication       import messages
from civicboom.model                   import Rating
from sqlalchemy.orm.exc import NoResultFound

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
        # remove any existing ratings
        # we need to commit after removal, otherwise SQLAlchemy
        # will optimise remove->add as modify-existing, and the
        # SQL trigger will break
        try:
            q = Session.query(Rating)
            q = q.filter(Rating.content_id==int(id))
            q = q.filter(Rating.member==c.logged_in_user)
            existing = q.one()
            Session.delete(existing)
            Session.commit()
        except NoResultFound:
            pass

        # add a new one
        if "rating" in request.POST:
            rating = int(request.POST["rating"])
            # rating = 0 = remove vote
            if rating > 0:
                r = Rating()
                r.content_id = int(id)
                r.member     = c.logged_in_user
                r.rating     = rating
                Session.add(r)
                Session.commit()
        user_log.info("Rated Content #%d as %d" % (int(id), int(request.POST["rating"])))

        return action_ok("Vote counted")


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
