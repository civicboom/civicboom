"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers      import WSGIController
from pylons                  import request, app_globals, tmpl_context as c, url, config, session
from pylons.controllers.util import abort, redirect
from pylons.templating       import render_mako as render
from pylons.i18n.translation import _, ungettext

from civicboom.model                   import meta
from civicboom.lib.database.get_cached import get_user
from civicboom.lib.misc                import flash_message, redirect_to_referer



import logging
log = logging.getLogger(__name__)


class BaseController(WSGIController):
    def __before__(self):

        c.logged_in_user = get_user(session.get('user_id'))

        # AuthKit Login Fallback - if AuthKit is enabled this will set the logged_in_user
        #   AuthKit would have already authenticated any cookies & sessions by this point
        #   so lookup the reporter of the remote user
        #   (someone who is slightly more security savy may want to double check the implications of this)
        if not c.logged_in_user and 'authkit.setup.method' in config and 'REMOTE_USER' in request.environ:
            c.logged_in_user = get_user(request.environ['REMOTE_USER'])


        # Setup Langauge
        #if c.logged_in_user has langauge prefernece:
        #  pass
        if 'lang' in session:
            pass #unfinished
            #set_lang(session['lang']) 


        # Setup site app_globals on first request
        # AllanC - I dont like this, is there a call we can maybe put in the tasks controler? or an init controler? that we can fire when the site is restarted?
        #          For development this is sufficent, but should not be used in a production env.
        if not hasattr(app_globals,'site_url'):
            app_globals.site_host = request.environ['SERVER_NAME']
            if config['debug']:
                app_globals.site_host = request.environ['HTTP_HOST']
            app_globals.site_url = "http://" + app_globals.site_host
        #c.current_path = request.environ.get('PATH_INFO')


        #AllanC - For gadgets and emails links and static content need to be absolute
        #         A gadget controler could set this True, any image or URL created with helpers.py would have c.server_name appended to them
        c.absolute_links = False

        current_request = request.environ.get("pylons.routes_dict")
        #for key in current_request:
        #  print "%s:%s" % (key,current_request[key])
        c.action    = current_request.get("action")
        c.action_id = current_request.get("id")



    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()
