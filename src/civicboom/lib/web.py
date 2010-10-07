from pylons import session, url, request, response, config, tmpl_context as c
from pylons.controllers.util import redirect
from pylons.templating        import render_mako
from pylons.decorators.secure import authenticated_form, get_pylons, csrf_detected_message, secure_form
#from civicboom.lib.base import *

from webhelpers.html import literal

from civicboom.lib.xml_utils import dictToXMLString
#from civicboom.lib.misc import DictAsObj

import formencode

import os
import time
import json
from decorator import decorator
import logging
import os

log = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# UnicodeMultiDict Convertion
#-------------------------------------------------------------------------------
def multidict_to_dict(multidict):
    from webob.multidict import UnicodeMultiDict
    dict = {}
    if isinstance(multidict, UnicodeMultiDict):
        for key in multidict.keys():
            dict[key] = multidict[key]
    return dict
    

#-------------------------------------------------------------------------------
# Redirect Referer
#-------------------------------------------------------------------------------
def redirect_to_referer():
    url_to = request.environ.get('HTTP_REFERER') or '/'
    if url_to == url.current(): # Detect if we are in a redirection loop and abort
        log.warning("Redirect loop detected for "+str(url_to))
        #redirect('/')
    #print "yay redirecting to %s" % url_to
    return redirect(url_to)


#-------------------------------------------------------------------------------
# Session Timed Keys Management
#-------------------------------------------------------------------------------
# sessions can be given a key pair with an expiry time
# a fetch with session_get will get the session value, but will return None if it's _exipre pair has expired
    

def session_delete(key):
    if key           in session: del session[key]
    if key+'_expire' in session: del session[key+'_expire']

def session_remove(key):
    value = session_get(key)
    session_delete(key)
    return value

def session_set(key, value, duration=None):
    """
    duration in seconds
    """
    session[key] = value
    if duration:
        session[key+'_expire'] = time.time() + duration

def session_get(key):
    key_expire = key+'_expire'
    if key_expire in session:  
        if time.time() > float(session[key_expire]):
            session_delete(key)
    if key in session:
        return session[key]
    return None



#-------------------------------------------------------------------------------
# Action Message System
#-------------------------------------------------------------------------------
def set_flash_message(new_message):
    flash_message = None
    flash_message_string = session_get('flash_message')
    if flash_message_string:
        flash_message = json.loads(flash_message_string)
    flash_message = overlay_status_message(flash_message, new_message)
    session_set('flash_message', json.dumps(flash_message), 60 * 5)
    overlay_status_message(c.result, flash_message)


def action_ok(message=None, data={}, code=200, template=None):
    assert not message or isinstance(message, basestring)
    assert isinstance(data, dict)
    assert isinstance(code, int)
    return {
        "status" : "ok",
        "message": message,
        "data"   : data,
        "code"   : code,
        "template": template,
    }

class action_error(Exception):
    def __init__(message=None, data={}, code=500, template=None):
        #assert not message or isinstance(message, basestring)
        #assert isinstance(data, dict)
        #assert isinstance(code, int)
        self.original_dict = {
            "status" : "error",
            "message": message,
            "data"   : data,
            "code"   : code,
            "template": template,
        }

def overlay_status_message(master_message, new_message):
    """

    """
    # Setup master message
    if not master_message:
        master_message = {}
    master_message['status']  = master_message.get('status' ) or 'ok'
    master_message['message'] = master_message.get('message') or u'' 
    master_message['data']    = master_message.get('data'   ) or {}

    if isinstance(new_message, basestring):
        new_message = {'status':'ok', 'message':new_message}

    # Overlay new message (if dict)
    if isinstance(new_message, dict):
        if master_message['status'] == 'ok' and 'status' in new_message:
            master_message['status'] = new_message['status']
        if 'message' in new_message and new_message['message']:
            master_message['message'] += '\n' + new_message['message']

    # Overlay new message (if string)
    if isinstance(new_message, basestring):
        master_message['message'] += '\n' + new_message

    # Tidy message whitespace
    master_message['message'] = master_message['message'].strip()

    
    master_message['data'].update(new_message.get('data') or {})
    
    # Pass though all keys that are not already in master
    for key in [key for key in new_message.keys() if key not in master_message]:
        master_message[key] = new_message[key]

    return master_message


#-------------------------------------------------------------------------------
# Auto Format Output
#-------------------------------------------------------------------------------

