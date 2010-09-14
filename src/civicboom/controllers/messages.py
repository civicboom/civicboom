
from civicboom.lib.base import *
from civicboom.model import Message
import json

log = logging.getLogger(__name__)
user_log = logging.getLogger("user")

class MessagesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py file has
    # a resource setup:
    #     map.resource('message', 'messages')


    @authorize(is_valid_user)
    def index(self, format='html'):
        """GET /: All items in the collection."""
        # url('messages')
        c.viewing_user = c.logged_in_user
        if format == "json":
            return action_ok(
                data = [{
                    "id": m.id,
                    "subject": m.subject,
                } for m in c.viewing_user.messages_to]
            )
        else:
            return render("/web/messages/index.mako")


    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def create(self):
        """POST /: Create a new item."""
        # url('messages')
        try:
            target = get_user(request.POST["target"])
            if not target:
                # FIXME: form validator to refresh with the same values?
                return action_error(_("Can't find user '%s'") % request.POST["target"], code=404)
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


    def new(self, format='html'):
        """GET /new: Form to create a new item."""
        # url('new_message')
        pass


    def update(self, id):
        """PUT /id: Update an existing item."""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(h.url('message', id=ID), method='put')
        # url('message', id=ID)
        pass


    @authorize(is_valid_user)
    @authenticate_form
    @action_redirector()
    def delete(self, id):
        """DELETE /id: Delete an existing item."""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(h.url('message', id=ID), method='delete')
        # url('message', id=ID)
        c.viewing_user = c.logged_in_user
        msg = Session.query(Message).filter(Message.id==int(id)).one()
        redir = None
        if msg.target == c.viewing_user: # FIXME messages to groups?
            # FIXME: test that delete-orphan works, and removes the
            # de-parented message
            if msg.source: # source exists = message, no source = notification
                user_log.debug("Deleting message")
                c.viewing_user.messages_to.remove(msg)
            else:
                user_log.debug("Deleting notification")
                c.viewing_user.messages_notification.remove(msg)
            Session.commit()
            return action_ok(_("Message deleted"))
        else:
            user_log.warning("User tried to delete somebody else's message") # FIXME: details
            return action_error(_("You are not the target of this message"), code=403)


    @authorize(is_valid_user)
    @auto_format_output()
    def show(self, id, format='html'):
        """GET /id: Show a specific item."""
        # url('message', id=ID)
        c.viewing_user = c.logged_in_user
        msg = Session.query(Message).filter(Message.id==id).one()
        if msg.target == c.viewing_user: # FIXME messages to groups?
            c.msg = msg
        else:
            return action_error(_("You are not the target of this message"), code=403)

        if format == "json":
            return action_ok(
                data = {
                    "id": c.msg.id,
                    "subject": c.msg.subject,
                    "content": c.msg.content,
                }
            )
        else:
            return render("/web/messages/read.mako")


    def edit(self, id, format='html'):
        """GET /id;edit: Form to edit an existing item."""
        # url('edit_message', id=ID)
        pass
