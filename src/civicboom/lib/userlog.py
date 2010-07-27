
from pylons import config
from pylons import request, response, session, tmpl_context as c, url

from sqlalchemy import engine_from_config
from sqlalchemy.sql import text

import logging

log_engine = None

def get_engine():
    global log_engine
    if not log_engine:
        log_engine = engine_from_config(config, 'sqlalchemy.log.')
    return log_engine

class UserLogHandler(logging.Handler):
    def emit(self, record):
        db_engine = get_engine()

        username = "None"
        if c.logged_in_user:
            username = c.logged_in_user.username
        url      = request.url
        addr     = request.environ["REMOTE_ADDR"]
        priority = record.levelno
        module   = record.pathname[record.pathname.find("civicboom"):]
        line_num = record.lineno
        message  = record.getMessage()

        connection = db_engine.connect()
        connection.execute(text("""
            INSERT INTO events(module, line_num, username, url, address, priority, message)
            VALUES(:module, :line_num, :username, :url, :address, :priority, :message)
        """), module=module, line_num=line_num, username=username, url=url, address=addr, priority=priority, message=message)
        # connection.commit()
        connection.close()

