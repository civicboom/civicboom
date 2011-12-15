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
from civicboom.model import init_model, init_model_extra
import cbutils.warehouse as wh

# for setting up the redis backend to beaker
import beaker
import cbutils.redis_ as redis_

# for connecting to the worker queue
import platform
from redis import Redis
import cbutils.worker as worker

#import logging
#log = logging.getLogger("sitemaster")

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

    #pylons.cache._push_object(config['pylons.app_globals'].cache)

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

    # Global translator setup
    #log.info("Init global i18n as en")
    #import gettext
    #langs = {
    #    "en": gettext.translation("civicboom", "./civicboom/i18n", languages=['en']),
    #}
    #langs["en"].install()

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
                        'profile',
                        'beaker.cache.enabled',
                        'cache.etags.enabled',
                        'cache.static_decorators.enabled',
                        'test.crawl_links',
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
                        'setting.age.min_signup',
                        'setting.age.accept',
                        'timedtask.batch_chunk_size',
                        #'media.media.width', # AllanC - the media processing imports the config in a differnt way. I dont know if this cast to int is needed
                        #'media.media.height',
                        ]
    for varname in integer_varnames:
        config[varname] = int(config[varname].strip())

    # websetup.py tries to access pylons.config before it is
    # officially ready -- so make it unofficially ready and pray (HACK)
    for k, v in list(config.items()):
        pylons.config[k] = v

    # configure modules that used to require pylons.config
    wh.configure(pylons.config)

    import civicboom.lib.communication.email_lib as email
    email.configure(pylons.config)

    # set up worker processors
    if pylons.config['worker.queue.type'] in ["inline", "threads"]:
        # AllanC changed it from worker.config=pylons.config because = replaces the reference. If worker.config is imported BEFORE this code is run then the importing class only access the empty original dict
        worker.config.update(pylons.config)
        # WARNING!!!
        # AllanC - NOTE!!! this update is fine AS LONG AS THE CONFIG IS NEVER CHANGED WHILE THE SITE IS RUNNING!
        #          in production this is never changed ... howver .. in testing we alter the state of the config to test ... even if most tests pass we could have some horrible hard to track down bugs because of this .update fix
        
        from civicboom.worker import init_worker_functions
        init_worker_functions(worker)

    # set up worker queue
    if pylons.config['worker.queue.type'] == "inline":
        worker.init_queue(None)
    elif pylons.config['worker.queue.type'] == "threads":  # pragma: no cover
        worker.start_worker()
    elif pylons.config['worker.queue.type'] == "redis":  # pragma: no cover
        worker.init_queue(redis_.RedisQueue(redis_.redis_from_url(config['worker.queue.url']), platform.node()))
    else:  # pragma: no cover
        log.error("Invalid worker type: %s" % pylons.config['worker.queue.type'])

    # set up cache
    from civicboom.lib.cache import init_cache
    init_cache(config)

    # set up cbtv
    import cbutils.cbtv as t
    if config.get('telemetry'):  # pragma: no cover -- telemetry is disabled during coverage test
        t.set_log(config['telemetry'])

    init_model_extra() # This will trigger a set of additional initalizers

    return config
