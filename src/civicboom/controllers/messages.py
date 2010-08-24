
from civicboom.lib.base import *
from civicboom.model import Message

log = logging.getLogger(__name__)
user_log = logging.getLogger("user")

class MessagesController(BaseController):

    @authorize(is_valid_user)
    def index(self):
        c.viewing_user = c.logged_in_user
        return render("/web/messages/index.mako")

    @authorize(is_valid_user)
    def read(self, id):
        c.viewing_user = c.logged_in_user
        msg = Session.query(Message).filter(Message.id==id).one()
        if msg.target == c.viewing_user: # FIXME messages to groups?
            c.msg = msg
        else:
            abort(403, "You are not the target of this message")
        return render("/web/messages/read.mako")

    @authorize(is_valid_user)
    @authenticate_form
    def send(self):
        # FIXME implement this
        pass

    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def delete(self):
        c.viewing_user = c.logged_in_user
        msg = Session.query(Message).filter(Message.id==request.POST["msg_id"]).one()
        redir = None
        if msg.target == c.viewing_user: # FIXME messages to groups?
            # FIXME: test that delete-orphan works, and removes the
            # de-parented message
            if request.POST["type"] == "message":
                user_log.debug("Deleting message")
                c.viewing_user.messages_to.remove(msg)
                Session.commit() # commit must come before the redirect is generated?
            if request.POST["type"] == "notification":
                user_log.debug("Deleting notification")
                c.viewing_user.messages_notification.remove(msg)
                Session.commit() # commit must come before the redirect is generated?
            return _("Message deleted")
        else:
            user_log.warning("User tried to delete somebody else's message") # FIXME: details
            return _("You are not the target of this message")
            # FIXME: flash_message should be red? abort(403, "You are not the target of this message")

