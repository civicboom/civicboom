"""
The base Controller API

Provides the BaseController class for subclassing.

Lots of stuff is imported here (eg controller action decorators) so that other
controllers can do "from civicboom.lib.base import *"
"""
from pylons.controllers       import WSGIController
from pylons                   import request, response, app_globals, tmpl_context as c, config
from pylons                   import session # needed for invalidating the session
from pylons.controllers.util  import abort
from pylons.templating        import render_mako, render_mako_def
from pylons.i18n.translation  import _, ungettext, set_lang
from pylons.decorators.secure import https
from webhelpers.pylonslib.secure_form import authentication_token

from civicboom.model.meta              import Session
from civicboom.model                   import meta, Member
from civicboom.lib.web                 import * #url, redirect, redirect_to_referer, set_flash_message, overlay_status_message, action_ok, action_error, auto_format_output, session_get, session_remove, session_set, session_keys, session_delete, authenticate_form, cacheable, web_params_to_kwargs, current_url, current_referer
from civicboom.lib.database.get_cached import get_member as _get_member, get_group as _get_group, get_membership as _get_membership, get_membership_tree as _get_membership_tree, get_message as _get_message, get_content as _get_content, get_members, get_member_email as _get_member_email
from civicboom.lib.database.query_helpers import to_apilist
from civicboom.lib.authentication      import authorize, get_lowest_role_for_user
from civicboom.lib.permissions         import account_type, role_required, age_required, has_role_required, raise_if_current_role_insufficent
from civicboom.lib.accounts            import deny_pending_user
from civicboom.lib.widget              import widget_defaults, setup_widget_env


from cbutils.misc import now
import cbutils.worker as worker

#from civicboom.model.member            import account_types
import civicboom.lib.errors as errors
from cbutils.cbtv import log as t_log, log_start as t_log_start, log_end as t_log_end

import simplejson as json
import platform
import formencode

import logging
log      = logging.getLogger(__name__)
user_log = logging.getLogger("user")

__all__ = [
    # pylons environment
    "request", "response", "app_globals", "c", "url","config",

    # sqlalchemy environment
    "Session", "meta",

    # return types
    "abort", "redirect", "action_ok", "action_error", "render",

    # decorators
    "https",
    "authorize",
    "authenticate_form",
    "auto_format_output",
    "web_params_to_kwargs",
    "cacheable",
    "web",
    "auth",
    "account_type", "role_required", "age_required",
    #"account_types", #types for use with with account_type decorator
    
    #errors
    "errors",
    
    # i18n
    "_", "x_",
    "ungettext", "set_lang",

    # session managemnet - is is prefered that all access to the session is via accessors
    "session_get", "session_remove", "session_set", "session_keys", "session_delete",

    "set_flash_message",

    # permissions
    "raise_if_current_role_insufficent", "has_role_required",

    # get objects
    "get_member", "get_group", "get_content", "get_message",
    "get_members",
    "normalize_member",
    
    #cache
    
    
    #log
    "user_log",
    "t_log", "t_log_start", "t_log_end",
    
    # misc
    "BaseController",
    "authentication_token",
    "redirect_to_referer", #TODO? potential for removal?
    "logging",
    "overlay_status_message",
    "current_url", "current_referer",
    "to_apilist",
    "now", # passthough to get datetime.datetime.now() but can be overridden by automted tests and is the prefered way of getting now()
]


def x_(s):
    """
    Mark a string as needing translation, but don't actually do anything
    with it at the time

    Useful for formencode, where error strings need to be defined globally,
    then formencode will call _(s) internally at a later date
    """
    return s


#-------------------------------------------------------------------------------
# Render
#-------------------------------------------------------------------------------

def render(*args, **kwargs):
    if not config['beaker.cache.enabled']:
        if 'cache_key'    in kwargs:
            del kwargs['cache_key']
        if 'cache_expire' in kwargs:
            del kwargs['cache_expire']
    if len(args)==2:
        # if args is 'template_filename', 'def_name' then call the def
        return render_mako_def(*args, **kwargs)
    else:
        # else if only 'template_filename' call the template file
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
# Get Objects
#-------------------------------------------------------------------------------

# AllanC - These get methods are to be used by Controllers as they raise action_error's that can be be interperited by the auto_formatter
#          Librarys normally use the methods in lib.database.get_cached
#          NOTE!: Please check the imports for what version of get_???? you are using! This controler version or the db version

def get_member(member_search, set_html_action_fallback=False, search_email=False):
    """
    Shortcut to return a member and raise not found automatically (as these are common opertations every time a member is fetched)
    """
    # Concept of 'me' in API
    if isinstance(member_search, basestring) and member_search.lower()=='me':
        if not c.logged_in_persona:
            raise action_error(_("cannot refer to 'me' when not logged in"), code=400)
        member_search = c.logged_in_persona
    member = _get_member(member_search)
    if not member and search_email:
        member = _get_member_email(member_search)
    if not member:
        raise action_error(_("member %s not found" % member_search), code=404)
    if member.status != "active":
        raise action_error(_("member %s is inactive" % member.username) , code=404)
    if set_html_action_fallback:
        # AllanC - see _get_content for rational behind this
        c.html_action_fallback_url = url('member', id=member.username)
    return member


