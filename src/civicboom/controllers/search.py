from civicboom.lib.base   import *
from civicboom.lib.database.gis import find_locations
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
            result = find_locations(request.GET["term"])
        else:
            result = []

        json_rows = [{"name": "%s (%s)" % (row.name, row.county), "location": row.location, "type": row.type} for row in result]
        return action_ok(data={"locations":json_rows})
