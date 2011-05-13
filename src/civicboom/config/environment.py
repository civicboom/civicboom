"""Pylons environment configuration"""
import os

import pylons
from pylons.configuration import PylonsConfig
from mako.lookup import TemplateLookup
from pylons.error import handle_mako_error
from sqlalchemy import engine_from_config

from paste.deploy.converters import asbool

import civicboom.lib.app_globals as app_globals
import civicboom.lib.helpers
from civicboom.config.routing import make_map
from civicboom.model import init_model
from civicboom.lib.civicboom_init import init as civicboom_init  # This will trigger a set of additional initalizers
import civicboom.lib.services.warehouse as wh

# for setting up the redis backend to beaker
import beaker
import civicboom.lib.redis_ as redis_

# for connecting to the worker queue
import platform
from redis import Redis
import civicboom.lib.worker as worker


def load_environment(global_conf, app_conf):
    """
    Configure the Pylons environment via the ``pylons.config``
    object
    """
    config = PylonsConfig()

    beaker.cache.clsmap['ext:redis'] = redis_.RedisManager

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
                        'demo_mode',
                        ]
    for varname in boolean_varnames:
        config[varname] = asbool(config.get(varname))

    # Integers in config file
    integer_varnames = ['payment.free.assignment_limit'  ,
                        'payment.plus.assignment_limit'  ,
                        'search.default.limit.sub_list'  ,
                        'search.default.limit.contents'  ,
                        'search.default.limit.members'   ,
                        'search.default.limit.messages'  ,
                        'setting.session.login_expire_time',
                        'email.smtp_port',
                        'setting.content.max_comment_length',
                        ]
    for varname in integer_varnames:
        config[varname] = int(config[varname].strip())

    # worker and websetup.py both try to access pylons.config before it is
    # officially ready -- so make it unofficially ready and pray (HACK)
    for k, v in list(config.items()):
        pylons.config[k] = v

    # configure the warehouse
    wh.configure(pylons.config)

    # set up worker processors
    from civicboom.lib.worker_threads.send_notification  import send_notification
    from civicboom.lib.worker_threads.process_media      import process_media
    from civicboom.lib.worker_threads.profanity_check    import profanity_check
    worker.add_worker_function('process_media'     , process_media    )
    worker.add_worker_function('send_notification' , send_notification)
    worker.add_worker_function('profanity_check'   , profanity_check  )

    # set up worker queue
    if pylons.config['worker.queue'] == "inline":
        worker.init_queue(None)
    elif pylons.config['worker.queue'] == "threads":
        worker.start_worker()
    elif pylons.config['worker.queue'] == "redis":
        worker.init_queue(redis_.RedisQueue(Redis(config['service.redis.server']), platform.node()))
    else:
        log.error("Invalid worker type: %s" % pylons.config['worker.queue'])

    civicboom_init() # This will tirgger a set of additional initalizers

    return config