def _find_template(result, type='html'):
    
    type_fallback = {
        'web'   : None  ,
        'mobile': 'web' ,
        'rss'   : None  ,
        'frag'  : 'web' ,
    }
    
    # Convert the type into the base folder structure
    if type=='html':
        type = 'web'
        if request.environ['is_mobile']:
            type = 'mobile'

    #If the result status is not OK then use the template for that status
    if result.get('status', 'ok') != 'ok':
        result['template'] = "%s" % result['status']

    if result.get('template'):
        template_part = result.get('template')               # Attempt to get template named in result
    else:
        template_part = '%s/%s' % (c.controller, c.action)   # Else fallback to controller/action
    
    def template_file_exisits(template_file):
        return os.path.exists(os.path.join(config['path.templates'], template_file))

    # Iterate through all possible templates using differnt fallback types
    template = None
    while template==None and type!=None:
        template = "%s/%s.mako" % (type, template_part)
        if not template_file_exisits(template):
            template = None
            type     = type_fallback[type]

    if not template:
        log.warn("Can't find template")

    return template



def setup_format_processors():
    
    def render_template(result, type):
        overlay_status_message(c.result, result)
        return render_mako(_find_template(result, type), extra_vars={"d": c.result['data']} )
        
    def format_json(result):
        #response.headers['Content-type'] = "application/json" #AllanC - Is this fixed now? - this used to break the error middleware when returning error codes like 403, long term this needs to be fixed
        return json.dumps(result)
        
    def format_xml(result):
        response.headers['Content-type'] = "text/xml"
        return dictToXMLString(result)
        
    def format_rss(result):
        #response.headers['Content-type'] = "application/rss+xml"
        #response.headers['Content-type'] = "text/xml"
        return render_template(result, 'rss')
    
    def format_frag(result):
        return render_template(result, 'frag')
        
    def format_html(result):
        return render_template(result, 'html')

    def format_redirect(result):
        """
        A special case for compatable browsers making REST calls
        Actions can be performed, session message set, and the client redirected back to it's http referer with the session flash message displayed
        
        Format Redirector 
        Will
          1.) take note of originator http_referer *[this method call]
          
          2.) perform an action [in auto_format_output]
          
          3.) set the flash message to the session [format_redirect in format_processors_end]
          4.) redirect to the originator http_referer
          
          Note: data part of the result is now LOST!
          
          5.) upon reloading the page the [base controler] will extract the flash message form the session
          6.) display message in a cool scrolling pop up box
        """
        if 'message' in result:
            set_flash_message(result) # Set flash message
        redirect_to_referer()
        
        #action_redirect = session_remove('action_redirect')
        #if action_redirect and action_redirect.find(url.current())<0: # If the redirector contains the current URL path we are in an infinate loop and need to return just the text rather than a redirect
        #    return redirect(action_redirect)
            
        #log.warning("Redirect loop detected for "+str(action_redirect))
        #return redirect("/")

    return dict(
        python   = lambda result:result,
        json     = format_json,
        xml      = format_xml,
        rss      = format_rss,
        html     = format_html,
        frag     = format_frag,
        redirect = format_redirect,
    )


format_processors = setup_format_processors()

