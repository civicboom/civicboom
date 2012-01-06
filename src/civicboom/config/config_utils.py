from paste.deploy.converters import asbool

def config_type_replacement(config):
    """
    Configs are always a dict of strings
    We need to convert key names of known types into those types
    """
    
    config['development_mode'] = asbool(config['debug'])

    # Booleans in config file
    boolean_varnames = ['feature.notifications',
                        'feature.aggregate.email',
                        'feature.aggregate.janrain',
                        'feature.aggregate.twitter_global',
                        'feature.profanity_filter',
                        #'security.disallow_https_cookie_in_http', # Depricated?
                        'online',
                        'test_mode',
                        'demo_mode',
                        'profile',
                        'beaker.cache.enabled',
                        'cache.etags.enabled',
                        'cache.static_decorators.enabled',
                        'test.crawl_links',
                        ]
    for varname in [varname for varname in boolean_varnames if varname in config]:
        config[varname] = asbool(config[varname])

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
    for varname in [varname for varname in integer_varnames if varname in config]:
        config[varname] = int(config[varname].strip())

