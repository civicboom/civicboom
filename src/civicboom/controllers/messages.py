
from civicboom.lib.base import *
from pylons.i18n.translation  import _ # FIXME: not included by "*" above? see bug #51
from civicboom.model import Message
import json

log = logging.getLogger(__name__)
user_log = logging.getLogger("user")

class MessagesController(BaseController):

    @authorize(is_valid_user)
    def index(self, format="html"):
        c.viewing_user = c.logged_in_user
        if format == "json":
            return json.dumps({
                "status": "ok",
                "data": [{
                    "id": m.id,
                    "subject": m.subject,
                } for m in c.viewing_user.messages_to]
            })
        else:
            return render("/web/messages/index.mako")

    @authorize(is_valid_user)
    def read(self, id, format="html"):
        c.viewing_user = c.logged_in_user
        msg = Session.query(Message).filter(Message.id==id).one()
        if msg.target == c.viewing_user: # FIXME messages to groups?
            c.msg = msg
        else:
            abort(403, "You are not the target of this message")

        if format == "json":
            return json.dumps({
                "status": "ok",
                "data": {
                    "id": c.msg.id,
                    "subject": c.msg.subject,
                    "content": c.msg.content,
                }
            })
        else:
            return render("/web/messages/read.mako")

    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def send(self):
        try:
            target = get_user(request.POST["target"])
            if not target:
                # FIXME: form validator to refresh with the same values?
                return action_error(_("Can't find user '%s'") % request.POST["target"])
            m = Message()
            m.source_id = c.logged_in_user.id # FIXME: or from any group they are admin of?
            m.target_id = target.id
            m.subject = request.POST["subject"]
            m.content = request.POST["content"]
            # FIXME: send a notification too?
            user_log.debug("Sending message to User #%d (%s)" % (target.id, target.username))
            Session.add(m)
            Session.commit()
            return action_ok(_("Message sent"))
        except Exception, e:
            log.exception("Error sending message:")
            return action_error(_("Error sending message"))

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
            return action_ok(_("Message deleted"))
        else:
            user_log.warning("User tried to delete somebody else's message") # FIXME: details
            return action_error(_("You are not the target of this message"))
            # FIXME: flash_message should be red? abort(403, "You are not the target of this message")