def get_group(id, is_current_persona_admin=False, is_current_persona_member=False, set_html_action_fallback=False):
    """
    Shortcut to return a group and raise not found or permission exceptions automatically (as these are common opertations every time a group is fetched)
    """
    group = get_member(id, set_html_action_fallback=set_html_action_fallback)
    if group.__type__ != 'group':
        raise action_error(_("%s is not a group" % id), code=404)
    if group.status != "active":
        raise action_error(_("group %s is inactive" % group.username) , code=404)
    if is_current_persona_admin:
        raise_if_current_role_insufficent('admin', group)
    if is_current_persona_member and not group.get_membership(c.logged_in_persona):
        raise action_error(_("you are not a member of this group"), code=403)
    return group


#def get_membership(group,member):
#    return _get_membership(group,member)


def get_message(message, is_target=False, is_target_or_source=False):
    message = _get_message(message)
    if not message:
        raise action_error(_("Message does not exist"), code=404)
    if is_target and message.target != c.logged_in_persona:
        raise action_error(_("You are not the target of this message"), code=403)
    if is_target_or_source and c.logged_in_persona and not (message.target==c.logged_in_persona or message.source==c.logged_in_persona):
        raise action_error(_("You are not the target or source of this message"), code=403)
    return message


def get_content(id, is_editable=False, is_viewable=False, is_parent_owner=False, content_type=None, set_html_action_fallback=False):
    """
    Shortcut to return content and raise not found or permission exceptions automatically (as these are common opertations every time a content is fetched)
    """
    if not str(id).isdigit():
        raise action_error(_("_content ID should be a number"), code=400)
    content = _get_content(int(id))
    if not content:
        raise action_error(_("The _content you requested could not be found"), code=404)
    if content_type and content.__type__ != content_type:
        raise action_error(_("The _content you requested was not %s" % content_type), code=404)
    if is_viewable:
        if not content.viewable_by(c.logged_in_persona):
            raise errors.error_view_permission()
            #raise action_error(_("The _content you requested is not viewable"), code=403)
        if content.__type__ == "comment":
            user_log.debug("Attempted to view a comment as an article")
            raise action_error(_('Attempted to view a comment as _article'))
    if is_editable and not content.editable_by(c.logged_in_persona):
        # AllanC TODO: need to check role in group to see if they can do this
        raise action_error(_("You do not have permission to edit this _content"), code=403)
    if is_parent_owner and not content.is_parent_owner(c.logged_in_persona):
        raise action_error(_("You are not the owner of the parent _content"), code=403)
    if set_html_action_fallback:
        # AllanC - Many times when we fetch content in an 'action' we dont have a template set.
        # if we perform an action but dont have a page to display an error occurs
        # we set a url fallback.
        # This bool can be set to auto generate this as a convenience
        c.html_action_fallback_url = url('content', id=content.id)
    return content


def normalize_member(member):
    """
    Will return integer member_id or raise action_error
    """
    try   : member = member.id
    except: pass
    assert isinstance(member, basestring)
    return member


