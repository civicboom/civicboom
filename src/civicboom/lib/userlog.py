
from pylons import config
from pylons import request, response, session, tmpl_context as c, url

from sqlalchemy import engine_from_config
from sqlalchemy.sql import text

import logging

class UserLogHandler(logging.Handler):
    db_engine = None

    def emit(self, record):
        if not self.db_engine:
            self.db_engine = engine_from_config(config, 'sqlalchemy.log.')

        #if c.has_key("username"):
        #    username = c.username
        username = "None"
        url = request.url
        addr = request.environ["REMOTE_ADDR"]
        priority = record.levelno
        module = record.pathname[record.pathname.find("civicboom"):] # +":"+str(record.lineno)
        message = record.getMessage()

        connection = self.db_engine.connect()
        connection.execute(text("""
            INSERT INTO events(module, username, url, address, priority, message)
            VALUES(:module, :username, :url, :address, :priority, :message)
        """), module=module, username=username, url=url, address=addr, priority=priority, message=message)
        # connection.commit()
        connection.close()

