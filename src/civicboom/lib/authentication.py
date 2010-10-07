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
log = logging.getLogger(__name__)
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

def is_valid_user(u):
    return u


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
    @decorator
    def wrapper(target, *args, **kwargs):

        # CHECK Loggin in
        if authenticator(c.logged_in_user):
            # Reinstate any session encoded POST data if this is the first page since the login_redirect
            if not session_get('login_redirect'):
                json_post = session_remove('login_redirect_post')
                if json_post:
                    post_overlay = json.loads(json_post)
                    c.target_url = "http://" + request.environ.get('HTTP_HOST') + request.environ.get('PATH_INFO')
                    c.post_values = post_overlay
                    from pylons.templating import render_mako as render # FIXME: how is this not imported from base? :/
                    return render("web/design09/misc/confirmpost.mako")

            # Make original method call
            result = target(*args, **kwargs)
            return result

        # ELSE Unauthorised
        else:
            # If request was a browser - prompt for login
            if c.format == "redirect":
                raise action_error(message="implement me, redirect authentication needs session handling of http_referer")
            if c.format == "html":
                redirect_url = "http://" + request.environ.get('HTTP_HOST') + request.environ.get('PATH_INFO') # AllanC - is there a way of just getting the whole request URL? why do I have to peice it together myself!
                if 'QUERY_STRING' in request.environ:
                    redirect_url += '?'+request.environ.get('QUERY_STRING')
                session_set('login_redirect'     , redirect_url, 60 * 10) # save timestamp with this url, expire after 5 min, if they do not complete the login process
                # save the the session POST data to be reinstated after the redirect
                if request.POST:
                    session_set('login_redirect_post', json.dumps(multidict_to_dict(request.POST)), 60 * 10) # save timestamp with this url, expire after 5 min, if they do not complete the login process
                return redirect(url_from_widget(controller='account', action='signin', protocol="https")) #This uses the from_widget url call to ensure that widget actions preserve the widget env

            # If API request - error unauthorised
            else:
                raise action_error(message="unauthorised", code=403) #Error to be formared by auto_formatter

    return wrapper

def login_redirector():
    """
    If this method returns (rather than aborting with a redirect) then there is no login_redirector
    """
    login_redirect = session_remove('login_redirect')
    if login_redirect:
        return redirect(login_redirect)


def signin_user(user, login_provider=None):
    """
    Perform the sigin for a user
    """
    user_log.info("logged in with %s" % login_provider)   # Log user login
    session_set('user_id' , user.id      ) # Set server session variable to user.id
    session_set('username', user.username) # Set server session username so in debug email can identify user    
    response.set_cookie("civicboom_logged_in" , "True", int(config["beaker.session.timeout"]))

def signin_user_and_redirect(user, login_provider=None):
    """
    Perform the sigin for a user
    """
    signin_user(user, login_provider)
    
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
