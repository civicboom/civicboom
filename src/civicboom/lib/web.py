from pylons import url as url_pylons, session, request, response, config, tmpl_context as c, app_globals
from pylons.controllers.util  import redirect as redirect_pylons
from pylons.templating        import render_mako
from pylons.decorators.secure import authenticated_form, get_pylons, secure_form
from pylons.controllers.util  import etag_cache as pylons_etag_cache # Used for removing eTags on errors

from cbutils.cbxml import dictToXMLString

from civicboom.lib.widget import widget_defaults

import os
import time
import simplejson as json
import re
from decorator import decorator
import logging
import urllib

log = logging.getLogger(__name__)
user_log = logging.getLogger("user")


#-------------------------------------------------------------------------------
# UnicodeMultiDict Convertion
#-------------------------------------------------------------------------------
def multidict_to_dict(multidict):
    from webob.multidict import UnicodeMultiDict
    dict = {}
    if isinstance(multidict, UnicodeMultiDict):
        for key in multidict:
            dict[key] = multidict[key]
    return dict


#-------------------------------------------------------------------------------
# Subdomain format
#-------------------------------------------------------------------------------

subdomain_formats = {
    ''      : 'web'    ,
    'www'   : 'web'    ,
    'widget': 'widget' ,
    'm'     : 'mobile' ,
    'api-v1': 'api'    ,
}


def get_subdomain_format(environ=None):
    """
    hardcoded list of ifs, because this function is called millions of times,
    and dictionary lookups (especially from globals (10x especially from
    app_globals)) are comparatively slow (only 0.01ms vs 0.1ms, but over a
    million calls it adds up)
    """
    if not environ:
        environ = request.environ
    subdomain = environ.get("HTTP_HOST", "").split(".")[0]
    if subdomain == "w" or subdomain == "widget":
        return "widget"
    if subdomain == "m" or subdomain == "mobile":
        return "mobile"
    return 'web'

def get_domain(environ=None):
    if not environ:
        environ = request.environ
    return ".".join(environ.get("HTTP_HOST", "").split(".")[1:])

#-------------------------------------------------------------------------------
# URL Generation
#-------------------------------------------------------------------------------

from cbutils.cbtv import log as t_log

@t_log("generating url")
def url(*args, **kwargs):
    """
    Passthough for Pylons URL generator with a few new features
    """
    import cbutils.worker as w
    if hasattr(w, 'url'):
        _url = w.url
    else:
        _url = url_pylons

    # BUGFIX - if protocol is passed as None it goes baddgy ... this remove is ... seems unnessisary because url shoud deal with it (sigh)
    #if 'protocol' in kwargs and not isinstance(kwargs['protocol'], basestring):
    #    del kwargs['protocol']
    # if protocol is None, something has gone weird, so complain loudly...
    assert (('protocol' not in kwargs) or isinstance(kwargs['protocol'], basestring))

    # - workaround for routes bug where it can't handle sub_domain=None or unspecified
    #   https://bitbucket.org/bbangert/routes/issue/50
    # - also workaround for some weirdness - url('members') turns into a fully qualified
    #   URL with no subdomain without this o_O
    #if 'sub_domain' not in kwargs:
    #    kwargs['sub_domain'] = _url.environ.get("HTTP_HOST", "").split(".")[0]

    # Encode current widget state into URL if in widget mode
    if kwargs.get('sub_domain')=='widget' or (get_subdomain_format(_url.environ)=='widget' and 'sub_domain' not in kwargs): # If widget and not linking to new subdomain
        widget_var_prefix = config['setting.widget.var_prefix'   ]
        widget_theme      = config['setting.widget.default_theme']
        try:
            # Just in case c does not exisit in thread
            widget_theme = c.widget['theme']
        except:
            pass
        if kwargs.get('theme'):
            widget_theme = kwargs['theme']
        
        # AllanC - ***ING MASSIVE HACK ... it's 5:30 AM FFS!
        if widget_theme=='gradient':
            kwargs[widget_var_prefix+'theme'] = widget_theme
        else:
            #print "-----------------------------------------"
            widget_default = dict(widget_defaults.get(widget_theme))
            #print widget_default
            for key, default_value in widget_default.iteritems():
                default_value = str(default_value)
                # Check if value is the same as widget default - there is no need to add this to the URL if they match
                required_fields = ['theme']
                try:
                    w_key = widget_var_prefix + key
                    c_val = c.widget[key]
                    try:
                        c_val = c_val['username']
                    except:
                        c_val = str(c_val)
                    #print "key:%s dv:%s cv:%s" %(key,default_value, c_val)
                    if key in required_fields or c_val!=default_value:
                        #print "STORE: %s:%s" % (w_key,c_val)
                        kwargs[w_key] = c_val
                except:
                    pass

    args = list(args)
    if 'current' in args:
        args.remove('current')
        return _url.current(*args, **kwargs)
    else:
        return _url(        *args, **kwargs)




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


