"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper


def cb_resource(mapper, single, plural, **kwargs):
    # nothing uses this yet, so it is untested
    #if kwargs:
    #    return mapper.resource(single, plural, **kwargs)

    # lists
    # GET /foo.json
    mapper.connect('formatted_'+plural, '/'+plural+'.{format}',                controller=plural, action='index',  conditions=dict(method=['GET']))
    mapper.connect(plural, '/'+plural,                                         controller=plural, action='index',  conditions=dict(method=['GET']))

    # POST /foo.json
    mapper.connect('formatted_'+plural, '/'+plural+'.{format}',                controller=plural, action='create', conditions=dict(method=['POST']))
    mapper.connect('/'+plural,                                                 controller=plural, action='create', conditions=dict(method=['POST']))

    # list actions (needs to come before items, as /foo/new needs to be before /foo/{id})
    # /foo/new.json
    mapper.connect('formatted_new_'+single, '/'+plural+'/new.{format}',        controller=plural, action='new',    conditions=dict(method=['GET']))
    mapper.connect('new_'+single, '/'+plural+'/new',                           controller=plural, action='new',    conditions=dict(method=['GET']))

    # items
    # GET/PUT/DELETE for /foo/42.json, /foo/42
    mapper.connect('formatted_'+single, '/'+plural+'/{id}.{format}',           controller=plural, action='show',   conditions=dict(method=['GET']))
    mapper.connect(single, '/'+plural+'/{id}',                                 controller=plural, action='show',   conditions=dict(method=['GET']))

    mapper.connect('/'+plural+'/{id}.{format}',                                controller=plural, action='update', conditions=dict(method=['PUT']))
    mapper.connect('/'+plural+'/{id}',                                         controller=plural, action='update', conditions=dict(method=['PUT']))

    mapper.connect('/'+plural+'/{id}.{format}',                                controller=plural, action='delete', conditions=dict(method=['DELETE']))
    mapper.connect('/'+plural+'/{id}',                                         controller=plural, action='delete', conditions=dict(method=['DELETE']))

    # item actions
    # /foo/{id}/edit
    # - part of the main controller by tradition, but do we want it there?
    # - if we put edit into foo_actions, then lots of controllers that currently only have edit as their
    #   one action would need to be split into two files
    mapper.connect('formatted_edit_'+single, '/'+plural+'/{id}/edit.{format}', controller=plural, action='edit',   conditions=dict(method=['GET']))
    mapper.connect('edit_'+single, '/'+plural+'/{id}/edit',                    controller=plural, action='edit',   conditions=dict(method=['GET']))

    # /foo/42/activate
    mapper.connect(single+'_action', '/'+plural+'/{id}/{action}.{format}',     controller=single+'_actions', format='redirect', conditions=dict(method=['POST', 'PUT', 'DELETE']))
    mapper.connect(single+'_action', '/'+plural+'/{id}/{action}.{format}',     controller=single+'_actions', format='html'    , conditions=dict(method=['GET']))
    mapper.connect('/'+plural+'/{id}/{action}',                                controller=single+'_actions', format='html')


def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # CUSTOM ROUTES HERE
    map.connect('/', controller='misc', action='titlepage')
    map.connect('/about/{id}' , controller='misc', action="about")
    map.connect('/help/{id}'  , controller='misc', action="help", format="frag")
    map.connect('/settings/{id}/{panel}.{format}', controller='settings', action='panel')
    map.connect('/settings/{id}/{panel}', controller='settings', action='panel')
    
    cb_resource(map, 'content', 'contents')
    cb_resource(map, 'message', 'messages')
    cb_resource(map, 'member',  'members' )
    cb_resource(map, 'setting', 'settings')
    cb_resource(map, 'feed',    'feeds'   )
    cb_resource(map, 'group',   'groups'  )
    cb_resource(map, 'medium',  'media'   )

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
    map.connect('/{controller}/{action}/{id}.{format}')  # CAFI
    map.connect('/{controller}/{action}/{id}')           # CAI
    map.connect('/{controller}/{action}.{format}')       # CAF
    map.connect('/{controller}/{action}')                # CA
    map.connect('/{controller}' , action="index")        # C

    return map
