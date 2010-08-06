import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from civicboom.model.meta import Session
from civicboom.model import Message
from civicboom.lib.base import BaseController, render

log = logging.getLogger(__name__)

class MessagesController(BaseController):

    def index(self):
        c.viewing_user = c.logged_in_user
        return render("/web/messages/index.mako")

    def read(self, id):
        c.viewing_user = c.logged_in_user
        msg = Session.query(Message).filter(Message.id==id).one()
        if msg.target == c.viewing_user: # FIXME messages to groups?
            c.msg = msg
        else:
            die("You are not the target of this message")
        return render("/web/messages/read.mako")
