from civicboom.lib.base   import *
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
    def location(self, format="html"):
        """
        Used in location autocomplete
        """
        if "term" in request.GET:
            q = request.GET["term"]
            connection = get_engine().connect()
            query = """
                SELECT
                    t.name as name,
                    ST_AsText(t.way) AS location,
                    t.place as place,
                    (
                        SELECT c.name AS county
                        FROM osm_point c
                        WHERE c.place='county'
                        ORDER BY ST_Distance(t.way, c.way)
                        LIMIT 1
                    ) AS county
                FROM
                    osm_point t
                WHERE
                    t.name ILIKE %s
                    AND t.place is not null
            """
            result = connection.execute(query, [q+"%", ])
        else:
            result = []

        json_rows = [{"name": "%s (%s)" % (row.name, row.county), "location": row.location, "type": row.place} for row in result]
        return action_ok(data={"locations":json_rows})
