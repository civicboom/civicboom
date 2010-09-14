from pylons import session, url, request, response, config, tmpl_context as c
from pylons.controllers.util import redirect
from pylons.templating        import render_mako
#from civicboom.lib.base import *

from webhelpers.html import literal

from civicboom.lib.xml_utils import dictToXMLString

import formencode

import time
import json
from decorator import decorator
import logging

log = logging.getLogger(__name__)


#-------------------------------------------------------------------------------
# Misc
#-------------------------------------------------------------------------------

def flash_message(message):
    if hasattr(message, 'keys'):
        message = json.dumps(message)
    #message.replace('\n','<br/>\n')
    if 'flash_message' in session:
        session['flash_message'] = session['flash_message'] + literal("<br/>") + message
    else:
        session['flash_message'] = message

def redirect_to_referer():
    url_to = request.environ.get('HTTP_REFERER')
    if url_to == url.current(): # Detect if we are in a redirection loop and abort
        log.warning("Redirect loop detected for "+str(url_to))
        redirect('/')
    if not url_to:
        #url_to = url.current()
        redirect('/')
    return redirect(url_to)

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
# Session Timed Keys Management
#-------------------------------------------------------------------------------
# sessions can be given a key pair with an expiry time
# a fetch with session_get will get the session value, but will return None if it's _exipre pair has expired

def session_remove(key):
    if key           in session: del session[key]
    if key+'_expire' in session: del session[key+'_expire']

def session_set(key, value, duration):
    """
    duration in seconds
    """
    session[key]           = value
    session[key+'_expire'] = time.time() + duration
    pass

def session_get(key):
    key_expire = key+'_expire'
    if key_expire in session:  
        if time.time() > float(session[key_expire]):
            session_remove(key)
    if key in session:
        return session[key]
    return None

#-------------------------------------------------------------------------------
# Action Redirector
#-------------------------------------------------------------------------------
def action_redirector():
    """
    Action Redirector Decorator
    Will
      0.) take note of originator http_referer
      1.) perform an action
      2.) set the flash message to the result of the action
      3.) redirect to the originator http_referer

    Anything wrapped by the fuction must return a string as this will be aggregated out via 'flash message' or 'JSON'

    -- the beauty of this decorator is that AJAX requests have no http_referer, so the action return plain text without an http_referer,
    -- thus actions can be used by both "Compatable web HTTP requests" or 'AJAX requests' without chnaging any code
    Chrome sends a referrer with ajax requests, which breaks this; solution is adding an explicit format to the url (eg /controller/action.json)

    Todo enchncement: it is possible for an infinate redirect loop if the session is lost, it would be nice if when the decorator is attached to a method, it takes note of that method name, if that method name is part of the url e.g the string "/methodname/" then just return plain text rather than a redirect
    """

    def my_decorator(target):
        def wrapper(target, *args, **kwargs):
            if session_get('action_redirect') == None and 'HTTP_REFERER' in request.environ:
                session_set('action_redirect', request.environ.get('HTTP_REFERER'), 60 * 5)

            result = target(*args, **kwargs) # Execute the wrapped function

            if len(args) > 1 and args[-1] == "json": # assumes action(self, format) or action(self, id, format)
                response.headers['Content-type'] = "application/json"
                return result
            else:
                action_redirect = session_get('action_redirect')
                session_remove('action_redirect')
                if action_redirect and action_redirect.find(url.current())<0: #If the redirector contains the current URL path we are in an infinate loop and need to return just the text rather than a redirect
                    flash_message(result)
                    return redirect(action_redirect)
                else:
                    log.warning("Redirect loop detected for "+str(action_redirect))
                    return redirect("/")

        return decorator(wrapper)(target) # Fix the wrappers call signiture
    return my_decorator

#-------------------------------------------------------------------------------
# Actions
#-------------------------------------------------------------------------------

def action_ok(msg=None, data=None, code=200):
    return {
        "status" : "ok",
        "message": msg,
        "data"   : data,
        "code"   : code,
    }