def current_protocol():
    return request.environ.get('wsgi.url_scheme', 'http')


def current_host(protocol=None):
    if not protocol:
        protocol = current_protocol()
    return  protocol + "://" + request.environ.get('HTTP_HOST')


def current_url(protocol=None):
    target_url = current_host(protocol) + request.environ.get('PATH_INFO')
    if 'QUERY_STRING' in request.environ:
        target_url += '?'+request.environ.get('QUERY_STRING')
    return target_url


def redirect_to_referer():
    url_to = session_remove('login_action_referer') or current_referer() or '/' #cookie_get('login_action_referer') or
    if url_to == url('current'): # Detect if we are in a redirection loop and abort
        log.warning("Redirect loop detected for %s" % url_to)
        #redirect('/')
    #print "yay redirecting to %s" % url_to
    return redirect(url_to)


#-------------------------------------------------------------------------------
# Session Timed Keys Management
#-------------------------------------------------------------------------------
# sessions can be given a key pair with an expiry time
# a fetch with session_get will get the session value, but will return None if it's _exipre pair has expired
    

def session_delete(key):
    if key in session:
        del session[key]
    if key+'_expire' in session:
        del session[key+'_expire']


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


def session_keys():
    return [key for key in session if '_expire' not in key]

#-------------------------------------------------------------------------------
# Cookie Timed Keys Management
#-------------------------------------------------------------------------------
# cookies can be given a key pair with an expiry time
# a fetch with session_get will get the session value, but will return None if it's _exipre pair has expired

# http://pythonpaste.org/webob/reference.html#id5


def cookie_delete(key):
    #log.debug("delete %s" % key)
    try:
        response.unset_cookie(key)
    except:
        pass
    try:
        response.delete_cookie(key)
    except:
        pass


def cookie_remove(key):
    value = cookie_get(key)
    cookie_delete(key)
    return value


def cookie_set(key, value, max_age=3600*24*365, secure=None, sub_domain=None, domain=None):
    """
    duration in seconds
    """
    #print "COOKIE setting %s:%s" %(key, value)
    if secure == None:
        secure = (current_protocol() == "https")
    if sub_domain != None:
        domain = sub_domain+'.'+(domain or get_domain())
    response.set_cookie(key, value, max_age=max_age, secure=secure, path='/', domain=domain) #, domain=request.environ.get("HTTP_HOST", "") # AllanC - domain remarked because firefox 3.5 was not retaining the logged_in cookie with domain localhost


def cookie_get(key):
    #log.debug("getting %s:%s" %(key, request.cookies.get(key)))
    # GregM Pass the cookie through urllib unquote_plus to fix any url encoding (and replace + with space!)
    if request.cookies.get(key):
        return urllib.unquote_plus(request.cookies.get(key))
    return request.cookies.get(key)



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


def action_ok(message=None, data={}, code=200, **kwargs):
    assert not message or isinstance(message, basestring)
    assert isinstance(data, dict)
    assert isinstance(code, int)
    d = {
        "status" : "ok",
        "message": message,
        "data"   : data,
        "code"   : code,
    }
    #if template:
    #    d["template"] = template
    d.update(kwargs)
    return d




