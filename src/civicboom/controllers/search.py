import logging
import json

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from civicboom.lib.base import BaseController, render
from civicboom.lib.gis  import get_engine
from civicboom.model.content           import Content, DraftContent
from civicboom.model.meta              import Session
from sqlalchemy                        import or_

log = logging.getLogger(__name__)
tmpl_prefix = '/web/design09'

class SearchController(BaseController):
    def index(self):
        # Return a rendered template
        #return render('/search.mako')
        # or, return a string
        return 'Hello World. Search for: [box]'

    def content(self, id=None):
        if not id:
            return redirect(url(controller='search', action='index'))
        results = Session.query(Content).filter(or_(Content.title.match(id), Content.content.match(id)))
        return render(tmpl_prefix+"/search/content.mako", extra_vars={"term": id, "results":results})

    def location(self, format="html"):
        if "query" in request.GET:
            q = request.GET["query"]
            connection = get_engine().connect()
            query = """
                SELECT name, ST_AsText(location) AS location, type
                FROM places
                WHERE
                    name ILIKE %s
                    AND ST_DWithin(location, 'POINT(54 -3)', 10)
                LIMIT 20
            """;
            result = connection.execute(query, [q+"%", ])
        else:
            result = []

        if format == "html":
            return render(tmpl_prefix+"/search/location.mako")
        elif format == "json":
            json_rows = [{"name":row.name,"location":row.location,"type":row.type} for row in result]
            return json.dumps({"ResultSet": {"Results": json_rows}})