def auto_format_output():
    """
    Once a controler aciton has finished processing it will return a python dict
    This decorator inspects the python dict and converts the dict into one of the following:
        - JSON
        - XML
        - RSS
        - HTML (with htmlfill overlay if nessisary) [auto selecting mobile template if needed]
            + Web 
            + Mobile
        - HTML_FRAGMENT
            Used to generate fragments of pages for use with AJAX calls or as a component of a static page
        - PYTHON (just the plain python dict for internal calls)
        - REDIRECT (compatable old borswer action to have session message set and redirected to referer)
            
    Should be passed a python dictonary containing
        {
            data   : the python dict to render (default {})
            
            status : 'ok' or 'error' (optional defaults to ok)
            message: the flash message or error message (optional: default '')
            
            template: (required for html rendering) the template name, will default to XML if format==html and template not specifyed
        }
    """
    def my_decorator(target):
        def wrapper(target, *args, **kwargs):
            
            #if format in format_processors_pre:
            #    format_processors[format]()
            
            # Origninal method call
            try:
                result = target(*args, **kwargs) # Execute the wrapped function
            except action_error as ae:
                if c.format == "python":
                    raise
                else:
                    result = ae.original_dict

            # After
            # Is result a dict with data?
            if hasattr(result, "keys"): #and 'data' in result # Sometimes we only return a status and msg, cheking for data is overkill
                
                if c.format=='html' and not _find_template(result):
                    log.warning("Format HTML with no template")
                    c.format='xml' #If format HTML and no template supplied fall back to XML
                
                # set the HTTP status code
                if 'code' in result:
                    response.status = int(result['code'])
                    # Status code redirector has been disabled - old notes:
                    # This will trigger the error document action in the error controler after this action is returned
                    # problem with the error document intercepting is that we loose the {'message':''}
                    # a new call to error/document is made from scratch, this sets the default format to html again! if the format is in the query string this overrides it, but in the url path it gets lost
                    # Verifyed as calling error/document.html/None
                    #del result['code']
                
                # Render to format
                if c.format in format_processors:
                    return format_processors[c.format](result)
                else:
                    log.warning("Unknown format: "+str(c.format))
                
            # If pre-rendered HTML or JSON or unknown format - just pass it through, we can not format it any further
            log.debug("returning pre-rendered stuff")
            return result
        
        return decorator(wrapper)(target) # Fix the wrappers call signiture
    return my_decorator


#-------------------------------------------------------------------------------
# Decorators
#-------------------------------------------------------------------------------

@decorator
def authenticate_form(func, *args, **kwargs):
    """
    slightly hacked version of pylons.decorators.secure.authenticated_form to
    support authenticated PUT and DELETE requests
    """
    if c.authenticated_form: return func(*args, **kwargs) # If already authenticated, pass through
    
    request = get_pylons(args).request
    response = get_pylons(args).response

    # XXX: Shish - the body is not parsed for PUT or DELETE, so parse it ourselves
    # FIXME: breaks with multipart uploads
    try:
        # request.body = "foo=bar&baz=quz"
        if request.body and request.method in ["PUT", "DELETE"]:
            param_list = request.body.split("&") # ["foo=bar", "baz=qux"]
            param_pair = [part.split("=", 2) for part in param_list] # [("foo", "bar"), ("baz", "qux")]
            param_dict = dict(param_pair) # {"foo": "bar", "baz": "qux"}
        else:
            param_dict = {}
    except ValueError, e:
        log.error("Failed to parse body: "+request.body)
        abort(500)

    # check for auth token in POST or other  # check params for PUT and DELETE cases
    if authenticated_form(request.POST) or authenticated_form(param_dict):
        if authenticated_form(request.POST):
            del request.POST[secure_form.token_key]
        c.authenticated_form = True
        return func(*args, **kwargs)

    # no token = can't be sure the user really intended to post this, ask them
    else:
        log.warn('Cross-site request forgery detected, request denied: %r '
                 'REMOTE_ADDR: %s' % (request, request.remote_addr))
        #abort(403, detail=csrf_detected_message)
        response.status_int = 403
        
        format = c.format
        if args[-1] in format_processors:
            format = args[-1]
        
        if format in ['html','redirect']:
            c.target_url = "http://" + request.environ.get('HTTP_HOST') + request.environ.get('PATH_INFO')
            if 'QUERY_STRING' in request.environ:
                c.target_url += '?'+request.environ.get('QUERY_STRING')
            c.post_values = param_dict
            return render("web/design09/misc/confirmpost.mako")
        else:
            raise action_error(message="Cross-site request forgery detected, request denied: include a valid authentication_token in your form POST")


def cacheable(time=60*60*24*365, anon_only=True):
    def _cacheable(func, *args, **kwargs):
        from pylons import request, response
        if not anon_only or 'civicboom_logged_in' not in request.cookies: # no cache for logged in users
            response.headers["Cache-Control"] = "public,max-age=%d" % time
            response.headers["Vary"] = "cookie"
            if "Pragma" in response.headers: del response.headers["Pragma"]
            #log.info(pprint.pformat(response.headers))
        return func(*args, **kwargs)
    return decorator(_cacheable)


def web_params_to_kwargs():
    """
    converts any params from a form submission or query string into kwargs
    """
    def my_decorator(target):
        def wrapper(target, *args, **kwargs):
            kwargs.update(request.params) # Update the kwargs
            result = target(*args, **kwargs) # Execute the wrapped function
            return result
        return decorator(wrapper)(target) # Fix the wrappers call signiture
    return my_decorator
