from civicboom.lib.base   import *
from civicboom.lib.search import *
from civicboom.lib.database.gis import get_engine
from civicboom.model      import Content, Member
from sqlalchemy           import or_, and_
from sqlalchemy.orm       import join

log = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# Search Filters
#-------------------------------------------------------------------------------
def _get_search_filters():
    def append_search_text(query, text):
        return query.filter(or_(Content.title.match(text), Content.content.match(text)))
    
    def append_search_location(query, location_text):
        parts = location_text.split(",")
        (lon, lat, radius) = (None, None, None)
        if len(parts) == 2:
            (lon, lat) = parts
            radius = 10
        elif len(parts) == 3:
            (lon, lat, radius) = parts
        zoom = 10 # FIXME: inverse of radius? see bug #50
        if lon and lat and radius:
            location = (lon, lat, zoom)
            return query.filter("ST_DWithin(location, 'SRID=4326;POINT(%d %d)', %d)" % (float(lon), float(lat), float(radius)))
        else:
            return query
    
    def append_search_id(query, id):
        return query.filter(Content.id==int(id))

    def append_search_type(query, type_text):
        return query.filter(Content.__type__==type_text)
    
    def append_search_creator(query, creator_text):
        try:
            return query.filter(Content.creator_id==int(creator_text))
        except:
            return query.filter(Member.username==creator_text)
    
    def append_search_response_to(query, article_id):
        return query.filter(Content.parent_id==int(article_id))

    
    search_filters = {
        'id'         : append_search_id ,
        'creator'    : append_search_creator ,
        'query'      : append_search_text ,
        'location'   : append_search_location ,
        'type'       : append_search_type ,
        'response_to': append_search_response_to ,
    }
    
    return search_filters

search_filters = _get_search_filters()


#-------------------------------------------------------------------------------
# Search Controller
#-------------------------------------------------------------------------------

class SearchController(BaseController):
    
    @auto_format_output()
    def index(self):
        return action_ok()

    @auto_format_output()
    @web_params_to_kwargs()
    def content(self, **kwargs):
        
        results  = Session.query(Content).select_from(join(Content, Member, Content.creator)).filter(and_(Content.__type__!='comment', Content.__type__!='draft', Content.status=='show', Content.private==False)).order_by(Content.id.desc()) # Setup base content search query - this is mirroed in the member propery content_public
        
        
        if 'limit' not in kwargs: #Set default limit and offset (can be overfidden by user)
            kwargs['limit'] = 20
        if 'offset' not in kwargs:
            kwargs['offset'] = 0
        if 'include_fields' not in kwargs:
            kwargs['include_fields'] = ",creator"
        if 'exclude_fields' not in kwargs:
            kwargs['exclude_fields'] = ",creator_id"
        if 'list_type' not in kwargs:
            kwargs['list_type'] = 'list'
            if c.format == 'rss':                       # Default RSS to list_with_media
                kwargs['include_fields'] += ',attachments'
        
        for key in [key for key in search_filters.keys() if key in kwargs]: # Append filters to results query based on kwarg params
            results = search_filters[key](results, kwargs[key])
        results = results.limit(kwargs['limit']).offset(kwargs['offset']) # Apply limit and offset (must be done at end)
        
        return action_ok(data={'list': [content.to_dict(kwargs['list_type'], include_fields=kwargs['include_fields'], exclude_fields=kwargs['exclude_fields']) for content in results.all()]}) # return dictionaty of content to be formatted
        
        """
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
            u = get_member(request.GET["author"])
            results = results.filter(Content.creator_id==u.id)
        
        if "response_to" in request.GET:
            cid = int(request.GET["response_to"])
            results = results.filter(Content.parent_id==cid)
        
        results = results[0:20]
        
        
        if format == "xml":
            return render("/rss/search/content.mako", extra_vars={"term":q, "location":location, "results":results})
        else:
            return render("/search/content.mako", extra_vars={"term":q, "location":location, "results":results})
        """
        

    @auto_format_output()
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


    @auto_format_output()
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
            """;
            result = connection.execute(query, [q+"%", ])
        else:
            result = []

        json_rows = [{"name":row.name, "location":row.location, "type":row.place} for row in result]
        return action_ok(data={"locations":json_rows})