#-------------------------------------------------------------------------------
# Base Controller
#-------------------------------------------------------------------------------
class BaseController(WSGIController):
    
    def __before__(self):
        
        # If this is a multiple call to base then abort
        # Result is always set, so if it is not set then we know this is first call
        # This is needed because methods like member_actions.py:groups calls members.py:index. This would trigger 2 calls to base
        if hasattr(c, 'result'):
            return
        
        # AllanC - useful for debug
        #from pylons import session
        #print ""
        #print "CALL"
        #print request.environ.get("pylons.routes_dict")
        #print "GET"
        #print request.GET
        #print "POST"
        #print request.POST
        #print "SESSION"
        #print session
        #print "COOKIES"
        #print request.cookies
        
        # Setup globals c ------------------------------------------------------
        c.result = action_ok()  # Default return object
        
        # Request global - have the system able to easly view request details as globals
        current_request = request.environ.get("pylons.routes_dict")
        c.controller = current_request.get("controller")
        c.action     = current_request.get("action")
        c.id         = current_request.get("id")        
        #print "controller=%s action=%s id=%s" % (c.controller, c.action, c.id)
        
        c.format                   = current_request.get("format") or "html"
        c.subformat                = get_subdomain_format()
        c.auto_format_top_call     = False # Used as a flag to the auto_formatter to only output the top level decorator
        
        # For development we cant fake a subdomain call when acessing 127.0.0.1 :(
        # In the same way as we toggle_cache we can toogle_force_mobile
        if cookie_get("force_mobile") and not cookie_get('force_web'):
            log.debug('force_mobile cookie present')
            c.subformat = 'mobile'
        # If we are not forcing mobile - attempt to redirect first time mobile viewers to the correct subdomain
        # Redirect to mobile site if needed
        if not cookie_get("force_mobile") and cookie_get('force_web') and c.subformat=='mobile': # If user is forcing m. then remove the force_web cookie
            log.debug('removing force_web cookie')
            cookie_delete('force_web')
        if c.format=='html' and request.environ.get('is_mobile') and not cookie_get('force_web') and c.subformat=='web':
            mobile_url = url('current', sub_domain='m')
            log.debug('redirecting mobile user to %s' % mobile_url)
            redirect(mobile_url)
        
        c.authenticated_form       = None # if we want to call a controler action internaly from another action we get errors because the auth_token is delted, this can be set by the authenticated_form decorator so we allow subcall requests
        c.web_params_to_kwargs     = None
        c.html_action_fallback_url = None # Some actions like 'follow' and 'accept' do not have templates - a fallback can be set and @auto_format interperits this as a redirect fallback
        c.host                     = request.environ.get('HTTP_HOST', request.environ.get('SERVER_NAME'))
        c.etag_master_generated    = False

        request.environ['app_version'] = app_globals.version
        request.environ['node_name']   = platform.node()

        # Widget default settings
        widget_theme = request.params.get(config['setting.widget.var_prefix']+'theme')
        if widget_theme not in widget_defaults:
            widget_theme = config['setting.widget.default_theme']
        c.widget = dict(widget_defaults[widget_theme])
        if get_subdomain_format() == 'widget':
            setup_widget_env()
        c.widget['theme'] = widget_theme # Set the widget theme to the one requested (this is needed because theme 'light' could be set, it does not exist so gets 'basic', then overwrites theme with 'light' again from set_env)

        # Log out if missing logged_in -------------------------------
        # The cache is active if logged_in is false. If the cookie is
        # missing (deleted, expired, something else) but the main session cookie
        # is still there then caching could activate by accident. As such, if
        # the logged_in cookie is missing, force a logout.
        if session_get('logged_in_user') and not request.cookies.get("logged_in"):
            log.warning("logged_in_user is set, but logged_in is missing")
            session.invalidate()

        # Login ----------------------------------------------------------------
        # Fetch logged in user from session id (if present)
        
        login_session_fields = ['logged_in_user', 'logged_in_persona', 'logged_in_persona_path', 'logged_in_persona_role']
        logged_in = {}
        for field in login_session_fields:
            logged_in[field] = session_get(field)
            setattr(c, field, logged_in[field])
        
        c.logged_in_user         = _get_member(logged_in['logged_in_user'])
        c.logged_in_persona      = c.logged_in_user
        if c.logged_in_user and not c.logged_in_persona_role:
            c.logged_in_persona_role = 'admin'
        if logged_in['logged_in_user'] != logged_in['logged_in_persona']:
            group_persona = _get_group(logged_in['logged_in_persona'])
            if group_persona: # and group_persona.id == c.logged_in_persona_path[-1]: #Wanted to double check group permissions matched the group being set
                role = get_lowest_role_for_user()
                if role:
                    c.logged_in_persona      = group_persona
                    c.logged_in_persona_role = role
            
        # Set Env - In the event of a server error these will be visable
        for field in login_session_fields:
            request.environ[field] = str(getattr(c, field))
            #print request.environ[field]
        
        if c.logged_in_user:
            request.environ['logged_in_user_email'] = c.logged_in_user.email_normalized
        
        # Setup Langauge -------------------------------------------------------
        #  - there is a way of setting fallback langauges, investigate?
        if 'lang' in request.params:
            _lang = request.params['lang'] # If lang set in URL
            session_set('lang', request.params['lang'])
        elif session_get('lang'):
            _lang = session_get('lang') # Lang set for this users session
        #elif c.logged_in_persona has lang:
        #    self._set_lang(c.logged_in_persona.?)     # Lang in user preferences
        #elif request.environ.get("Accept-Language"):
        #   langs = request.environ.get("Accept-Language").split(";")[0]
        #   for lang in langs:
        #       ...
        else:
            _lang = config['lang'] # Default lang in config file

        c.lang = _lang
        set_lang(_lang)
        formencode.api.set_stdtranslation(domain="civicboom", languages=[_lang])
    
        
        # User pending regisration? --------------------------------------------
        # redirect to complete registration process
        if c.logged_in_user and c.logged_in_user.status == 'pending' and deny_pending_user(url('current')):
            set_flash_message(_('Please complete the registration process'))
            redirect(url(controller='register', action='new_user', id=c.logged_in_user.id))

        # Session Flash Message ------------------------------------------------
        flash_message_session = session_remove('flash_message')
        if flash_message_session:
            try:
                overlay_status_message(c.result, json.loads(flash_message_session))
            except ValueError:
                overlay_status_message(c.result,            flash_message_session )
        

    @t_log(lambda f,a,k: request.environ["pylons.routes_dict"]["controller"]+":"+request.environ["pylons.routes_dict"]["action"], bookmark=True)
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

            # now that the database objects officially exist, we can run the
            # jobs that use them
            worker.flush()
