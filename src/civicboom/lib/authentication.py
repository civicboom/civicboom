"""
Tools used for Authentication of users
"""

# Pylons imports
from civicboom.lib.base import redirect, _, ungettext, render, c, request, url, flash_message, session, response, config

# Civicboom imports
from civicboom.model      import User, UserLogin
from civicboom.model.meta import Session

from civicboom.lib.web     import session_set, session_get, session_remove
from civicboom.lib.helpers import url_from_widget

# Other imports
from sqlalchemy.orm import join

# Pyhton package imports
import hashlib
from decorator import decorator

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

# Authkit imports
from authkit.permissions import RequestPermission
from authkit.authorize   import PermissionError, NotAuthenticatedError
from authkit.authorize   import NotAuthorizedError, middleware
#from authkit.authorize.pylons_adaptors import authorize


class ValidCivicboomUser(RequestPermission):
    """
    Skeliton class to check for a Civicboom user to be present
    """
    def __init__(self, accept_empty=False):
        self.accept_empty = accept_empty
    def check(self, app, environ, start_response):
        if 'REMOTE_USER' not in environ:
            raise NotAuthenticatedError('Not Authenticated')
        return app(environ, start_response)
is_valid_user = ValidCivicboomUser()


def valid_username_and_password(environ, username, password):
    """
    Check local db if a users username and password are valid
    
      for AuthKit, this function is pointed too from the development.ini file
      authkit.form.authenticate.function = civicboom.lib.authentication:valid_username_and_password
    """
    user = get_user_and_check_password(username, password)
    if user:
        user_log.info(user)
        return True
    else:
        flash_message(_("Incorrect username and password"))
        return False


def render_signin():
    """
    AuthKit Render Signin
    Reference: http://pylonsbook.com/en/1.1/simplesite-tutorial-part-3.html#styling-the-sign-in-screen

      for AuthKit, this function is pointed too from the development.ini file
      authkit.form.template.obj          = civicboom.lib.authentication:render_signin
    """
    # Future placeholder for differnt login pages based
    #setup_widget_env()
    #if c.widget_reporter: #if identify_widget_url():
    #  result = render('/design09/widget/widget_signin.mako')
    #elif identify_mobile_url():
    #  result = render('/design09/mobile/mobile_signin.mako')
    #else:
    result = render('/web/account/signin.mako')
    result = result.replace('%', '%%').replace('FORM_ACTION', '%s') #VERY IMPORTANT! because this is executing outside of the normal page framework
    return str(result)

def render_badcookie():
    """
    Cookie Expired Page
    had these in the ini file
      authkit.cookie.badcookie.page         = false
      authkit.cookie.badcookie.template.obj = indicofb.lib.auth_permissions:render_badcookie
    (AllanC - could not get this to work WTF?)
    """
    flash_message(_("Your login has expired please log in again"))
    return redirect('/')
    
    

   
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
                result = target(*args, **kwargs)
            else:
                # AllanC - is there a way of just getting the whole request URL? why do I have to peice it together myself!
                redirect_url = "http://" + request.environ.get('HTTP_HOST') + request.environ.get('PATH_INFO')
                if 'QUERY_STRING' in request.environ:
                    redirect_url += '?'+request.environ.get('QUERY_STRING')
                    
                session_set('login_redirect', redirect_url, 60 * 10) # save timestamp with this url, expire after 5 min, if they do not complete the login process
                # TODO: This could also save the the session POST data and reinstate it after the redirect
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
    
    # If no redirect send them to the page root
    return redirect('/')
    
def signout_user(user):
    user_log.info("logged out")
    session.clear()
    response.set_cookie("civicboom_logged_in", None)
    request.cookies.pop("civicboom_logged_in", None) #AllanC This does not seem to remove the item - hence the "None" set in the line above, sigh :(
    #session.save()
    #flash_message("Successfully signed out!")
