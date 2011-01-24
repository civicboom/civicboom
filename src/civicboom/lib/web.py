from pylons import session, url, request, response, config, tmpl_context as c
from pylons.controllers.util  import redirect as redirect_pylons
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
from pprint import pformat
import logging
import os

log = logging.getLogger(__name__)
user_log = logging.getLogger("user")

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

def redirect(*args, **kwargs):
    if not c.format or c.format == "html" or c.format == "redirect":
        redirect_pylons(*args, **kwargs)
    else:
        raise Exception('unable to perform redirect with format=%s' % c.format)

def current_referer(protocol=None):
    #AllanC TODO - needs to enforce prosocol change - for login actions
    return request.environ.get('HTTP_REFERER')

def current_host(protocol=None):
    if not protocol:
        protocol = request.environ.get('HTTP_X_URL_SCHEME', 'http')
    return  protocol + "://" + request.environ.get('HTTP_HOST')

def current_url(protocol=None):
    target_url = current_host(protocol) + request.environ.get('PATH_INFO')
    if 'QUERY_STRING' in request.environ:
        target_url += '?'+request.environ.get('QUERY_STRING')
    return target_url

def redirect_to_referer():
    url_to = session_remove('login_action_referer') or current_referer() or '/'
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
    d = {
        "status" : "ok",
        "message": message,
        "data"   : data,
        "code"   : code,
    }
    if template:
        d["template"] = template
    return d

# AllanC - convenicen metod for returning lists
def action_ok_list(list, obj_type=None, **kwargs):
    return action_ok(data={'list': {
            'items' : list     ,
            'count' : len(list),
            'limit' : None     ,
            'offset': 0        ,
            'type'  : obj_type ,
        }
    }, **kwargs)


class action_error(Exception):
    def __init__(self, message=None, data={}, code=500, template=None, status='error'):
        assert not message or isinstance(message, basestring)
        assert isinstance(data, dict)
        assert isinstance(code, int)
        self.original_dict = {
            "status" : status,
            "message": message,
            "data"   : data,
            "code"   : code,
        }
        if template:
            self.original_dict["template"] = template
    def __str__( self ):
        return str(self.original_dict)

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

def _find_subformat():
    domain = request.environ.get("HTTP_HOST", "")
    if domain.startswith("mobile.") or domain.startswith("m.") or request.environ['is_mobile']:
        return "mobile"
    if domain.startswith("widget.") or domain.startswith("w."):
        return "widget"
    return "web"

def _find_template(result, type):
    #If the result status is not OK then use the template for that status
    if result.get('status', 'ok') == 'error':
        template_part = "error"
    else:
        # if template file is specified use it, else default to type/controller/action.mako
        template_part = result.get('template', '%s/%s' % (c.controller, c.action))

    # html is a meta-format -- if we are asked for a html template,
    # redirect to web, mobile or widget depending on the environment
    if type == "html":
        subformat = _find_subformat()
        paths = [
            os.path.join("html", subformat, template_part),
            os.path.join("html", "web",     template_part),
        ]
    else:
        paths = [
            os.path.join(type, template_part),
        ]

    for path in paths:
        if os.path.exists(os.path.join(config['path.templates'], path+".mako")):
            return path+".mako"

    raise Exception("Failed to find template for %s/%s/%s [%s]. Tried:\n%s" % (type, c.controller, c.action, result.get("template", "-"), "\n".join(paths)))


def setup_format_processors():
    def render_template(result, type):
        overlay_status_message(c.result, result)
        return render_mako(_find_template(result, type), extra_vars={"d": c.result['data']} )
        
    def format_json(result):
        response.headers['Content-type'] = "application/json"
        for n in list(result):
            if n not in ['status', 'message', 'data']:
                del result[n]
        return json.dumps(result)
        
    def format_xml(result):
        response.headers['Content-type'] = "text/xml"
        for n in list(result):
            if n not in ['status', 'message', 'data']:
                del result[n]
        return '<?xml version="1.0" encoding="UTF-8"?>' + dictToXMLString(result)
        
    def format_rss(result):
        response.headers['Content-type'] = "application/rss+xml; charset=utf-8"
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

