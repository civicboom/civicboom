from civicboom.lib.base import *
from civicboom.controllers.contents import _get_content

from civicboom.lib.communication       import messages

log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")


class ContentActionsController(BaseController):
    """
    Content Actions
    """

    #---------------------------------------------------------------------------
    # Rate: Article
    #---------------------------------------------------------------------------
    @auto_format_output
    @web_params_to_kwargs
    @authorize(is_valid_user)
    @authenticate_form
    def rate(self, id, rating=None):
        """
        POST /contents/{id}/rate: rate an article

        @api contents 1.0 (WIP)

        @param rating  optional int, default 0
               0       remove rating
               1-5     set rating

        @return 200   rated ok
        @return 400   invalid rating
        """
        content = _get_content(id)
        content.rate(c.logged_in_persona, int(rating))
        user_log.debug("Rated Content #%d as %d" % (int(id), int(rating)))
        return action_ok(_("Vote counted"))


    #---------------------------------------------------------------------------
    # Boom: User Visable Content (to all followers)
    #---------------------------------------------------------------------------

    @auto_format_output
    @authorize(is_valid_user)
    @authenticate_form
    def boom(self, id, format="html"):
        """
        POST /contents/{id}/boom: alert your followers to an article

        @api contents 1.0 (WIP)

        @return 200   boomed successfully
        """
        # FIXME: add entry to booms table, and look that up rather than the session variable
        boomkey = 'boom%s' % id
        if boomkey in session:
            raise action_error(_('already boomed this'), code=400)
        session[boomkey] = True

        content = _get_content(id)
        if content.creator == c.logged_in_persona:
            raise action_error(_('You can not boom your own content, all your followers were already notified when you uploaded this content'))
        content.boom_to_all_followers(c.logged_in_persona)

        user_log.debug("Boomed Content #%d" % int(id))
        return action_ok(_("All your followers have been informed about this content"))


    #---------------------------------------------------------------------------
    # Approve: Response Content (organisation only)
    #---------------------------------------------------------------------------

    @auto_format_output
    @authorize(is_valid_user)
    @authenticate_form
    def approve(self, id):
        """
        POST /contents/{id}/approve: claim an article for publishing

        @api contents 1.0 (WIP)

        @return 200   locked ok
        @return 500   error locking
        """
        content = _get_content(id, is_parent_owner=True)
        if content.parent_approve():
            user_log.debug("Approved & Locked Content #%d" % int(id))
            return action_ok(_("content has been approved and locked"))
        raise action_error(_('Error locking content'))



    #---------------------------------------------------------------------------
    # Disassociate: Response Content (organistaion only)
    #---------------------------------------------------------------------------

    @auto_format_output
    @authorize(is_valid_user)
    @authenticate_form
    def disasociate(self, id):
        """
        POST /contents/{id}/disassociate: unlink an article from its parent

        Useful if eg. a response is so offensive that one doesn't want it
        in the "responses" list of the request

        @api contents 1.0 (WIP)

        @return 200   disassociated ok
        @return 500   error disassociating
        """
        content = _get_content(id, is_parent_owner=True)
        if content.parent_dissasociate():
            user_log.debug("Disassociated Content #%d" % int(id))
            return action_ok(_("content has dissasociated from your parent content"))
        raise action_error(_('Error dissasociating content'))


    #---------------------------------------------------------------------------
    # Seen: Response Content (organisation only)
    #---------------------------------------------------------------------------

    @auto_format_output
    @authorize(is_valid_user)
    @authenticate_form
    def seen(self, id):
        """
        POST /contents/{id}/seen: mark response as seen

        @api contents 1.0 (WIP)

        @return 200   seen ok
        @return 500   error
        """
        content = _get_content(id, is_parent_owner=True)
        if content.parent_seen():
            user_log.debug("Seen Content #%d" % int(id))
            return action_ok(_("content has been marked as seen"))
        raise action_error(_('Error'))


    #---------------------------------------------------------------------------
    # Accept: Assignment
    #---------------------------------------------------------------------------

    @auto_format_output
    @authorize(is_valid_user)
    @authenticate_form
    def accept(self, id=None):
        """
        POST /contents/{id}/accept: accept an assignment

        @api contents 1.0 (WIP)

        @return 200   accepted ok
        @return 500   error accepting
        """
        assignment = _get_content(id)
        status     = assignment.accept(c.logged_in_persona)
        # AllanC - TODO: need message to user as to why they could not accept the assignment
        #         private assingment? not invited?
        #         already withdraw before so cannot accept again
        if status == True:
            assignment.creator.send_message(messages.assignment_accepted(member=c.logged_in_persona, assignment=assignment))
            user_log.debug("Accepted Content #%d" % int(id))
            return action_ok(_("_assignment accepted"))
        #elif isinstance(status,str):
        raise action_error(_('Error accepting _assignment'), code=400)


    #---------------------------------------------------------------------------
    # Withdraw: from Assignment
    #---------------------------------------------------------------------------

    @auto_format_output
    @authorize(is_valid_user)
    @authenticate_form
    def withdraw(self, id=None):
        """
        POST /contents/{id}/witdraw: withdraw from an assignment

        @api contents 1.0 (WIP)

        @return 200   withdrawn ok
        @return 500   error withdrawing
        """
        assignment = _get_content(id)
        status     = assignment.withdraw(c.logged_in_persona)
        if status == True:
            user_log.debug("Withdrew from Content #%d" % int(id))
            return action_ok(_("_assignment interest withdrawn"))
        #elif isinstance(status,str):
        #return status
        raise action_error(_('Error withdrawing _assignment interest'), code=400)


    #-----------------------------------------------------------------------------
    # Flag
    #-----------------------------------------------------------------------------
    @auto_format_output
    @web_params_to_kwargs
    @authorize(is_valid_user)
    @authenticate_form
    def flag(self, id, type='offensive', comment=''):
        """
        POST /contents/{id}/flag: Flag this content as being inapproprate of copyright violoation

        @api contents 1.0 (WIP)

        @param type      ?
        @param comment   ?
        """
        _get_content(id).flag(member=c.logged_in_persona, type=type, comment=comment)
        user_log.debug("Flagged Content #%d as %s" % (int(id), type))
        return action_ok(_("An administrator has been alerted to this content"))
        #raise action_error(_("Error flaging content, please email us"))



    #-----------------------------------------------------------------------------
    # Add to Interest List
    #-----------------------------------------------------------------------------
    @auto_format_output
    @authorize(is_valid_user)
    @authenticate_form
    def add_to_interests(self, id):
        """
        POST /contents/{id}/add_to_interests: Flag this content as being interesting
        
        @api contents 1.0 (WIP)
        """
        c.logged_in_persona.add_to_interests(id)
        user_log.debug("Interested in Content #%d" % int(id))
        return action_ok(_("added to interest list"))
