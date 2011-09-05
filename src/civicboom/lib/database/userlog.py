
from pylons import config, request, tmpl_context as c

from sqlalchemy import engine_from_config
from sqlalchemy.sql import text

from uuid import uuid1 as uuid
import logging
import platform

log_engine = None


def get_engine():
    global log_engine
    if not log_engine:
        log_engine = engine_from_config(config, 'sqlalchemy.log.')
    return log_engine


class UserLogHandler(logging.Handler):
    def emit(self, record):
        id = uuid()
        node = platform.node()
        username = "None"
        persona = "None"
        if hasattr(c, "logged_in_user") and c.logged_in_user:
            username = c.logged_in_user.id
        if hasattr(c, "logged_in_persona") and c.logged_in_persona:
            persona = c.logged_in_persona.id
        url      = request.url
        addr     = request.environ["REMOTE_ADDR"]
        priority = record.levelno
        module   = record.pathname[record.pathname.find("civicboom"):]
        line_num = record.lineno
        message  = record.getMessage()

        get_engine().execute(text("""
            INSERT INTO events(id, node, module, line_num, username, persona, url, address, priority, message)
            VALUES(:id, :node, :module, :line_num, :username, :persona, :url, :address, :priority, :message)
        """), id=str(id), node=node, module=module, line_num=line_num, username=username, persona=persona, url=url, address=addr, priority=priority, message=message)
