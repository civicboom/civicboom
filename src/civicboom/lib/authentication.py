"""
Tools used for Authentication of users
"""

# Pylons imports
from civicboom.lib.base import redirect, _, ungettext, render, c, request, url, flash_message

# Civicboom imports
from civicboom.model      import User, UserLogin
from civicboom.model.meta import Session

from civicboom.lib.misc import session_set

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

def get_user_and_check_password(username, password):
    """
    Called by account controller and/or AuthKit valid_password to return a user from local db
    """
    password = hashlib.sha1(password).hexdigest()
    try:
        q = Session.query(User).select_from(join(User, UserLogin, User.login_details))
        q = q.filter(User.username   == username  )
        q = q.filter(User.status     == 'active'  )
        q = q.filter(UserLogin.type  == 'password')
        q = q.filter(UserLogin.token == password  )
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
        q = q.filter(User.status     == 'active'  )
        q = q.filter(UserLogin.token == identifyer )
        q = q.one()
        return q
    except:
        return None    


#-------------------------------------------------------------------------------
# AuthKit
#-------------------------------------------------------------------------------
# This section could be removed completely and the rest of the site will still function as authorise is overwritten in the Custom Login Section

# Authkit imports
from authkit.permissions import RequestPermission
from authkit.authorize   import PermissionError, NotAuthenticatedError
from authkit.authorize   import NotAuthorizedError, middleware
from authkit.authorize.pylons_adaptors import authorize


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
    return redirect_to('/')
    
    

   
#-------------------------------------------------------------------------------
# Custom Authentication
#-------------------------------------------------------------------------------

# Todo - look into how session is verifyed - http://pylonshq.com/docs/en/1.0/sessions/#using-session-in-secure-forms
#        what is the secure form setting for?

#is_valid_user=None # Override for AuthKit transition, if this is remmed out AuthKit can be re-endabled without any changes to controlers
#def login_redirector(authenticator):

# Override AuthKits authorise method with our own custom login decorator
def authorize(authenticator):
    """
    Check if logged in user has been set
    If not sends you to a login page
    Once you log in, it sends you back to the original url call.
    """
    def my_decorator(target):
        def wrapper(target, *args, **kwargs):

            if c.logged_in_user:
                result = target(*args, **kwargs)
            else:
                session_set('login_redirect', request.environ.get('PATH_INFO'), 60 * 10) # save timestamp with this url, expire after 5 min, if they do not complete the login process
                # TODO: This could also save the the session POST data and reinstate it after the redirect
                return redirect(url(controller='account', action='signin'))

            return result
        return decorator(wrapper)(target)
    return my_decorator