class action_error(Exception):
    def __init__(self, message=None, data={}, code=500, status='error', **kwargs):
        assert isinstance(message, basestring)
        assert isinstance(data, dict)
        assert isinstance(code, int)
        self.original_dict = {
            "status" : status,
            "message": message,
            "data"   : data,
            "code"   : code,
        }
        self.original_dict.update(kwargs)
        #if template:
        #    self.original_dict["template"] = template

    def __str__( self ):
        return str(self.original_dict)


def overlay_status_message(master_message, new_message):
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
    for key in [key for key in new_message if key not in master_message]:
        master_message[key] = new_message[key]

    return master_message


#-------------------------------------------------------------------------------
# Auto Format Output
#-------------------------------------------------------------------------------


def _find_template(result, type):
    #If the result status is not OK then use the template for that status
    if result.get('status', 'ok') == 'error':
        template_part = "error"
    else:
        # if template file is specified use it, else default to type/controller/action.mako
        template_part = result.get('template', '%s/%s' % (c.controller, c.action))

    # html is a meta-format -- if we are asked for a html template,
    # redirect to web, mobile or widget depending on the environment
    #subformat = get_subdomain_format() # Proto: Set once in auto formatter with c.format to avoid unecessary repeated calls
    subformat = c.subformat
    if type == "html":
        paths = [
            os.path.join("html", subformat, template_part),
            os.path.join("html", "web",     template_part),
        ]
        if subformat=='widget':
            paths.insert(0, os.path.join("html", subformat, c.widget['theme'], template_part)) # AllanC - widgets have a special case and can have multiple themes - see addtion for list types below as well
        ## AllanC: TODO
        ## if there is no web template but there is a frag for this template part
        ## wrap the fragment in a frag_container.mako
        ## WIP see web/frag.mako
    else:
        paths = [
            os.path.join(type, template_part),
        ]

    # So far we may have been unable to find a template file for this action
    # It may be a 'list' with an 'object type'. we can add the default list renderer for the list as a last ditch effort
    if 'data' in result and 'list' in result['data'] and 'type' in result['data']['list']:
        list_type = result['data']['list']['type']
        list_part = None
        if   list_type == 'contents':
            list_part = 'contents/index'
        elif list_type == 'members':
            list_part = 'members/index'
        elif list_type == 'messages':
            list_part = 'messages/index'
        if list_part:
            paths = paths + [
                os.path.join(type, list_part)              ,
                os.path.join("html", subformat, list_part) ,
                os.path.join("html", "web"    , list_part) ,
            ]
            # HACK - AllanC - insert 1 so it's after os.path.join(type, list_part)
            if subformat=='widget':
                paths.insert(1, os.path.join("html", subformat, c.widget['theme'], list_part)) # AllanC - widgets have a special case and can have multiple themes - hack here to inset at item 1
    
    for path in paths:
        if os.path.exists(os.path.join(config['path.templates'], path+".mako")):
            log.debug('Rendering Template %s.mako' % path)
            return path+".mako"
    
    # TO BE REMOVED
    # AllanC - this can be removed at a later date if needed, but the GOOGLE BOT IS DOING MY NUT IN!!!!
    #          I think the google bot has a list of URL's that it's scanning from months ago .. we dont want server errors for this
    if type=='rss' and c.action=='get_widget':
        return 'html/web/error.mako'
    
    raise Exception("Failed to find template for %s/%s/%s [%s]. Tried:\n%s" % (type, c.controller, c.action, result.get("template", "-"), "\n".join(paths)))


def _find_template_basic(controller=None, action=None, format=None):
    controller = controller or c.controller
    action = action or c.action
    format = format or c.format or "html"
    template_part = '%s/%s' % (controller, action)
    #subformat = get_subdomain_format() # Proto: Set once in auto formatter with c.format to avoid unecessary repeated calls
    subformat = c.subformat
    if format == "html":
        paths = [
            os.path.join("html", subformat, template_part),
            os.path.join("html", "web",     template_part),
        ]
        ## AllanC: TODO
        ## if there is no web template but there is a frag for this template part
        ## wrap the fragment in a frag_container.mako
        ## WIP see web/frag.mako
    else:
        paths = [
            os.path.join(format, template_part),
        ]
    for path in paths:
        if os.path.exists(os.path.join(config['path.templates'], path+".mako")):
            return path+".mako"
    raise Exception("Failed to find template for %s/%s/%s [%s]. Tried:\n%s" % (format, controller, action, "", "\n".join(paths)))


