
from civicboom.lib.base   import *
from civicboom.lib.search import *
from civicboom.lib.database.gis import get_engine
from civicboom.model      import Content, Member
from sqlalchemy           import or_
from sqlalchemy.orm       import join

log = logging.getLogger(__name__)
tmpl_prefix = '/web/design09'

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
        if lon:
            location = (lon, lat, zoom)
            return query.filter("ST_DWithin(location, 'SRID=4326;POINT(%d %d)', %d)" % (float(lon), float(lat), float(radius)))
    
    def append_search_type(query, type_text):
        return query.filter(Content.__type__==type_text)
    
    def append_search_creator(query, creator_text):
        try:
            return query.filter(Content.creator_id==int(creator_text))
        except:
            return query.select_from(join(Content, Member, Content.creator)).filter(Member.username==creator_text)
    
    def append_search_response_to(query, article_id):
        query = query.filter(Content.parent_id==int(article_id))
        
    #def append_search_limit(query, limit):
    #    print "limit"
    #    return query.limit(limit)
    
    search_filters = {
        'query'      : append_search_text ,
        'location'   : append_search_location ,
        'type'       : append_search_type ,
        'creator'    : append_search_creator ,
        'response_to': append_search_response_to ,
    #    'limit'      : append_search_limit ,
    }
    
    return search_filters

search_filters = _get_search_filters()


#-------------------------------------------------------------------------------
# Search Controller
#-------------------------------------------------------------------------------

class SearchController(BaseController):
    
    def index(self):
        return render(tmpl_prefix+"/search/index.mako")

    @auto_format_output()
    def content(self, **kwargs):
        kwargs.update(request.GET) # Update the kwargs with request params from query string
        
        results  = Session.query(Content).filter(Content.__type__!='comment').order_by(Content.id.desc()) # Setup base content search query
        
        if 'limit' not in kwargs: #Set default limit and offset (can be overfidden by user)
            kwargs['limit'] = 20
        if 'offset' not in kwargs:
            kwargs['offset'] = 0
        
        for key in [key for key in search_filters.keys() if key in kwargs]: # Append filters to results query based on kwarg params
            results = search_filters[key](results, kwargs[key])
        results = results.limit(kwargs['limit']).offset(kwargs['offset']) # Apply limit and offset (must be done at end)
        
        return {'data': {'list': [content.to_dict('list') for content in results.all()]}} # return dictionaty of content to be formatted
        
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
        """
        

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

        if format == "xml":
            return render("/rss/search/content.mako", extra_vars={"term":"moo", "location":"location", "results":results})
        else:
            return render(tmpl_prefix+"/search/content.mako", extra_vars={"term":"moo", "location":"location", "results":results})


    @auto_format_output()
    def location(self, format="html"):
        """
        Used in location autocomplete
        """
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
