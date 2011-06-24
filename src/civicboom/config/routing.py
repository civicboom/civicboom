"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper
import re


def cb_resource(mapper, single, plural, **kwargs):
    # nothing uses this yet, so it is untested
    #if kwargs:
    #    return mapper.resource(single, plural, **kwargs)

    # lists
    # GET/POST /foo.json
    mapper.connect(plural, '/'+plural+'{.format}',                             controller=plural, action='index',  conditions=dict(method=['GET']))
    mapper.connect(None,   '/'+plural+'{.format}',                             controller=plural, action='create', conditions=dict(method=['POST']))

    # list actions (needs to come before items, as /foo/new needs to be before /foo/{id})
    # GET /foo/new.json
    mapper.connect('new_'+single, '/'+plural+'/new{.format}',                  controller=plural, action='new',    conditions=dict(method=['GET']))

    # items
    # GET/PUT/DELETE for /foo/42.json, /foo/42
    mapper.connect(single, '/'+plural+'/{id}{.format}',                        controller=plural, action='show',   conditions=dict(method=['GET']))
    mapper.connect(None,   '/'+plural+'/{id}{.format}',                        controller=plural, action='update', conditions=dict(method=['PUT']))
    mapper.connect(None,   '/'+plural+'/{id}{.format}',                        controller=plural, action='delete', conditions=dict(method=['DELETE']))

    # item actions (edit is special, it lives in the main controller rather than _actions)
    mapper.connect('edit_'+single,   '/'+plural+'/{id}/edit{.format}',         controller=plural, action='edit',   conditions=dict(method=['GET']))
    mapper.connect(single+'_action', '/'+plural+'/{id}/{action}{.format}',     controller=single+'_actions',       conditions=dict(method=['GET', 'POST', 'PUT', 'DELETE']))


def _subdomain_check(kargs, mapper, environ):
    """Screen the kargs for a subdomain and alter it appropriately depending
    on the current subdomain or lack therof.
    
    Monkeypatch by Shish - if we have a subdomain currently, and it isn't
    in the ignore list, and we aren't explicitly removing it, don't remove it
    """
    if mapper.sub_domains:
        subdomain_specified = 'sub_domain' in kargs
        subdomain = kargs.pop('sub_domain', None)
        if isinstance(subdomain, unicode):
            subdomain = str(subdomain)
        
        fullhost = environ.get('HTTP_HOST') or environ.get('SERVER_NAME')
        
        # In case environ defaulted to {}
        if not fullhost:
            return kargs
        
        hostmatch = fullhost.split(':')
        host = hostmatch[0]
        port = ''
        if len(hostmatch) > 1:
            port += ':' + hostmatch[1]
        sub_match = re.compile('^.+?\.(%s)$' % mapper.domain_match)
        domain = re.sub(sub_match, r'\1', host)
        if subdomain and not host.startswith(subdomain) and \
            subdomain not in mapper.sub_domains_ignore:
            kargs['_host'] = subdomain + '.' + domain + port
        elif (subdomain in mapper.sub_domains_ignore or \
            (subdomain_specified and subdomain is None)) and domain != host:
            kargs['_host'] = domain + port
        return kargs
    else:
        return kargs


def make_map(config):
    """Create, configure and return the routes Mapper"""

    import routes.util
    routes.util._subdomain_check = _subdomain_check

    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.sub_domains = True
    #map.sub_domains_ignore = ["www", ]


    # CUSTOM ROUTES HERE
    map.connect(None, '/', controller='misc', action='titlepage')
    map.connect(None, '/robots.txt', controller='misc', action='robots')
    map.connect(None, '/about/{id}' , controller='misc', action="about")
    map.connect(None, '/profile',     controller='profile', action="index")
    map.connect(None, '/help/{id}'  , controller='misc', action="help", format="frag")
    map.connect(None, '/settings/{id}/{panel}{.format}', controller='settings', action='panel', format="html")
    map.connect(None, '/contents/{id}{.format}/-/{title}', controller='contents', action='show', conditions=dict(method=['GET']))
    map.redirect('/api.html', '/doc/')

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

    map.connect('/{controller}/{action}/{id}{.format}')
    map.connect('/{controller}/{action}{.format}')
    map.connect('/{controller}{.format}', action="index")

    return map
