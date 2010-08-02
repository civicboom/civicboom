from pylons import session, url, request
from pylons.controllers.util import redirect

from webhelpers.html import literal

import time

#-------------------------------------------------------------------------------
# Web
#-------------------------------------------------------------------------------

def flash_message(message):
    if 'flash_message' in session:
        session['flash_message'] = session['flash_message'] + literal("<br/>") + message
    else:
        session['flash_message'] = message
    #session.save() # Unneeded as auto is set to true in the session setup in the ini

def redirect_to_referer():
    url_to = request.environ.get('HTTP_REFERER')
    if url_to == url.current(): # Detect if we are in a redirection loop and abort
        redirect('/')
    if not url_to:
        url_to = url.current()
    return redirect(url_to)



def session_remove(key):
    del session[key]
    del session[key+'_expire']

def session_set(key, value, duration):
    """
    duration in seconds
    """
    session[key]           = value
    session[key+'_expire'] = time.time() + duration
    pass

def session_get(key):
    value      = None
    key_expire = key+'_expire'
    if key_expire in session:  
        if time.time() > float(session[key_expire]):
            session_remove(key)
    if key in session:
        return session[key]
    return  None




#-------------------------------------------------------------------------------
# Misc
#-------------------------------------------------------------------------------

def remove_where(list, check_for_removal_function):
    """
    Remove items from a list is the removal function returns True
    """
    for item in list:
        if check_for_removal_function(item):
            list.remove(item)


def dict_to_stringprint(d, indent=''):
    """
    Iterate though dictionatys and sub dictonarys creating a formatted plain text string
    Useful for debugging
    """
    s = ''
    if hasattr(d,'keys'):
      keylist = d.keys()
      keylist.sort()
      for key in keylist:
        s += key +"\n"+ dict_to_stringprint(d.get(key), indent=indent+'  ')
    else:
        s += indent + str(d) + "\n"
    return s