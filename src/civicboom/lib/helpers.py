"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from civicboom.model.meta import LogSession
from sqlalchemy.sql import text
from pylons import request, response, session, tmpl_context as c, url
import logging


class UserLogger:
    def __init__(self, module):
        self.module = module
        #self.ulog = logging.getLogger("user")
        #self.ulog.

    def info(self, msg):
        #self.ulog.info("Anonymous ("+request.environ["REMOTE_ADDR"]+"): "+request.url+" - "+text)
        #if c.has_key("username"):
        #    username = c.username
        username = "None"
        url = request.url
        addr = request.environ["REMOTE_ADDR"]

        sess = LogSession()
        conn = sess.connection()
        conn.execute(text("""
            INSERT INTO events(module, username, url, address, priority, message)
            VALUES(:module, :username, :url, :address, :priority, :message)
        """), module=self.module, username=username, url=url, address=addr, priority=logging.INFO, message=msg)
        sess.commit()

