"""Pylons middleware initialization"""
from beaker.middleware import SessionMiddleware
from paste.cascade import Cascade
from paste.registry import RegistryManager
from paste.urlparser import StaticURLParser
from paste.deploy.converters import asbool
#from pylons import config
from pylons.middleware import ErrorHandler, StatusCodeRedirect
from pylons.wsgiapp import PylonsApp
from routes.middleware import RoutesMiddleware
import authkit.authenticate

from civicboom.config.environment import load_environment

from civicboom.middleware.MobileDetectionMiddleware import MobileDetectionMiddleware
from civicboom.middleware.GZipMiddleware            import GZipMiddleware


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

    # Routing/Session/Cache Middleware
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = authkit.authenticate.middleware(app, app_conf) #Here so AuthKit can use authkit.cookie.nouserincookie = true  at   http://pylonsbook.com/en/1.1/authentication-and-authorization.html#cookie-options
    #app = CacheMiddleware(app, config) # Cache now setup in app_globals as suggested in http://pylonshq.com/docs/en/1.0/upgrading/
    
    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)
    app = MobileDetectionMiddleware(app)
    #app = GZipMiddleware(app) #AllanC - not implemented yet, need a way for a controler to trigger Gziping, maybe via a decorator? is this the right place in the middleware stack? top executed last?
    

    if asbool(full_stack):
        # Handle Python exceptions
        app = ErrorHandler(app, global_conf, **config['pylons.errorware'])

        #app = authkit.authenticate.middleware(app, app_conf) # Pylons book suggested authkit should go here at first

        # Display error documents for 401, 403, 404 status codes (and
        # 500 when debug is disabled)
        if asbool(config['debug']):
            app = StatusCodeRedirect(app)
        else:
            app = StatusCodeRedirect(app, [400, 401, 403, 404, 500])

    # Establish the Registry for this application
    app = RegistryManager(app)

    if asbool(static_files):
        # Serve static files
        static_app = StaticURLParser(config['pylons.paths']['static_files'])
        app = Cascade([static_app, app])

    app.config = config

    return app