def setup_format_processors():
    def render_template(result, type):
        overlay_status_message(c.result, result)
        return render_mako(_find_template(result, type), extra_vars={"d": c.result['data']} )
        
    def format_json(result):
        response.headers['Content-type'] = "application/json; charset=utf-8"
        for n in list(result):
            if n not in ['status', 'message', 'data']:
                del result[n]
        cb = request.GET.get("callback")
        json_data = json.dumps(result, use_decimal=True)
        if cb and re.match("^[a-zA-Z][a-zA-Z0-9_]*$", cb):
            json_data = u"%s(%s)" % (cb, json_data)
        return json_data
        
    def format_xml(result):
        response.headers['Content-type'] = "text/xml; charset=utf-8"
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
        #print result
        #import traceback
        #traceback.print_stack()
        # AllanC - if we perform an HTML action but have not come from our site and used format='redirect' then we want the redirect to the html object that the action has been performed on rather than displaying an error
        if c.html_action_fallback_url: #and c.format == 'html'
            set_flash_message(result)
            redirect(c.html_action_fallback_url)
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
            
        #log.warning("Redirect loop detected for %s" % action_redirect)
        #return redirect("/")
    
    def format_print(result):
        if result.get('status', 'ok') == 'error':
            return render_template(result, 'html')
        frag = render_template(result, 'frag')
        return render_mako('print/wrapper.mako', extra_vars={"inner_html": frag})
    
    def format_ical(result):
        abort(501)
        
    def format_pdf(result):
        import subprocess
        print_formatted = format_print(result)
        
        import ho.pisa as pisa
        import cStringIO as StringIO
        
        io = StringIO.StringIO()
        
        def link_handler(uri, rel):
            if uri[0:4] != 'http':
                uri = 'https://localhost' + uri
            return uri
            
        pdf = pisa.pisaDocument(StringIO.StringIO(print_formatted.encode("UTF-8")), io, link_callback = link_handler, encoding="UTF-8")# path, link_callback, debug, show_error_as_pdf, default_css, xhtml, encoding, xml_output, raise_exception, capacity)
        if not pdf.err:
            response.headers['Content-type'] = "application/pdf"
            return io.getvalue()
        return pdf.err
    
    

    return {
        'python'   : lambda result:result,
        'json'     : format_json,
        'xml'      : format_xml,
        'rss'      : format_rss,
        'html'     : format_html,
        'frag'     : format_frag,
        'redirect' : format_redirect,
        'print'    : format_print,
        'ical'     : format_ical,
        'pdf'      : format_pdf,
    }


format_processors = setup_format_processors()


