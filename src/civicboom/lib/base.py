"""
The base Controller API

Provides the BaseController class for subclassing.

Lots of stuff is imported here (eg controller action decorators) so that other
controllers can do "from civicboom.lib.base import *"
"""
from pylons.controllers       import WSGIController
from pylons                   import request, response, app_globals, tmpl_context as c, url, config, session
from pylons.controllers.util  import abort, redirect
from pylons.templating        import render_mako
from pylons.i18n.translation  import _, ungettext, set_lang
from pylons.decorators.secure import https
from webhelpers.pylonslib.secure_form import authentication_token

from civicboom.model.meta              import Session
from civicboom.model                   import meta
from civicboom.lib.web                 import redirect_to_referer, set_flash_message, overlay_status_message, action_ok, action_error, auto_format_output, session_get, session_remove, session_set, authenticate_form, cacheable
from civicboom.lib.database.get_cached import get_user
from civicboom.lib.civicboom_lib       import deny_pending_user
from civicboom.lib.authentication      import authorize, is_valid_user

import json

import logging
log = logging.getLogger(__name__)

__all__ = [
    # pylons environment
    "request", "response", "app_globals", "c", "url", "config",

    # sqlalchemy environment
    "Session", "meta",

    # return types
    "abort", "redirect", "action_ok", "action_error", "render",

    # decorators
    "https", "authenticate_form",
    "auto_format_output",
    "authorize", "is_valid_user",
    "cacheable",

    # i18n
    "_", "ungettext", "set_lang",

    # session managemnet - is is prefered that all access to the session is via accessors
    "session_get", "session_remove", "session_set",

    "set_flash_message",

    # misc
    "BaseController",
    "authentication_token",
    "redirect_to_referer", #TODO? potential for removal?
    "get_user",
    "logging",
]

#-------------------------------------------------------------------------------
# Render
#-------------------------------------------------------------------------------
def render(*args, **kargs):
    if app_globals.cache_enabled: return render_mako(*args, **kargs)
    else                        : return render_mako(*args, **kargs)

#-------------------------------------------------------------------------------
# Base Controller
#-------------------------------------------------------------------------------
class BaseController(WSGIController):
    
    def _set_lang(self, lang):
        c.lang = lang
        set_lang(lang)
    
    def __before__(self):

        # Setup globals c
        # Request global - have the system able to easly view request details as globals
        current_request = request.environ.get("pylons.routes_dict")
        c.controller = current_request.get("controller")
        c.action     = current_request.get("action")
        c.id         = current_request.get("id")
        c.format     = current_request.get("format", request.params.get('format', config['default_format'] ) )
        
        c.result = {'status':'ok', 'message':'', 'data':{}}
        
        c.authenticated_form = None # if we want to call a controler action internaly from another action we get errors because the auth_token is delted, this can be set by the authenticated_form decorator so we allow subcall requests


        # Login - Fetch logged in user from session id (if present)
        c.logged_in_user = get_user(session_get('user_id'))

        # Setup Langauge
        #  - there is a way of setting fallback langauges, investigate?
        if   'lang' in request.params:  self._set_lang(request.params['lang']) # If lang set in URL
        elif 'lang' in session       :  self._set_lang(       session['lang']) # Lang set for this users session
        #elif c.logged_in_user has lang: self._set_lang(c.logged_in_user.?)     # Lang in user preferences
        else                         :  self._set_lang(        config['lang']) # Default lang in config file

        # User pending regisration? - redirect to complete registration process
        if c.logged_in_user and c.logged_in_user.status=='pending' and deny_pending_user(url.current()):
            set_flash_message(_('Please complete the regisration process'))
            redirect(url(controller='register', action='new_user', id=c.logged_in_user.id))

        # Setup site app_globals on first request
        # AllanC - I dont like this, is there a call we can maybe put in the tasks controler? or an init controler? that we can fire when the site is restarted?
        #          For development this is sufficent, but should not be used in a production env.
        #
        # TODO - yeah, we really need a STARTUP method that gets called to init these
        if not hasattr(app_globals,'site_url'):
            app_globals.site_host = request.environ['SERVER_NAME']
            if config['debug']:
                app_globals.site_host = request.environ['HTTP_HOST']
            app_globals.site_url           = "http://" + app_globals.site_host
            #import urllib
            #app_globals.janrain_signin_url = urllib.quote_plus(url(controller='account', action='signin', host=app_globals.site_host, protocol='https'))


        #AllanC - For gadgets and emails links and static content need to be absolute
        #         A gadget controler could set this True, any image or URL created with helpers.py would have host appended to them
        c.absolute_links = False
        
        # Session Flash Message
        flash_message_session = session_remove('flash_message')
        if flash_message_session:
            try:               overlay_status_message(c.result, json.loads(flash_message_session))
            except ValueError: overlay_status_message(c.result,            flash_message_session )


    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()
