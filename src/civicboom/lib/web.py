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
    return redirect(url_to)


#-------------------------------------------------------------------------------
# Session Timed Keys Management
#-------------------------------------------------------------------------------
# sessions can be given a key pair with an expiry time
# a fetch with session_get will get the session value, but will return None if it's _exipre pair has expired
    

def session_remove(key):
    value = session_get(key)
    if key           in session: del session[key]
    if key+'_expire' in session: del session[key+'_expire']
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
            session_remove(key)
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


def action_ok(message=None, data=None, code=200, template=None):
    return {
        "status" : "ok",
        "message": message,
        "data"   : data,
        "code"   : code,
        "template": template,
    }

def action_error(message=None, data=None, code=500):
    return {
        "status" : "error",
        "message": message,
        "data"   : data,
        "code"   : code,
    }

def overlay_status_message(master_message, new_message):
    """

    """
    # Setup master message
    if not master_message:
        master_message = {}
    master_message['status']  = master_message.get('status', 'ok')
    master_message['message'] = master_message.get('message', u'')

    # Overlay new message (if dict)
    if 'status' in new_message:
        if master_message['status'] == 'ok':
            master_message['status'] = new_message['status']
    if 'message' in new_message and new_message['message']:
        master_message['message'] += '\n' + new_message['message']

    # Overlay new message (if string)
    if isinstance(new_message, basestring):
        master_message['message'] += '\n' + new_message

    # Tidy message whitespace
    master_message['message'] = master_message['message'].strip()

    return master_message


#-------------------------------------------------------------------------------
# Auto Format Output
#-------------------------------------------------------------------------------

#To be depricated?
"""
def get_format_processors_pre():
    def format_redirect():
        #if session_get('action_redirect') == None and 'HTTP_REFERER' in request.environ:
        #    session_set('action_redirect', request.environ.get('HTTP_REFERER'), 60 * 5)
        
        # WHAT? I just looked at this ... why are we using a session? we have our own state after the action is performed so why bother with a session?
        pass
    
    return dict(
        redirect = format_redirect,
    )
"""

def get_format_processors_end():
    def format_json(result):
        response.headers['Content-type'] = "application/json"
        return json.dumps(result)
        
    def format_xml(result):
        response.headers['Content-type'] = "text/xml"
        return dictToXMLString(result)
        
    def format_rss(result):
        response.headers['Content-type'] = "application/rss+xml"
        return 'implement RSS' # TODO: ???
    
    def format_html(result):
        overlay_status_message(c.result, result)                           # Set standard template data dict for template to use
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
        if 'message' in result: set_flash_message(result) # Set flash message
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
        redirect = format_redirect,
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
        - REDIRECT (compatable old borswer action to have session message set and redirected to referer)
            
    Should be passed a python dictonary containing
        {
            data   : the python dict to render (required) if not present will just pass though this decorator
            
            status : 'ok' or 'error' (optional defaults to ok)
            message: the flash message or error message (optional: default '')
            
            htmlfill: (optional) kwargs for the htmlfill system (html rendering only)
            template: (required for html rendering) the template name, will default to XML if format==html and template not specifyed
        }
    """
    
    format_processors_end = get_format_processors_end()
    #format_processors_pre = get_format_processors_pre()
    
    def my_decorator(target):
        def wrapper(target, *args, **kwargs):
            
            #if format in format_processors_pre:
            #    format_processors[format]()

            # Origninal method call
            result = target(*args, **kwargs) # Execute the wrapped function

            
            # After
            # Is result a dict with data?
            if hasattr(result, "keys"): #and 'data' in result # Sometimes we only return a status and msg, cheking for data is overkill

                # Set default FORMAT (if nessisary)
                format = c.format
                if len(args)==3 and args[2] in format_processors_end and args[2]: format = args[2] # The 3rd arg should be a format, if it is a valid format set it
                if 'format' in kwargs                                       : format = kwargs['format'] #FIXME? the kwarg format is NEVER passed :( this is why we reply on c.format (set by the base controler)
                
                if format=='html' and 'template' not in result:
                    log.warning("Format HTML with no template")
                    format='xml' #If format HTML and no template supplied fall back to XML
                
                # Set default STATUS and MSG (if nessisary)
                if 'status'  not in result: result['status']  = 'ok'
                if 'message' not in result: result['message'] = ''
                
                # set the HTTP status code
                if 'code' in result:
                    response.status = int(result['code'])
                    del result['code']
                
                # Render to format
                if format in format_processors_end:
                    return format_processors_end[format](result)
                else:
                    log.warning("Unknown format: "+str(format))
                
            # If pre-rendered HTML or JSON or unknown format - just pass it through, we can not format it any further
            log.debug("returning pre-rendered stuff")
            return result
        
        return decorator(wrapper)(target) # Fix the wrappers call signiture
    return my_decorator
