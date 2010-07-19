import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from civicboom.lib.base import BaseController, render
from civicboom.lib.userlog import get_engine

log = logging.getLogger(__name__)

class EventlogController(BaseController):

    def index(self):
        #s = request.params["s"]
        connection = get_engine().connect()

        result = connection.execute(
            "SELECT * FROM events ORDER BY date_sent DESC"
        )
        #return "\n<p>".join([", ".join([str(col) for col in row]) for row in result])
        return render("eventlog.mako", extra_vars={"events": list(result)})
