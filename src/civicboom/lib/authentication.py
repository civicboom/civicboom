"""
Tools used for Authentication of users
"""

# Pylons imports
from civicboom.lib.base import *

# Civicboom imports
from civicboom.model      import User, UserLogin
from civicboom.model.meta import Session

from civicboom.lib.web     import session_set, session_get, session_remove, multidict_to_dict
from civicboom.lib.helpers import url_from_widget

# Other imports
from sqlalchemy.orm import join

# Pyhton package imports
import hashlib
from decorator import decorator
import json

# Logging
import logging
user_log = logging.getLogger("user")



#-------------------------------------------------------------------------------
# Standard Tools
#-------------------------------------------------------------------------------

def encode_plain_text_password(password):
    return hashlib.sha1(password).hexdigest()

def get_user_and_check_password(username, password):
    """
    Called by account controller and/or AuthKit valid_password to return a user from local db
    """
    try:
        q = Session.query(User).select_from(join(User, UserLogin, User.login_details))
        q = q.filter(User.username   == username  )
        q = q.filter(User.status     == 'active'  )
        q = q.filter(UserLogin.type  == 'password')
        q = q.filter(UserLogin.token == encode_plain_text_password(password))
        q = q.one()
        return q
    except:
        return None


def get_user_from_openid_identifyer(identifyer):
    """
    Called by account controller to return a user from our db from an openid identifyer
    """
    try:
        q = Session.query(User).select_from(join(User, UserLogin, User.login_details))
        #q = q.filter(User.status     == 'active'  ) # the base controler checks for pending status and redirects to login page accordingly
        q = q.filter(UserLogin.token == identifyer )
        q = q.one()
        return q
    except:
        return None



#-------------------------------------------------------------------------------
# AuthKit
#-------------------------------------------------------------------------------
# This section could be block remmed or removed and the rest of the site will still function as authorise is overwritten in the Custom Login Section

is_valid_user = None

   
#-------------------------------------------------------------------------------
# Custom Authentication
#-------------------------------------------------------------------------------

# Todo - look into how session is verifyed - http://pylonshq.com/docs/en/1.0/sessions/#using-session-in-secure-forms
#        what is the secure form setting for?

#is_valid_user=None # Override for AuthKit transition, if this is remmed out AuthKit can be re-endabled without any changes to controlers
#def login_redirector(authenticator):

# Override AuthKits authorise method with our own custom login decorator
# To degrade back to AuthKit rename this method
def authorize(authenticator):
    """
    Check if logged in user has been set
    If not sends you to a login page
    Once you log in, it sends you back to the original url call.
    """
    def my_decorator(target):
        # do something with authenticator here if needed
        def wrapper(target, *args, **kwargs):

            if c.logged_in_user:

                # Reinstate any session encoded POST data if this is the first page since the login_redirect
                if not session_get('login_redirect'):
                    json_post = session_get('login_redirect_post')
                    session_remove('login_redirect_post')
                    if json_post:
                        post_overlay = json.loads(json_post)
                        #for key in post_overlay.keys():
                        #    request.POST[key] = post_overlay[key]
                        #request.POST = post_overlay
                        # TODO - want to re-instate post_overlay over request.POST but the security model wont let me :(
                        
                # Make original method call
                result = target(*args, **kwargs)
            else:
                # AllanC - is there a way of just getting the whole request URL? why do I have to peice it together myself!
                redirect_url = "http://" + request.environ.get('HTTP_HOST') + request.environ.get('PATH_INFO')
                if 'QUERY_STRING' in request.environ:
                    redirect_url += '?'+request.environ.get('QUERY_STRING')
                    
                session_set('login_redirect'     , redirect_url, 60 * 10) # save timestamp with this url, expire after 5 min, if they do not complete the login process
                
                # save the the session POST data to be reinstated after the redirect
                if request.POST:
                    session_set('login_redirect_post', json.dumps(multidict_to_dict(request.POST)), 60 * 10) # save timestamp with this url, expire after 5 min, if they do not complete the login process
                
                return redirect(url_from_widget(controller='account', action='signin', protocol="https")) #This uses the from_widget url call to ensure that widget actions preserve the widget env
            return result
        
        return decorator(wrapper)(target)
    return my_decorator

def login_redirector():
    """
    If this method returns (rather than aborting with a redirect) then there is no login_redirector
    """
    login_redirect = session_get('login_redirect')
    if login_redirect:
        session_remove('login_redirect')
        return redirect(login_redirect)


def signin_user(user):
    """
    Perform the sigin for a user
    """
    user_log.info("logged in")   # Log user login
    session['user_id' ] = user.id       # Set server session variable to user.id
    session['username'] = user.username # Set server session username so in debug email can identify user    
    response.set_cookie("civicboom_logged_in" , "True", int(config["beaker.session.timeout"]))
    
    if 'popup_close' in request.params:
        # Redirect to close the login frame, but keep the login_redirector for a separte call later
        return redirect(url(controller='misc', action='close_popup'))
    
    # Redirect them back to where they were going if a redirect was set
    login_redirector()
    
    # If no redirect send them to private profile and out of https and back to http
    return redirect(url(controller="profile", action="index", protocol="http"))
    
def signout_user(user):
    user_log.info("logged out")
    session.clear()
    response.delete_cookie("civicboom_logged_in")
    #session.save()
    #flash_message("Successfully signed out!")
