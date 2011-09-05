"""Pylons middleware initialization"""
from beaker.middleware import SessionMiddleware
from paste.cascade import Cascade
from paste.registry import RegistryManager
from paste.urlparser import StaticURLParser
from paste.fileapp import FileApp
from paste.deploy.converters import asbool
#from paste.deploy.config import PrefixMiddleware
#from pylons.middleware import StatusCodeRedirect
from pylons.middleware import ErrorHandler
from pylons.wsgiapp import PylonsApp
from routes.middleware import RoutesMiddleware


from civicboom.config.environment import load_environment

from civicboom.middleware.MobileDetectionMiddleware import MobileDetectionMiddleware
from civicboom.middleware.EnvironMiddleware import EnvironMiddleware
from civicboom.middleware.SecurifyCookiesMiddleware import SecurifyCookiesMiddleware


class HeaderURLParser(StaticURLParser):
    def make_app(self, filename):
        # set headers so that static content can be cached
        headers = [
            ("Cache-Control", "public,max-age=%d" % int(60 * 60 * 24 * 365)),
            ("Vary", "Accept-Encoding"),
        ]
        return FileApp(filename, headers)#, content_type='application/octetstream')


def make_app(global_conf, full_stack=True, static_files=True, **app_conf):
    """Create a Pylons WSGI application and return it

    ``global_conf``
        The inherited configuration for this application. Normally from
        the [DEFAULT] section of the Paste ini file.

    ``full_stack``
        Whether this application provides a full WSGI stack (by default,
        meaning it handles its own exceptions and errors). Disable
        full_stack when this application is "managed" by another WSGI
        middleware.

    ``static_files``
        Whether this application serves its own static files; disable
        when another web server is responsible for serving them.

    ``app_conf``
        The application's local configuration. Normally specified in
        the [app:<name>] section of the Paste ini file (where <name>
        defaults to main).

    """
    # Configure the Pylons environment
    config = load_environment(global_conf, app_conf)

    # The Pylons WSGI app
    app = PylonsApp(config=config)

    if config['profile']:  # pragma: no cover - nightly profiles do the full stack
        from repoze.profiler import AccumulatingProfileMiddleware
        app = AccumulatingProfileMiddleware(
            app,
            log_filename='/tmp/cb-website.prof',
            discard_first_request=True,
            flush_at_shutdown=True,
            path='/__profile__'
        )


    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    #app = CacheMiddleware(app, config) # Cache now setup in app_globals as suggested in http://pylonshq.com/docs/en/1.0/upgrading/

    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)
    app = MobileDetectionMiddleware(app)
    app = EnvironMiddleware(app)
    app = SecurifyCookiesMiddleware(app)

    if asbool(full_stack):
        # Handle Python exceptions
        app = ErrorHandler(app, global_conf, **config['pylons.errorware'])

    # Establish the Registry for this application
    app = RegistryManager(app)

    if asbool(static_files):
        # Serve static files
        static_app = HeaderURLParser(config['pylons.paths']['static_files'])
        app = Cascade([static_app, app])

    app.config = config

    return app
