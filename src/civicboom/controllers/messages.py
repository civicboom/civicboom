import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators.secure import authenticate_form

from civicboom.lib.authentication      import authorize, is_valid_user
from civicboom.model.meta import Session
from civicboom.model import Message
from civicboom.lib.base import BaseController, render

log = logging.getLogger(__name__)

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
            die("You are not the target of this message")
        return render("/web/messages/read.mako")

    @authorize(is_valid_user)
    @authenticate_form
    def send(self):
        # FIXME implement this
        pass

    @authorize(is_valid_user)
    @authenticate_form
    def delete(self):
        c.viewing_user = c.logged_in_user
        msg = Session.query(Message).filter(Message.id==request.POST["msg_id"]).one()
        if msg.target == c.viewing_user: # FIXME messages to groups?
            # FIXME: test that delete-orphan works, and removes the
            # de-parented message
            c.viewing_user.messages_to.remove(msg)
            Session.commit()
        else:
            die("You are not the target of this message")
        return redirect(url.current(action='index'))

