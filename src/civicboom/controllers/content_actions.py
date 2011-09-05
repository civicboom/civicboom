from civicboom.lib.base import *
from civicboom.controllers.contents import ContentsController
from civicboom.lib.communication    import messages
from cbutils.misc import update_dict

content_search = ContentsController().index

log      = logging.getLogger(__name__)


class ContentActionsController(BaseController):
    """
    Content Actions and lists relating to an item of content
    """

    #---------------------------------------------------------------------------
    # Action - Rate: Article
    #---------------------------------------------------------------------------
    @web
    @auth
    def rate(self, id, rating=0, **kwargs):
        """
        POST /contents/{id}/rate: rate an article
        @type action
        @api contents 1.0 (WIP)

        @param rating  optional int, default 0
               0       remove rating
               1-5     set rating

        @return 200   rated ok
        @return 400   invalid rating
        """
        content = get_content(id, set_html_action_fallback=True)
        content.rate(c.logged_in_persona, int(rating))
        user_log.debug("Rated Content #%d as %d" % (int(id), int(rating)))
        return action_ok(_("Vote counted"))


    #---------------------------------------------------------------------------
    # Action - Boom: User Visable Content (via boom stream)
    #---------------------------------------------------------------------------
    @web
    @auth
    def boom(self, id, **kwargs):
        """
        POST /contents/{id}/boom: alert your followers to an article
        @type action
        @api contents 1.0 (WIP)

        @return 200   boomed successfully
        """
        # AllanC: Depricated
        # FIXME: add entry to booms table, and look that up rather than the session variable
        #boomkey = 'boom%s' % id
        #if boomkey in session:
        #    raise action_error(_('already boomed this'), code=400)
        #session[boomkey] = True

        content = get_content(id, set_html_action_fallback=True)
        if content.creator == c.logged_in_persona:
            raise action_error(_('You can not boom your own content'), code=400)
        content.boom_content(c.logged_in_persona)

        user_log.debug("Boomed Content #%d" % content.id)
        return action_ok(_("Content has been Boomed"))


    #---------------------------------------------------------------------------
    # Action - Approve: Response Content (organisation only)
    #---------------------------------------------------------------------------
    @web
    @auth
    @role_required('editor')
    #@account_type('plus')
    def approve(self, id, **kwargs):
        """
        POST /contents/{id}/approve: claim an article for publishing

        @api contents 1.0 (WIP)

        @return 200   locked ok
        @return 500   error locking
        """
        content = get_content(id, is_parent_owner=True, set_html_action_fallback=True)
        if content.parent_approve():
            user_log.debug("Approved & Locked Content #%d" % int(id))
            return action_ok(_("content has been approved and locked"))
        raise action_error(_('Error locking content'))


    #---------------------------------------------------------------------------
    # Action - Disassociate: Response Content (organistaion only)
    #---------------------------------------------------------------------------
    @web
    @auth
    @role_required('editor')
    #@account_type('plus')
    def disassociate(self, id, **kwargs):
        """
        POST /contents/{id}/disassociate: unlink an article from its parent

        Useful if eg. a response is so offensive that one doesn't want it
        in the "responses" list of the request
        @type action
        @api contents 1.0 (WIP)

        @return 200   disassociated ok
        @return 500   error disassociating
        """
        content = get_content(id, is_parent_owner=True, set_html_action_fallback=True)
        if content.parent_disassociate():
            user_log.debug("Disassociated Content #%d" % int(id))
            return action_ok(_("content has disassociated from your parent content"))
        raise action_error(_('Error disassociating content'))


    #---------------------------------------------------------------------------
    # Action - Seen: Response Content (organisation only)
    #---------------------------------------------------------------------------
    @web
    @auth
    @role_required('editor')
    #@account_type('plus')
    def seen(self, id, **kwargs):
        """
        POST /contents/{id}/seen: mark response as seen
        @type action
        @api contents 1.0 (WIP)

        @return 200   seen ok
        @return 500   error
        """
        content = get_content(id, is_parent_owner=True, set_html_action_fallback=True)
        if content.parent_seen():
            user_log.debug("Seen Content #%d" % int(id))
            return action_ok(_("content has been marked as seen"))
        raise action_error(_('Error'))


    #---------------------------------------------------------------------------
    # Action - Accept: Assignment
    #---------------------------------------------------------------------------
    @web
    @auth
    @role_required('editor')
    @age_required(config['setting.age.accept'])
    def accept(self, id=None, **kwargs):
        """
        POST /contents/{id}/accept: accept an assignment
        @type action
        @api contents 1.0 (WIP)

        @return 200   accepted ok
        @return 500   error accepting
        """
        assignment = get_content(id, content_type='assignment', is_viewable=True, set_html_action_fallback=True)
        
        # AllanC - TODO: need message to user as to why they could not accept the assignment
        #         private assingment? not invited?
        #         already withdraw before so cannot accept again
        
        if assignment.accept(c.logged_in_persona):
            ## AllanC - TOTAL ballzup!!! assignment.creator.send_notification(messages.assignment_accepted(member=c.logged_in_persona, assignment=assignment, you=assignment.creator))
            user_log.debug("Accepted Content #%d" % assignment.id)
            # A convenience feature for flow of new users. If they are following nobody (they are probably a new user), then auto follow the assignment creator
            #if c.logged_in_persona.num_following <= 2:
            if c.logged_in_persona.config['auto_follow_on_accept']:
                try:
                    c.logged_in_persona.follow(assignment.creator)
                except:
                    pass #we dont care if they are already following this user.
            return action_ok(_("_assignment accepted"))
        raise action_error(_('Unable to accept _assignment'))


    #---------------------------------------------------------------------------
    # Action - Withdraw: from Assignment
    #---------------------------------------------------------------------------
    @web
    @auth
    @role_required('editor')
    def withdraw(self, id=None, **kwargs):
        """
        POST /contents/{id}/withdraw: withdraw from an assignment
        @type action
        @api contents 1.0 (WIP)

        @return 200   withdrawn ok
        @return 500   error withdrawing
        """
        assignment = get_content(id, set_html_action_fallback=True)
        
        status     = assignment.withdraw(c.logged_in_persona)
        if status == True:
            user_log.debug("Withdrew from Content #%d" % int(id))
            return action_ok(_("_assignment interest withdrawn"))
        #elif isinstance(status,str):
        #return status
        raise action_error(_('Error withdrawing _assignment interest'), code=400)


    #-----------------------------------------------------------------------------
    # Action - Flag
    #-----------------------------------------------------------------------------
    @web
    def flag(self, id, **kwargs):
        """
        POST /contents/{id}/flag: Flag this content for administrator attention
        @type action
        @api contents 1.0 (WIP)

        @param type      what the type of the problem is
               offensive
               spam
               copyright
               other
        @param comment   a text string for the user's comment
        """
        @auth
        def flag_action(id, type='offensive', comment='', **kwargs):
            get_content(id).flag(member=c.logged_in_persona, type=type, comment=comment, moderator_address=config['email.moderator'])
            user_log.debug("Flagged Content #%d as %s" % (int(id), type))
            return action_ok(_("An administrator has been alerted to this content"))
            #raise action_error(_("Error flaging content, please email us"))
        
        # AllanC - as this is a special case we can render templates if the user trys to GET data
        if request.environ['REQUEST_METHOD'] == 'GET':
            return action_ok() # This will then trigger the auto-formatter to auto select the appropiate template for the format specified
        else:
            return flag_action(id, **kwargs)


    #---------------------------------------------------------------------------
    # Action - Push to members
    #---------------------------------------------------------------------------
    @web
    @auth
    @role_required('editor')
    def push_to(self, id=None, members=[], **kwargs):
        """
        POST /contents/{id}/push_to: push this content with a notification to members
        @type action
        @api contents 1.0 (WIP)

        @param members a comma separated list of usernames that will be alerted to this content

        @return 500   error not implemented yet
        """

        raise action_error(_('not implemented'), code=500)


    #-----------------------------------------------------------------------------
    # Action - Add to Interest List
    #-----------------------------------------------------------------------------
    @web
    @auth
    def add_to_interests(self, id, **kwargs):
        """
        POST /contents/{id}/add_to_interests: Flag this content as being interesting
        @type action
        @api contents 1.0 (WIP)
        """
        c.logged_in_persona.add_to_interests(id)
        user_log.debug("Interested in Content #%d" % int(id))
        return action_ok(_("added to interest list"))


    #-----------------------------------------------------------------------------
    # List - User Actions
    #-----------------------------------------------------------------------------
    @web
    def actions(self, id, **kwargs):
        """
        GET /contents/{id}/actions: actions the current user can perform on this content
        @type list
        @api contents 1.0 (WIP)
        
        @param * (see common list return controls)
        
        @comment Allan This is a special case return and will only return an array of strings rather than a complete list object with count, offset, etc
        
        @return 200   list ok
                list  the list
        @return 404   not found
        """
        content = get_content(id, is_viewable=True)
        actions = content.action_list_for(member=c.logged_in_persona, role=c.logged_in_persona_role)
        return action_ok(data={'list': actions})


    #-----------------------------------------------------------------------------
    # List - Comments
    #-----------------------------------------------------------------------------
    @web
    def comments(self, id, **kwargs):
        """
        GET /contents/{id}/comments: Get a list of comments on the article
        @type list
        @api contents 1.0 (WIP)
        
        @return list  the list of comments
        
        @example https://test.civicboom.com/contents/1/comments.json
        """
        #content = get_content(id, is_viewable=True)
        #return to_apilist(content.comments, **kwargs)
        return content_search(comments_to=id, **kwargs)


    #-----------------------------------------------------------------------------
    # List - Accepted status
    #-----------------------------------------------------------------------------
    @web
    def accepted_status(self, id, **kwargs):
        """
        GET /contents/{id}/accepted_status: Get a list of accepted reporters
        @type list
        @api contents 1.0 (WIP)
        
        @comment Allan currently a special case and does not use the common list controls
        
        @return list  the list of comments
        """
        content = get_content(id, is_viewable=True)
        
        if hasattr(content, 'assigned_to'):
            assigned_to = [update_dict(a.member.to_dict(), {'status': a.status}) for a in content.assigned_to]  # 'update_date':a.update_date
            return to_apilist(assigned_to, obj_type='contents', **kwargs) #TODO transform
        return to_apilist()


    #-----------------------------------------------------------------------------
    # List - Responses
    #-----------------------------------------------------------------------------
    @web
    def responses(self, id, **kwargs):
        """
        GET /contents/{id}/responses: Get a list of responses

        shortcut to /contents?response_to={id}

        @type list
        @api contents 1.0 (WIP)
        """
        #content = _get_content(id, is_viewable=True)
        #if 'include_fields' not in kwargs:
        #    kwargs['include_fields']='creator'
        #return action_ok(data={'list': [c.to_dict(**kwargs) for c in content.responses]})
        return content_search(response_to=id, **kwargs)
    
    
    #-----------------------------------------------------------------------------
    # List - Contributors
    #-----------------------------------------------------------------------------
    @web
    def contributors(self, id, **kwargs):
        """
        GET /contents/{id}/contributors: Get list of contributors (unimplemented)

        shortcut to /contents?response_to={id}

        @type list
        @api contents 1.0 (WIP)
        
        @comment AllanC will currently return empty list - unimplemented
        """
        content = get_content(id, is_viewable=True)
        return to_apilist()


    #-----------------------------------------------------------------------------
    # List - Boomed by
    #-----------------------------------------------------------------------------
    @web
    def boomed_by(self, id, **kwargs):
        """
        GET /contents/{id}/boomed_by: Get list of members that have boomed this content (unimplemented)

        shortcut to /members?boomed={id}

        @type list
        @api contents 1.0 (WIP)
        
        @comment AllanC will currently return empty list - unimplemented
        """
        return to_apilist()
