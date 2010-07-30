"""
Tools used for Authentication of users
"""

# Pyhton package imports
import hashlib
import decorator

# Pylons imports
from civicboom.lib.base import redirect, _, session, render
#from pylons.i18n.translation import _, ungettext

# Civicboom imports
from civicboom.lib.misc   import flash_message
from civicboom.model      import User, UserLogin
from civicboom.model.meta import Session

# Other imports
from sqlalchemy.orm import join


# Authkit imports
from authkit.permissions import RequestPermission
from authkit.authorize   import PermissionError, NotAuthenticatedError
from authkit.authorize   import NotAuthorizedError, middleware
from authkit.authorize.pylons_adaptors import authorize
#from pylons.templating  import render_mako as render # for render of the signin page (activated outside of the normal base controler as the middleware intercepts it)



# Logging
import logging
user_log = logging.getLogger("user")


#-------------------------------------------------------------------------------
# Custom Civicboom Authentication
#-------------------------------------------------------------------------------

# Todo - look into how session data is verifyed - http://pylonshq.com/docs/en/1.0/sessions/#using-session-in-secure-forms

#@authorize(is_valid_user)
def login_redirector(func, *args, **kargs):
    """
    Check if logged in user has been set
    If not sends you to a login page
    Once you log in, it sends you back to the original url call.
    """
    if c.logged_in_user:
        return func(*args, **kargs)
    else:
        session['login_redirect'] = request.environ.get('PATH_INFO')
        # TODO: This could also save the the session POST data and reinstate it after the redirect
        # TODO: save a timestamp with this url, expire after 10 min, if they do not complete the login process
        #session.save()
        return redirect(url(controller='account', action='signin_janrain'))
#login_redirector = decorator(login_redirector)


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
    def get_user_and_check_password(username, password):
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