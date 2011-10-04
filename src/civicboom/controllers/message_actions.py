from civicboom.lib.base import *
from civicboom.lib.database.get_cached import get_message

log = logging.getLogger(__name__)


class MessageActionsController(BaseController):
    """
    Actions and lists that can be performed on a message
    """

    #-----------------------------------------------------------------------------
    # Action - Flag
    #-----------------------------------------------------------------------------
    @web
    def flag(self, id, **kwargs):
        """
        POST /members/{id}/flag: Flag this content for administrator attention
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
            get_message(id).flag(raising_member=c.logged_in_user, type=type, comment=comment, moderator_address=config['email.moderator'])
            user_log.debug("Flagged Message #%d as %s" % (int(id), type))
            return action_ok(_("An administrator has been alerted to this member"))
        
        # AllanC - as this is a special case we can render templates if the user trys to GET data
        if request.environ['REQUEST_METHOD'] == 'GET':
            return action_ok() # This will then trigger the auto-formatter to auto select the appropiate template for the format specified
        else:
            return flag_action(id, **kwargs)

