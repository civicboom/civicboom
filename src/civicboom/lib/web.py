from pylons import session, url, request, response
from pylons.controllers.util import redirect

from webhelpers.html import literal

import time
import json
from decorator import decorator
import logging

log = logging.getLogger(__name__)


#-------------------------------------------------------------------------------
# Misc
#-------------------------------------------------------------------------------

def flash_message(message):
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
        url_to = url.current()
    return redirect(url_to)


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
                    flash_message(str(result))
                    return redirect(action_redirect)
                else:
                    log.warning("Redirect loop detected for "+str(action_redirect))
                    return redirect("/")

        return decorator(wrapper)(target) # Fix the wrappers call signiture
    return my_decorator

def action_ok(msg, data=None):
    return json.dumps({
        "status": "ok",
        "message": msg,
        "data": data,
    })

def action_error(msg, data=None):
    return json.dumps({
        "status": "error",
        "message": msg,
        "data": data,
    })

