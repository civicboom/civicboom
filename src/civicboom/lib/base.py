"""
The base Controller API

Provides the BaseController class for subclassing.

Lots of stuff is imported here (eg controller action decorators) so that other
controllers can do "from civicboom.lib.base import *"
"""
from pylons.controllers       import WSGIController
from pylons                   import request, response, app_globals, tmpl_context as c, url, config, session
from pylons.controllers.util  import abort
from pylons.templating        import render_mako
from pylons.i18n.translation  import _, ungettext, set_lang
from pylons.decorators.secure import https
from webhelpers.pylonslib.secure_form import authentication_token

from civicboom.model.meta              import Session
from civicboom.model                   import meta
from civicboom.lib.web                 import redirect, redirect_to_referer, set_flash_message, overlay_status_message, action_ok, action_ok_list, action_error, auto_format_output, session_get, session_remove, session_set, authenticate_form, cacheable, web_params_to_kwargs
from civicboom.lib.database.get_cached import get_member, get_group, get_membership
from civicboom.lib.database.etag_manager import gen_cache_key
from civicboom.lib.civicboom_lib       import deny_pending_user
from civicboom.lib.authentication      import authorize
from civicboom.lib.permissions         import account_type
#from civicboom.model.member            import account_types
import civicboom.lib.errors as errors

import json

import logging
log = logging.getLogger(__name__)

__all__ = [
    # pylons environment
    "request", "response", "app_globals", "c", "url", "config",

    # sqlalchemy environment
    "Session", "meta",

    # return types
    "abort", "redirect", "action_ok", "action_ok_list", "action_error", "render",

    # decorators
    "https",
    "authorize", 
    "authenticate_form",
    "auto_format_output",
    "web_params_to_kwargs",
    "cacheable",
    "web",
    "auth",
    "account_type",
    #"account_types", #types for use with with account_type decorator
    
    #errors
    "errors",
    
    # i18n
    "_", "ungettext", "set_lang",

    # session managemnet - is is prefered that all access to the session is via accessors
    "session_get", "session_remove", "session_set",

    "set_flash_message",

    # misc
    "BaseController",
    "authentication_token",
    "redirect_to_referer", #TODO? potential for removal?
    "get_member", "get_group", #AllanC - should be used with cuation, we need to be careful about permissions
    "logging",
    "overlay_status_message",
    
    #cache
    "gen_cache_key"
]

#-------------------------------------------------------------------------------
# Render
#-------------------------------------------------------------------------------
def render(*args, **kwargs):
    if app_globals.cache_enabled:
        return render_mako(*args, **kwargs)
    else:
        if 'cache_key'    in kwargs: del kwargs['cache_key']
        if 'cache_expire' in kwargs: del kwargs['cache_expire']
        return render_mako(*args, **kwargs)

#-------------------------------------------------------------------------------
# Decorators - Merged
#-------------------------------------------------------------------------------

# Reference - http://stackoverflow.com/questions/2182858/how-can-i-pack-serveral-decorators-into-one

def chained(*dec_funs):
    def _inner_chain(f):
        for dec in reversed(dec_funs):
            f = dec(f)
        return f
    return _inner_chain

web  = chained(auto_format_output, web_params_to_kwargs)
auth = chained(authorize, authenticate_form)


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
        
        c.result = {'status':'ok', 'message':'', 'data':{}}

        c.format               = None #AllanC - c.format now handled by @auto_format_output in lib so the formatting is only applyed once
        c.authenticated_form   = None # if we want to call a controler action internaly from another action we get errors because the auth_token is delted, this can be set by the authenticated_form decorator so we allow subcall requests
        c.web_params_to_kwargs = None

        #c.widget = dict(
        #    theme    = 'light' ,
        #    width    = 240 ,
        #    height   = 320 ,
        #    title    = '' ,
        #    username = '' ,
        #)

        # Login - Fetch logged in user from session id (if present)
        username                 = session_get('username')
        username_persona         = session_get('username_persona')
        
        c.logged_in_user         = get_member(username)
        c.logged_in_persona      = c.logged_in_user
        c.logged_in_persona_role = None #session_get('role')
        if username != username_persona:
            persona    = get_group(username_persona)
            membership = get_membership(persona ,c.logged_in_user)
            if membership:
                c.logged_in_persona      = persona
                c.logged_in_persona_role = membership.role

        # Setup Langauge
        #  - there is a way of setting fallback langauges, investigate?
        if   'lang' in request.params:  self._set_lang(request.params['lang']) # If lang set in URL
        elif 'lang' in session       :  self._set_lang(       session['lang']) # Lang set for this users session
        #elif c.logged_in_persona has lang: self._set_lang(c.logged_in_persona.?)     # Lang in user preferences
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
            app_globals.site_host = request.environ.get('HTTP_HOST', request.environ.get('SERVER_NAME'))
            ##app_globals.site_url  = "http://" + app_globals.site_host
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

    def print_controller_status(self):
        from civicboom.lib.web import current_referer, current_url
        print "current_referer: %s" % current_referer()
        print "current_url    : %s" % current_url()
        print c

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            # apparently remove() doesn't always do a good job and we eventually
            # run out of connections; close() works though
            # http://www.mail-archive.com/sqlalchemy@googlegroups.com/msg05489.html
            #meta.Session.remove()
            meta.Session.close()
