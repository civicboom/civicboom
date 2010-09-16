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
    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def rate(self, id, format="html"):
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

        user_log.debug("Rated Content #%d as %d" % (int(id), int(request.POST["rating"])))
        return action_ok(_("Vote counted"))


    #---------------------------------------------------------------------------
    # Boom: User Visable Content (to all followers)
    #---------------------------------------------------------------------------

    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def boom(self, id, format="html"):
        # FIXME: add entry to booms table, and look that up rather than the session variable
        boomkey = 'boom%s' % id
        if boomkey in session:
            return action_error(_('already boomed this'))
        session[boomkey] = True

        content = get_content(id)
        if content.creator == c.logged_in_user:
            return action_error(_('You can not boom your own content, all your followers were already notified when you uploaded this content'))
        content.boom_to_all_followers(c.logged_in_user)

        user_log.debug("Boomed Content #%d" % int(id))
        return action_ok(_("All your followers have been informed about this content"))


    #---------------------------------------------------------------------------
    # Approve: User Visable Content (organistaion only)
    #---------------------------------------------------------------------------

    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def approve(self, id, format="html"):
        content = get_content(id)
        if content.is_parent_owner(c.logged_in_user):
            if content.lock():
                user_log.debug("Locked Content #%d" % int(id))
                return action_ok(_("content has been approved and locked"))
        return action_error(_('Error locking content'))




    #---------------------------------------------------------------------------
    # Disassociate: User Visable Content (organistaion only)
    #---------------------------------------------------------------------------

    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def disasociate(self, format="html"):
        content = get_content(id)
        if content.is_parent_owner(c.logged_in_user):
            if content.dissasociate_from_parent():
                user_log.debug("Disassociated Content #%d" % int(id))
                return action_ok(_("content has dissasociated from your content"))
        return action_error(_('Error dissasociating content'))



    #---------------------------------------------------------------------------
    # Accept: Assignment
    #---------------------------------------------------------------------------

    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def accept(self, id=None, format="html"):
        assignment = get_content(id)
        status     = assignment.accept(c.logged_in_user)
        if status == True:
            assignment.creator.send_message(messages.assignment_accepted(member=c.logged_in_user, assignment=assignment))
            user_log.debug("Accepted Content #%d" % int(id))
            return action_ok(_("_assignment accepted"))
        #elif isinstance(status,str):
        return action_error(_('Error accepting _assignment'))


    #---------------------------------------------------------------------------
    # Withdraw: from Assignment
    #---------------------------------------------------------------------------

    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def withdraw(self, id=None, format="html"):
        assignment = get_content(id)
        status     = assignment.withdraw(c.logged_in_user)
        if status == True:
            assignment.creator.send_message(messages.assignment_interest_withdrawn(member=c.logged_in_user, assignment=assignment))
            user_log.debug("Withdrew from Content #%d" % int(id))
            return action_ok(_("_assignment interest withdrawn"))
        #elif isinstance(status,str):
        #return status
        return action_error(_('Error withdrawing _assignment interest'))
