from civicboom.lib.base   import *
from civicboom.lib.search import *
from civicboom.lib.database.gis import get_engine
from civicboom.model      import Content, Member
from sqlalchemy           import or_, and_
from sqlalchemy.orm       import join

log = logging.getLogger(__name__)



#-------------------------------------------------------------------------------
# Search Controller
#-------------------------------------------------------------------------------

class SearchController(BaseController):

    @auto_format_output
    def content2(self, format="html"):
        results = Session.query(Content)
        query = AndFilter([
            OrFilter([
                TextFilter("terrorists"),
                AndFilter([
                    LocationFilter([1, 51], 10),
                    TagFilter("Science & Nature")
                ]),
                AuthorFilter("unittest")
            ]),
            NotFilter(OrFilter([
                TextFilter("waffles"),
                TagFilter("Business")
            ]))
        ])
        results = results.filter(sql(query))
        results = results[0:20]

        return action_ok(data={"term":"moo", "location":"location", "results":results})


    @auto_format_output
    def location(self, format="html"):
        """
        Used in location autocomplete
        """
        if "term" in request.GET:
            q = request.GET["term"]
            connection = get_engine().connect()
            query = """
                SELECT name, ST_AsText(way) AS location, place
                FROM osm_point
                WHERE
                    name ILIKE %s
                    AND place IS NOT NULL -- IN ('city')
                    AND ST_DWithin(way, 'SRID=4326;POINT(-3 54)', 10)
                LIMIT 20
            """
            result = connection.execute(query, [q+"%", ])
        else:
            result = []

        json_rows = [{"name":row.name, "location":row.location, "type":row.place} for row in result]
        return action_ok(data={"locations":json_rows})
