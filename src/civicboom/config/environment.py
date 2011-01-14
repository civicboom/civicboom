"""Pylons environment configuration"""
import os

from pylons.configuration import PylonsConfig
from mako.lookup import TemplateLookup
#from pylons import config
from pylons.error import handle_mako_error
from sqlalchemy import engine_from_config

from paste.deploy.converters import asbool

import civicboom.lib.app_globals as app_globals
import civicboom.lib.helpers
from civicboom.config.routing import make_map
from civicboom.model import init_model
from civicboom.lib.worker import start_worker
from civicboom.lib.civicboom_init import init as civicboom_init # This will tirgger a set of additional initalizers

def load_environment(global_conf, app_conf):
    """
    Configure the Pylons environment via the ``pylons.config``
    object
    """
    config = PylonsConfig()

    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
            controllers=os.path.join(root, 'controllers'),
            static_files=os.path.join(root, 'public'),
            templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='civicboom', paths=paths)

    config['routes.map']         = make_map(config)
    config['pylons.app_globals'] = app_globals.Globals(config)

    import pylons
    pylons.cache._push_object(config['pylons.app_globals'].cache)

    config['pylons.h'] = civicboom.lib.helpers

    # Create the Mako TemplateLookup, with the default auto-escaping
    config['pylons.app_globals'].mako_lookup = TemplateLookup(
            directories=paths['templates'],
            error_handler=handle_mako_error,
            module_directory=os.path.join(app_conf['cache_dir'], 'templates'),
            input_encoding='utf-8', default_filters=['escape'],
            imports=['from webhelpers.html import escape'])

    # Setup the SQLAlchemy database engine
    engine = engine_from_config(config, 'sqlalchemy.main.')
    init_model(engine)

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)
    config['development_mode'] = asbool(config['debug'])

    # Booleans in config file
    boolean_varnames = ['feature.notifications',
                        'feature.aggregate.email',
                        'feature.aggregate.janrain',
                        'feature.aggregate.twitter_global',
                        'feature.profanity_filter',
                        'security.disallow_https_cookie_in_http',
                        'online',
                        'test_mode',
                        ]
    for varname in boolean_varnames:
        config[varname] = asbool(config[varname])

    # Integers in config file
    integer_varnames = ['payment.free.assignment_limit',
                        'payment.plus.assignment_limit',
                        ]
    for varname in integer_varnames:
        config[varname] = int(config[varname].strip())
    

    # worker and websetup.py both try to access pylons.config before it is
    # officially ready -- so make it unofficially ready and pray (HACK)
    from pylons import config as pylons_config
    for k, v in list(config.items()):
        pylons_config[k] = v

    civicboom_init() # This will tirgger a set of additional initalizers
    start_worker()

    return config
