"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # CUSTOM ROUTES HERE
    map.connect('/', controller='misc', action='titlepage')
    map.resource('message', 'messages')
    map.resource('setting', 'settings')
    map.resource('content', 'contents')
    map.connect('content_action', '/contents/{id}/{action}.{format}', controller='content_actions')
    map.connect('content_action', '/contents/{id}/{action}', controller='content_actions', format="redirect")
    map.resource('feed',    'feeds'   )


    # Map the /admin url to FA's AdminController
    # Map static files  
    map.connect('fa_static', '/admin/_static/{path_info:.*}', controller='admin', action='static')
    # Index page
    map.connect('admin', '/admin', controller='admin', action='models')
    map.connect('formatted_admin', '/admin.json', controller='admin', action='models', format='json')
    # Models
    map.resource('model', 'models', path_prefix='/admin/{model_name}', controller='admin')


    # Redirects were eating form posts so they have been remmed out for refernece
    #map.redirect('/{controller}/'         , '/{controller}'         ) 
    #map.redirect('/{controller}/{action}/', '/{controller}/{action}')

    # the first route that matches url() args is the one that's generated,
    # so put routes without slashes first
    map.connect('/{controller}/{action}.{format}/{id}')  # CAFI
    #map.connect('/{controller}/{action}.{format}/{id}/') # CAFI/
    map.connect('/{controller}/{action}/{id}')           # CAI
    #map.connect('/{controller}/{action}/{id}/')          # CAI/
    map.connect('/{controller}/{action}.{format}')       # CAF
    #map.connect('/{controller}/{action}.{format}/')      # CAF/
    map.connect('/{controller}/{action}')                # CA
    #map.connect('/{controller}/{action}/')               # CA/
    map.connect('/{controller}' , action="index")        # C
    #map.connect('/{controller}/', action="index")        # C/

    return map