def action_error(msg=None, data=None, code=400):
    return {
        "status" : "error",
        "message": msg,
        "data"   : data,
        "code"   : code,
    }

def action_msg(dict):
    """
    Takes a large python dictonary and just returns a dict with status and msg and a blank data
    This is used in auto formatting when we want status to be flashed through
    """
    a = {'status':'ok', 'msg':'', 'data':''}
    if 'status'  in dict: a['status']  = dict['status']
    if 'message' in dict: a['message'] = dict['message']
    return a

#-------------------------------------------------------------------------------
# Auto Format Output
#-------------------------------------------------------------------------------

def get_format_processors():
    def format_json(result):
        #response.headers['Content-type'] = "application/json"
        return json.dumps(result)
        
    def format_xml(result):
        response.headers['Content-type'] = "text/xml"
        return dictToXMLString(result)
        
    def format_rss(result):
        return 'implement RSS' # TODO: ???
    
    def format_html(result):
        c.data = result['data']                                            # Set standard template data dict for template to use
        if 'message' in result: flash_message(action_msg(result))          # Set flash message
        template_filename = "web/%s.mako" % result['template']             # Find template filename
        if request.environ['is_mobile']:                                   # If mobile rendering
            # TODO: detect mobile template
            #   - (middleware needs to be upgraded  to look for subdomain m. in url)
            mobile_template_filename = "mobile/%s.mako" % result['template']
            # if exists(mobile_template_filename)
            #   template_filename = mobile_template_filename
        return render_mako(template_filename)
        # Used to use HTMLFILL, but this was incompatable with JSON and XML as formencode.Invalid were objects
        # Now the python dict has an ['error'] attribute that templates render themselfs
        # it may even be possible for us to create our own poor mans htmlfill that overlays the html with our own validation data
        #if 'htmlfill' in result: return formencode.htmlfill.render(html, **result['htmlfill'])
        #else                   : return html

    
    return dict(
        python = lambda result:result,
        json   = format_json,
        xml    = format_xml,
        rss    = format_rss,
        html   = format_html,
    )


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
        - PYTHON (just the plain python dict for internal calls)
            
    Should be passed a python dictonary containing
        {
            data   : the python dict to render (required) if not present will just pass though this decorator
            
            status : 'ok' or 'error' (optional defaults to ok)
            message: the flash message or error message (optional: default '')
            
            htmlfill: (optional) kwargs for the htmlfill system (html rendering only)
            template: (required for html rendering) the template name, will default to XML if format==html and template not specifyed
        }
    """
    
    default_format    = config['default_format']
    format_processors = get_format_processors()
    
    def my_decorator(target):
        def wrapper(target, *args, **kwargs):
            # Before
            #  do nothing
            log.debug('calling %s with args: %s kwargs: %s' % (target.__name__, args, kwargs))
            
            # Origninal method call
            result = target(*args, **kwargs) # Execute the wrapped function
            
            # After
            
            # Is return is a dict?
            if hasattr(result, "keys") and 'data' in result:
                
                # Set default FORMAT (if nessisary)
                format = default_format
                if c.format          : format = c.format
                if len(args)==3 and args[2] in format_processors: format = args[2] # The 3rd arg should be a format, if it is a valid format set it
                if 'format' in kwargs: format = kwargs['format'] #FIXME? the kwarg format is NEVER passed :( this is why we reply on c.format (set by the base controler)
                if format=='html' and 'template' not in result: format='xml' #If format HTML and no template supplied fall back to XML
                
                # Set default STATUS and MSG (if nessisary)
                if 'status'  not in result: result['status']  = 'ok'
                if 'message' not in result: result['message'] = ''

                # set the HTTP status code
                if 'code' in result:
                    response.status = int(result['code'])
                    del response['code']
                
                # Render to format
                if format in format_processors:
                    return format_processors[format](result)
                
            # If pre-rendered HTML or JSON or unknown format - just pass it through, we can not format it any further
            return result
        
        return decorator(wrapper)(target) # Fix the wrappers call signiture
    return my_decorator
