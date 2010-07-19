import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from civicboom.lib.base import BaseController, render
from civicboom.lib.userlog import get_engine

log = logging.getLogger(__name__)

class EventlogController(BaseController):

    def index(self):
        # Old-fashioned SQL building since events aren't part of the
        # SQLAlchemy model; beware of SQL injection
        # FIXME: make this do something...
        wheres = ["1=1", ]
        args = []
        if "module" in request.params:
            wheres.append("module = %s")
            args.append(request.params["module"])
        if "username" in request.params:
            wheres.append("username = %s")
            args.append(request.params["username"])
        if "address" in request.params:
            wheres.append("address = %s")
            args.append(request.params["address"])

        connection = get_engine().connect()
        query = "SELECT * FROM events WHERE "
        where = " AND ".join(wheres)
        order = " ORDER BY date_sent DESC"
        result = connection.execute(query + where + order, args)
        return render("eventlog.mako", extra_vars={"events": list(result)})
