
from civicboom.lib.base   import *
from civicboom.lib.search import *
from civicboom.lib.gis    import get_engine
from civicboom.model      import Content, Member
from sqlalchemy           import or_
import json

log = logging.getLogger(__name__)
tmpl_prefix = '/web/design09'


class SearchController(BaseController):
    def index(self):
        return render(tmpl_prefix+"/search/index.mako")

    @auto_format_output()
    def content(self, format="html"):
        results = Session.query(Content)

        if "query" in request.GET:
            q = request.GET["query"]
            results = results.filter(or_(Content.title.match(q), Content.content.match(q)))
        else:
            q = None

        if "location" in request.GET:
            location = request.GET["location"]
            parts = location.split(",")
            (lon, lat, radius) = (None, None, None)
            if len(parts) == 2:
                (lon, lat) = parts
                radius = 10
            elif len(parts) == 3:
                (lon, lat, radius) = parts
            zoom = 10 # FIXME: inverse of radius? see bug #50
            if lon:
                location = (lon, lat, zoom)
                results = results.filter("ST_DWithin(location, 'SRID=4326;POINT(%d %d)', %d)" % (float(lon), float(lat), float(radius)))
        else:
            location = None

        if "type" in request.GET:
            t = request.GET["type"]
            results = results.filter(Content.__type__==t)

        if "author" in request.GET:
            u = get_user(request.GET["author"])
            results = results.filter(Content.creator_id==u.id)

        if "response_to" in request.GET:
            cid = int(request.GET["response_to"])
            results = results.filter(Content.parent_id==cid)

        results = results[0:20]

        if format == "xml":
            return render("/rss/search/content.mako", extra_vars={"term":q, "location":location, "results":results})
        else:
            return render(tmpl_prefix+"/search/content.mako", extra_vars={"term":q, "location":location, "results":results})

    def content2(self, format="html"):
        results = Session.query(Content)

        query = AndFilter([
            OrFilter([
                TextFilter("terrorists"),
                AndFilter([
                    LocationFilter("canterbury"),
                    TagFilter("Science & Nature")
                ]),
                AuthorFilter("unittest")
            ]),
            NotFilter(OrFilter([
                TextFilter("waffles"),
                TagFilter("Business")
            ]))
        ])
        results = results.filter(unicode(query))

        results = results[0:20]

        if format == "xml":
            return render("/rss/search/content.mako", extra_vars={"term":q, "location":location, "results":results})
        else:
            return render(tmpl_prefix+"/search/content.mako", extra_vars={"term":q, "location":location, "results":results})


    @auto_format_output()
    def location(self, format="html"):
        if "term" in request.GET:
            q = request.GET["term"]
            connection = get_engine().connect()
            query = """
                SELECT name, ST_AsText(location) AS location, type
                FROM places
                WHERE
                    name ILIKE %s
                    AND ST_DWithin(location, 'SRID=4326;POINT(-3 54)', 10)
                LIMIT 20
            """;
            result = connection.execute(query, [q+"%", ])
        else:
            result = []

        if format == "html":
            return render(tmpl_prefix+"/search/location.mako")
        elif format == "json":
            json_rows = [{"name":row.name, "location":row.location, "type":row.type} for row in result]
            return action_ok(data={"locations":json_rows})


    @auto_format_output()
    def member(self, format="html"):
        if "term" in request.GET:
            s = request.GET["term"]
            q = Session.query(Member)
            q = q.filter(or_(Member.name.ilike("%"+s+"%"), Member.username.ilike("%"+s+"%")))
            result = q[0:20]
        else:
            result = []

        if format == "html":
            return render(tmpl_prefix+"/search/member.mako")
        elif format == "json":
            json_rows = [{"id":row.id, "name":row.name, "username":row.username, "avatar":row.avatar, "description":str(row)} for row in result]
            return action_ok(data={"members":json_rows})
