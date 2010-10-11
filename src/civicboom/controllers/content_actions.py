"""
Actions
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
    def rate(self, id, format="html"):
        """
        POST /contents/{id}/rate - rate an article

        @param rating (optional int, default 0)
          0   - remove rating
          1-5 - set rating

        @return 200 - rated ok
        @return 400 - invalid rating
        """
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
            if rating < 0 or rating > 5:
                raise action_error(_("Ratings can only be in the range 0 to 5"), code=400)

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
    def boom(self, id, format="html"):
        """
        POST /contents/{id}/boom - alert your followers to an article

        @return 200 - boomed successfully
        """
        # FIXME: add entry to booms table, and look that up rather than the session variable
        boomkey = 'boom%s' % id
        if boomkey in session:
            raise action_error(_('already boomed this'))
        session[boomkey] = True

        content = get_content(id)
        if content.creator == c.logged_in_user:
            raise action_error(_('You can not boom your own content, all your followers were already notified when you uploaded this content'))
        content.boom_to_all_followers(c.logged_in_user)

        user_log.debug("Boomed Content #%d" % int(id))
        return action_ok(_("All your followers have been informed about this content"))


    #---------------------------------------------------------------------------
    # Approve: User Visable Content (organisation only)
    #---------------------------------------------------------------------------

    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def approve(self, id, format="html"):
        """
        POST /contents/{id}/approve - claim an article for publishing

        @return 200 - locked ok
        @return 500 - error locking
        """
        content = get_content(id)
        if content.is_parent_owner(c.logged_in_user):
            if content.lock():
                user_log.debug("Locked Content #%d" % int(id))
                return action_ok(_("content has been approved and locked"))
        raise action_error(_('Error locking content'))




    #---------------------------------------------------------------------------
    # Disassociate: User Visable Content (organistaion only)
    #---------------------------------------------------------------------------

    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def disasociate(self, format="html"):
        """
        POST /contents/{id}/disassociate - unlink an article from its parent

        Useful if eg. a response is so offensive that one doesn't want it
        in the "responses" list of the request

        @return 200 - disassociated ok
        @return 500 - error disassociating
        """
        content = get_content(id)
        if content.is_parent_owner(c.logged_in_user):
            if content.dissasociate_from_parent():
                user_log.debug("Disassociated Content #%d" % int(id))
                return action_ok(_("content has dissasociated from your content"))
        raise action_error(_('Error dissasociating content'))



    #---------------------------------------------------------------------------
    # Accept: Assignment
    #---------------------------------------------------------------------------

    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def accept(self, id=None, format="html"):
        """
        POST /contents/{id}/accept - accept an assignment

        @return 200 - accepted ok
        @return 500 - error accepting
        """
        assignment = get_content(id)
        status     = assignment.accept(c.logged_in_user)
        if status == True:
            assignment.creator.send_message(messages.assignment_accepted(member=c.logged_in_user, assignment=assignment))
            user_log.debug("Accepted Content #%d" % int(id))
            return action_ok(_("_assignment accepted"))
        #elif isinstance(status,str):
        raise action_error(_('Error accepting _assignment'))


    #---------------------------------------------------------------------------
    # Withdraw: from Assignment
    #---------------------------------------------------------------------------

    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def withdraw(self, id=None, format="html"):
        """
        POST /contents/{id}/witdraw - withdraw from an assignment

        @return 200 - withdrawn ok
        @return 500 - error withdrawing
        """
        assignment = get_content(id)
        status     = assignment.withdraw(c.logged_in_user)
        if status == True:
            assignment.creator.send_message(messages.assignment_interest_withdrawn(member=c.logged_in_user, assignment=assignment))
            user_log.debug("Withdrew from Content #%d" % int(id))
            return action_ok(_("_assignment interest withdrawn"))
        #elif isinstance(status,str):
        #return status
        raise action_error(_('Error withdrawing _assignment interest'))


    #-----------------------------------------------------------------------------
    # Flag
    #-----------------------------------------------------------------------------
    @auto_format_output()
    @authorize(is_valid_user)
    @authenticate_form
    def flag(self, id):
        """
        POST /contents/{id}/flag - Flag this content as being inapproprate of copyright violoation

        @param type - ?
        @param comment - ?
        """
        form = request.POST
        try:
            get_content(id).flag(member=c.logged_in_user, type=form['type'], comment=form['comment'])
            return action_ok(_("An administrator has been alerted to this content"))
        except:
            raise action_error(_("Error flaging content, please email us"))
