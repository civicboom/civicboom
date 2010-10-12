"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def cb_resource(mapper, single, plural, **kwargs):
    if kwargs:
        return mapper.resource(single, plural, **kwargs)

    # list actions
    mapper.connect('formatted_'+plural, '/'+plural+'.{format}',                controller=plural, action='index',  conditions=dict(method=['GET']))
    mapper.connect(plural, '/'+plural,                                         controller=plural, action='index',  conditions=dict(method=['GET']))

    mapper.connect('formatted_'+plural, '/'+plural+'.{format}',                controller=plural, action='create', conditions=dict(method=['POST']))
    mapper.connect('/'+plural,                                                 controller=plural, action='create', conditions=dict(method=['POST']))

    # item actions
    # /foo/new needs to be before /foo/{id}
    mapper.connect('formatted_new_'+single, '/'+plural+'/new.{format}',        controller=plural, action='new',    conditions=dict(method=['GET']))
    mapper.connect('new_'+single, '/'+plural+'/new',                           controller=plural, action='new',    conditions=dict(method=['GET']))

    mapper.connect('formatted_'+single, '/'+plural+'/{id}.{format}',           controller=plural, action='show',   conditions=dict(method=['GET']))
    mapper.connect(single, '/'+plural+'/{id}',                                 controller=plural, action='show',   conditions=dict(method=['GET']))

    mapper.connect('/'+plural+'/{id}.{format}',                                controller=plural, action='update', conditions=dict(method=['PUT']))
    mapper.connect('/'+plural+'/{id}',                                         controller=plural, action='update', conditions=dict(method=['PUT']))

    mapper.connect('/'+plural+'/{id}.{format}',                                controller=plural, action='delete', conditions=dict(method=['DELETE']))
    mapper.connect('/'+plural+'/{id}',                                         controller=plural, action='delete', conditions=dict(method=['DELETE']))

    # item extra actions
    # /foo/{id}/edit is the only GET action
    mapper.connect('formatted_edit_'+single, '/'+plural+'/{id}.{format}/edit', controller=plural, action='edit',   conditions=dict(method=['GET']))
    mapper.connect('edit_'+single, '/'+plural+'/{id}/edit',                    controller=plural, action='edit',   conditions=dict(method=['GET']))

    # civicboom extra: foo_actions controller for separate /foo/42/activate methods
    mapper.connect('formatted_'+single+'_action', '/'+plural+'/{id}/{action}.{format}',  controller=single+'_actions', conditions=dict(method=['POST']))
    mapper.connect(single+'_action', '/'+plural+'/{id}/{action}',              controller=single+'_actions', format="redirect", conditions=dict(method=['POST']))


def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # CUSTOM ROUTES HERE
    map.connect('/', controller='misc', action='titlepage')
    cb_resource(map, 'message', 'messages')
    cb_resource(map, 'setting', 'settings')
    cb_resource(map, 'content', 'contents')
    cb_resource(map, 'feed',    'feeds'   )


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
    map.connect('/{controller}/{action}/{id}')           # CAI
    map.connect('/{controller}/{action}.{format}')       # CAF
    map.connect('/{controller}/{action}')                # CA
    map.connect('/{controller}' , action="index")        # C

    # actually, routes with slashes aren't used at all...
    #map.connect('/{controller}/{action}.{format}/{id}/') # CAFI/
    #map.connect('/{controller}/{action}/{id}/')          # CAI/
    #map.connect('/{controller}/{action}.{format}/')      # CAF/
    #map.connect('/{controller}/{action}/')               # CA/
    #map.connect('/{controller}/', action="index")        # C/

    return map