@decorator
def auto_format_output(target, *args, **kwargs):
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

    # If no format has been set, then this is the first time this decorator has been called
    # We only format the output on the 'first master call' through this decorator
    # This allows us to freely call controler actions internally without haveing to worry about specifying a format because they will always return python dictionarys
    auto_format_output_flag = False
    if not c.format:
        current_request = request.environ.get("pylons.routes_dict")
        # config breaks in production?
        #c.format     = current_request.get("format", request.params.get('format', config['default_format'] ) )
        c.format        = request.params.get("format", current_request.get("format", "html" ) )
        auto_format_output_flag = True

    try:
        result = target(*args, **kwargs) # Execute the wrapped function
    except action_error as ae:
        if c.format == "python":
            raise
        else:
            if ae.original_dict.get('code') == 402 and (c.format=="html" or c.format=="redirect"):
                return redirect(url(controller='misc', action='upgrade_account'))
            result = ae.original_dict
    
    # After
    # Is result a dict with data?
    if auto_format_output_flag and hasattr(result, "keys"): #and 'data' in result # Sometimes we only return a status and msg, cheking for data is overkill
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
    #log.debug("returning pre-rendered stuff")
    return result


#-------------------------------------------------------------------------------
# Decorators
#-------------------------------------------------------------------------------

@decorator
def authenticate_form(target, *args, **kwargs):
    """
    slightly hacked version of pylons.decorators.secure.authenticated_form to
    support authenticated PUT and DELETE requests
    """
    if c.authenticated_form:
        return target(*args, **kwargs) # If already authenticated, pass through
    
    request  = get_pylons(args).request
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
    except ValueError as e:
        log.error("Failed to parse body: "+request.body)
        abort(500)

    # check for auth token in POST or other  # check params for PUT and DELETE cases
    if secure_form.token_key in request.POST:
        param_dict[secure_form.token_key] = request.POST[secure_form.token_key]
    if secure_form.token_key in kwargs:
        param_dict[secure_form.token_key] = kwargs[secure_form.token_key]
    if authenticated_form(param_dict): #authenticated_form(request.POST) or 
        #if authenticated_form(request.POST):
        if secure_form.token_key in request.POST:
            del request.POST[secure_form.token_key]
        if secure_form.token_key in kwargs:
            del kwargs[secure_form.token_key]
        c.authenticated_form = True
        return target(*args, **kwargs)

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
            c.target_url = current_url()
            c.post_values = param_dict
            return render_mako("html/web/misc/confirmpost.mako")
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


@decorator
def web_params_to_kwargs(target, *args, **kwargs):
    """
    converts any params from a form submission or query string into kwargs
    Security notice - Developers should be aware that kwargs could be passed by the user and override kwargs set in the orrigninal method call
                      If this behaviure is incorrect then rather than using dict.update() method, it should be made to SKIP existing kwargs and not overwreit them



    Some boilerplate to trick the function into thinking it is inside a pylons app

    FIXME: this doesn't work, so none of the tests do :(

    ->>> import civicboom.lib.web
    ->>> class fake_request():
    -...     params = {}
    -...
    ->>> civicboom.lib.web.request = fake_request()


    Create a function like so

    ->>> @web_params_to_kwargs
    -... def test(id, cake=2):
    -...     print id, cake


    Called normally, it works normally

    ->>> print test(1)
    -1 2


    Called with pylons paramaters, it works too

    ->>> print test(1, cake=3)
    -1 3


    Called with web paramaters, it uses those

    ->>> request.params = {"cake": 4}
    ->>> print test(1)
    -1 4
    """
    if c.web_params_to_kwargs:
        return target(*args, **kwargs) # If already processed, pass through
    
    
    arg_names = target.func_code.co_varnames[:target.func_code.co_argcount]
    params = request.params
    new_args = []
    new_kwargs = {}

    for k, v in kwargs.items():
        new_kwargs[k] = v
    # FIXME: need to detect if the function accepts a "**" type, as this could be "**foo" rather than "**kwargs"
    # NOTE: ** types aren't counted towards the function's argument count, so arg_names cuts it off
    if "kwargs" in target.func_code.co_varnames:
        new_kwargs.update(params)

    exclude_fields = ['pylons', 'environ', 'start_response']
    for exclude_field in exclude_fields:
        if exclude_field in new_kwargs:
            del new_kwargs[exclude_field]

    for n, varname in enumerate(arg_names):
        if varname in params:
            new_args.append(params[varname])
        elif varname in kwargs:
            new_args.append(kwargs[varname])
        else:
            new_args.append(args[n])
        if varname in new_kwargs:
            del new_kwargs[varname]

    #user_log.info("calling "+target.func_name+", given param names, defaults, kwargs, web params are "+pformat(arg_names)+pformat(args)+pformat(kwargs)+pformat(params))
    #user_log.info("calling "+target.func_name+", now have param values and kwargs "+pformat(new_args)+pformat(new_kwargs))
    c.web_params_to_kwargs = (new_args, new_kwargs)
    return target(*new_args, **new_kwargs) # Execute the wrapped function