@decorator
def auto_format_output(target, *args, **kwargs):
    """
    Once a controller aciton has finished processing it will return a python dict
    This decorator inspects the python dict and converts the dict into one of the following:
        - JSON
        - XML
        - RSS
        - HTML (with htmlfill overlay if necessary) [auto selecting mobile template if needed]
            + Web
            + Mobile
        - HTML_FRAGMENT
            Used to generate fragments of pages for use with AJAX calls or as a component of a static page
        - PYTHON (just the plain python dict for internal calls)
        - REDIRECT (compatable old broswer action to have session message set and redirected to referer)
        - ICAL (calender support)
        - PDF (generate PDF for printing/archiving)
            
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
    # This allows us to freely call controler actions internally without having to worry about specifying a format because they will always return python dictionarys
    auto_format_output_flag = False # Each call to auto_format must have it's own local copy of auto_format_output_flag and not rely on the global c.
    if not c.auto_format_top_call:
        c.auto_format_top_call  = True # This prevent any subsiquent calls formatting therir output
        auto_format_output_flag = True

    try:
        result = target(*args, **kwargs) # Execute the wrapped function
    except action_error as ae:
        if not auto_format_output_flag: # If this is not the top level call then keep propergating the error up wards
            raise ae
        else:
            result = ae.original_dict # else, capture the error as the result to format and return
            
            pylons_etag_cache("") # remove any etags because errors should never be cached.
            
            # Special processing for some types of error code
            if result.get('code') == 404 and request.environ.get("HTTP_REFERER", "-") == "-":
                # 404 with no referer is normally a web spider
                pass
            else:
                # Log big user error as small server error
                user_log.debug('%s: %s' % (result.get('code'), result.get('message')))

            if c.format == "html" or c.format == "redirect":
                if result.get('code') == 402:
                    return redirect(url(controller='misc', action='about', id='upgrade_plans'))
            if c.format == "html" and c.html_action_fallback_url:
                set_flash_message(result) # Set flash message
                return redirect(c.html_action_fallback_url)
            
            
    
    # After
    # Is result a dict with data?
    if auto_format_output_flag and isinstance(result, dict):
        
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
            log.warning("Unknown format: %s" % c.format)
        
    # If pre-rendered HTML or JSON or unknown format - just pass it through, we can not format it any further
    #log.debug("returning pre-rendered stuff")
    return result


#-------------------------------------------------------------------------------
# Decorators
#-------------------------------------------------------------------------------

@decorator
def authenticate_form(_target, *args, **kwargs):
    """
    slightly hacked version of pylons.decorators.secure.authenticated_form to
    support authenticated PUT and DELETE requests
    """
    if c.authenticated_form:
        return _target(*args, **kwargs) # If already authenticated, pass through
    
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
        return _target(*args, **kwargs)

    # no token = can't be sure the user really intended to post this, ask them
    else:
        log.warn('Cross-site request forgery detected, request denied: %r '
                 'REMOTE_ADDR: %s' % (request, request.remote_addr))
        #abort(403, detail=csrf_detected_message)
        response.status_int = 403
        
        if c.format in ['html','redirect']:
            c.target_url = current_url()
            c.post_values = param_dict
            #return render_mako("html/web/misc/confirmpost.mako")
            return action_ok(template='misc/confirmpost', code=response.status_int)
        else:
            raise action_error(message="Cross-site request forgery detected, request denied: include a valid authentication_token in your form POST")


def cacheable(time=60*60*24*365, anon_only=True):
    """
    A static decorator to inform nginx to cache the returned content
    """
    def _cacheable(func, *args, **kwargs):
        if config['cache.static_decorators.enabled']:
            from pylons import request, response
            if not anon_only or 'logged_in' not in request.cookies: # no cache for logged in users
                response.headers["Cache-Control"] = "public,max-age=%d" % time
                response.headers["Vary"] = "Cookie"
                if "Pragma" in response.headers:
                    del response.headers["Pragma"]
        return func(*args, **kwargs)
    return decorator(_cacheable)


@decorator
def web_params_to_kwargs(_target, *args, **kwargs):
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
        return _target(*args, **kwargs) # If already processed, pass through
    
    
    arg_names = _target.func_code.co_varnames[:_target.func_code.co_argcount]
    params = request.params
    new_args = []
    new_kwargs = {}

    for k, v in kwargs.items():
        new_kwargs[k] = v
    # FIXME: need to detect if the function accepts a "**" type, as this could be "**foo" rather than "**kwargs"
    # NOTE: ** types aren't counted towards the function's argument count, so arg_names cuts it off
    if "kwargs" in _target.func_code.co_varnames:
        new_kwargs.update(params)

    # AllanC - it appears that routes variables are automatically forwarded as kwargs, they are to be removed, we dont want unneeded kwargs for caching. Could these not be set in the first place?
    # 'client_contact' is removed at the is not relevent for the API calls but should be logged in the request should we need to contact API users (see API docs)
    exclude_fields = ['pylons', 'environ', 'start_response', 'controller', 'action', 'format', 'sub_domain', 'client_contact'] 
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

    c.web_params_to_kwargs = (new_args, new_kwargs)
    return _target(*new_args, **new_kwargs) # Execute the wrapped function
